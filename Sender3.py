# Rohit Alen s2210057
import socket
import sys
import os
import math
import time
import select

def send_file(remote_host, port, filename, retry_timeout, window_size):

    with open(filename, 'rb') as f:
        fr = f.read()
        image = bytearray(fr)

    start_time = time.perf_counter()
    isSent = False

    try:
        base = -1
        sequence_number = 0
        lastSeqNum = math.ceil(float(len(image))/float(1024))
        lastPacketSize = len(image) - (lastSeqNum * 1024)
        isSent = False
        while isSent is False:
            #send packet while window in range
            while sequence_number - base <= window_size and sequence_number <= lastSeqNum:
                send_packet(sequence_number, lastSeqNum, lastPacketSize, image, remote_host, port)
                sequence_number +=1
            try:
                base = get_ack(base, retry_timeout)
            except socket.error as exc:
                sequence_number = base + 1
                if base == lastSeqNum:
                    isSent = True
    except socket.error as exc:
                print ("socket error : %s" %exc)

    end_time = time.perf_counter()
    file_size = os.path.getsize(filename)
    throughput = (file_size / 1024) / (end_time - start_time)
    print(f"{throughput:.2f}")
    s.close()

def get_ack(base, retry_timeout):
    s.settimeout(retry_timeout/1000)
    data, addr = s.recvfrom(2)
    ackSeqNum = int.from_bytes(data[:2], 'big')
    if base < ackSeqNum:
        return ackSeqNum
    else:
        return get_ack(base, retry_timeout)

def send_packet(sequence_number, lastSeqNo, lastPacketSize, image, remote_host, port):
    #set eof flag
    if sequence_number == lastSeqNo:
        eof_flag = 1
    else:
        eof_flag = 0
    if eof_flag != 1:
        size = 1024
    else:
        size = lastPacketSize
    packet = bytearray(sequence_number.to_bytes(2, byteorder='big'))
    packet.append(eof_flag)
    start = sequence_number*1024
    end = start + size
    packet.extend(image[start:end])
    try: 
        s.sendto(packet, (remote_host, port))
    except socket.error:
        select.select([],[s],[])

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 Sender3.py <RemoteHost> <Port> <Filename> <RetryTimeout> <WindowSize>")
        sys.exit(1)

    remote_host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
    retry_timeout = int(sys.argv[4])
    window_size = int(sys.argv[5])
    # Set up socket
    
    s = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    s.setblocking(False)
    #s.close()
    send_file(remote_host, port, filename, retry_timeout, window_size)
