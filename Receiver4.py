# Rohit Alen s2210057
from socket import *
import sys
import time
import struct

#receive data
def receive_file(port,filename,window_size):
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('localhost',port))
    file = bytearray()
    dict_packet = dict()
    last_sequenceno = pow(2, 16)
    base = 1
    packets = struct.pack('H', 0)
    last_packet = False
    addr = None
    while True:
        if base > last_sequenceno:
            break
        data, addr = s.recvfrom(1027)
        if data[2] == 1 :
            last_packet = True
        if not addr:
            addr = addr
        sequence_number = struct.unpack('H', data[0:2])[0]
        if last_packet:
            last_sequenceno = sequence_number
        if sequence_number in range(base - window_size, base):
            packets = struct.pack('H', sequence_number)
            s.sendto(packets, addr)
        if (sequence_number >= base and sequence_number < base + window_size):
            packetData = data[3:]
            packets = struct.pack('H', sequence_number)
            s.sendto(packets, addr)
            dict_packet[sequence_number] = packetData
            if sequence_number == base:
                window_acked = True
                for window_packet in range(base, base + window_size):
                    if not window_packet in dict_packet:
                        base = window_packet
                        window_acked = False
                        break
                    else:
                        file += dict_packet[window_packet]
                if window_acked:
                    base += window_size
    #for last packet
    ack_window = []
    for seq_num in range(0, window_size):
        if last_sequenceno - seq_num >= 1:
            ack_window.append((last_sequenceno - seq_num, struct.pack('H',last_sequenceno-seq_num)))
    for i in range(5):
        time.sleep(40/1000)
        for (sequence_number, packet) in sorted(ack_window, key=lambda x: x[0]):
            s.sendto(packet, addr)

    with open(filename, 'wb') as f:
        f.write(file)
        f.close()
    s.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 Receiver2.py <Port> <Filename> ,<WindowSize>")
        sys.exit(1)

    port = int(sys.argv[1])
    filename = sys.argv[2]
    window_size = int(sys.argv[3])

    receive_file(port, filename, window_size)
