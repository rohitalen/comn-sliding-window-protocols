
from socket import *
import sys
import os
import struct
import time
from threading import Thread, Lock
# define threads
def receive_ack():
    global timeOut
    global fileSent
    global time_out_thread
    global base
    global acks
    global lastWindowAck
    global timer_on
    global lock

    while(True):
        if fileSent:
            break
        data, addr= s.recvfrom(2)
        ackNum = struct.unpack('H', data[0:2])[0]
        with lock:
            acks.add(ackNum)
            if ackNum in range(len(packetsList) - window_size, len(packetsList)+1):
                lastWindowAck = True
            if ackNum == base:
                packets_acked = True
                for pack in range(base, next_sequenceNo):
                    if pack not in acks:
                        base = pack
                        packets_acked = False
                        break
                if packets_acked:
                    base = next_sequenceNo
                    timer_on = False
                else:
                    timer_on = True
                    timeOut = time.perf_counter()


def time_out():
    global retry_timeout
    global timer_on
    global lock
    global acks
    global timeOut
    global base
    global next_sequenceNo
    global lastWindowAck
    global lastWindowCount
    global fileSent
    global retry_lastWindow

    while(True):
        curent_time = time.perf_counter()
        with lock:
            if fileSent:
                break
            if not timer_on:
                continue
            if curent_time - timeOut < retry_timeout:
                continue
            else:
                timeOut = time.perf_counter()
            if len(packetsList) == len(acks):
                fileSent = True
                break
            if lastWindowCount == retry_lastWindow:
                fileSent = True
                break
            if lastWindowAck:
                lastWindowCount += 1
            
            change = 0
            while (base + change < next_sequenceNo):
                if (base + change >= len(fullPackets)):
                    break
                if (base + change) not in acks:
                    s.sendto(fullPackets[base + change], (remote_host, port))
                change += 1

def send_packet(packet_data, isLast_packet):
    global timeOut
    global timer_on
    global lock
    global base
    global next_sequenceNo
    
    with lock:
        if(next_sequenceNo < base + window_size):
            sequence_number = struct.pack('H', next_sequenceNo)
            if isLast_packet :
                eof_header = struct.pack('B', 1)
            else:
                eof_header = struct.pack('B', 0)
            fullPackets[next_sequenceNo] = sequence_number + eof_header + packet_data
            s.sendto(fullPackets[next_sequenceNo], (remote_host, port))
            if (base == next_sequenceNo):
                timer_on = True
                timeOut = time.perf_counter()
            next_sequenceNo += 1
            return True
        else:
            return False
# Initialize everything       
remote_host = sys.argv[1]
port =int(sys.argv[2])
filename = sys.argv[3]
retry_timeout = float(int(sys.argv[4])/float(1000))
window_size = int(sys.argv[5])
retry_lastWindow = 10
s = socket(AF_INET, SOCK_DGRAM) 
packetsList = []
with open(filename, 'rb') as fs:
    packet = fs.read(1024)
    while (packet):
        packetsList.append(packet)
        packet = fs.read(1024)
    fs.close()
next_sequenceNo = 1
base = 1
timer_on = True
lastFree = 0
acks = set()
lastWindowAck = False
lastWindowCount = 0
#lock
lock = Lock()
fullPackets = [None] * (len(packetsList) + 1)
fileSent = False
timeOut = time.perf_counter()
receeive_ack_thread = Thread(target=receive_ack)
time_out_thread = Thread(target=time_out)
start_time = time.perf_counter()
receeive_ack_thread.start()
time_out_thread.start()

while(not fileSent):
    if len(packetsList) == len(acks):
        with lock:
            fileSent = True
    if lastFree == len(packetsList):
        continue
    nextPacket = packetsList[lastFree]
    if (send_packet(nextPacket, lastFree == len(packetsList) - 1)):
        lastFree += 1


end_time = time.perf_counter()
file_size = os.path.getsize(filename)
throughput = (file_size / 1024) / (end_time - start_time)
print(f"{throughput:.2f}")
s.close()
sys.exit() #exit program