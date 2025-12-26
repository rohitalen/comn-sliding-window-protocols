# Rohit Alen s2210057
import socket
import sys 

def receive_file(port,filename):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('localhost', port))
    file = bytearray()
    sequence_number = 0
    next_sequence_number = 0
    #receive data and send acks
    while True:
        data, addr = s.recvfrom(1027) 
        sequence_number = int.from_bytes(data[:2],'big')
        if sequence_number == next_sequence_number:
            file.extend(data[3:])
            next_sequence_number += 1
        if next_sequence_number == 0 :
            ack_number = 0
        else :
            ack_number = next_sequence_number - 1
        packet = bytearray(ack_number.to_bytes(2, byteorder='big'))
        s.sendto(packet, addr)
        #if not in order
        while next_sequence_number != sequence_number + 1:
            data, addr = s.recvfrom(1027) 
            sequence_number = int.from_bytes(data[:2],'big')
            if sequence_number == next_sequence_number:
                file.extend(data[3:])
                next_sequence_number += 1
            if next_sequence_number == 0 :
                ack_number = 0
            else :
                ack_number = next_sequence_number - 1
            packet = bytearray(ack_number.to_bytes(2, byteorder='big'))
            s.sendto(packet, addr)
        if(data[2] == 1):
            x=0
            while(x<50):
                packet = bytearray(sequence_number.to_bytes(2, byteorder='big'))
                s.sendto(packet, addr)
                x+=1
            break 
    with open(filename, 'wb') as f:
        f.write(file)

    s.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 Receiver2.py <Port> <Filename>")
        sys.exit(1)

    port = int(sys.argv[1])
    filename = sys.argv[2]

    receive_file(port, filename)