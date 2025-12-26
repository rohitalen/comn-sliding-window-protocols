# Rohit Alen s2210057
import socket
import sys

def receive_file(port, filename):
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('localhost', port))
    
    # Open file for writing
    with open(filename, 'wb') as file:
        expected_sequence_number = 0
        
        while True:
            # Receive packet
            packet, addr = s.recvfrom(1027)
            # Extract sequence number and EoF flag from header
            sequence_number = int.from_bytes(packet[:2], 'big')
            eof_flag = int.from_bytes(packet[2:3], 'big')
            
            # Check for duplicate detection
            if sequence_number == expected_sequence_number:
                ack_packet = sequence_number.to_bytes(2, 'big')
                s.sendto(ack_packet, addr)
                file.write(packet[3:])
                if eof_flag == 1:
                    x=0
                    while(x<50):
                        s.sendto(ack_packet, addr)
                        x+=1
                    break
                # Toggle expected sequence number
                expected_sequence_number = 1 - expected_sequence_number
            else:
                # If duplicate, send ACK with the previous sequence number
                ack_packet = sequence_number.to_bytes(2, 'big')
                s.sendto(ack_packet, addr)
    print("closed")
    s.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 Receiver2.py <Port> <Filename>")
        sys.exit(1)

    port = int(sys.argv[1])
    filename = sys.argv[2]

    receive_file(port, filename)
