# Rohit Alen s2210057
import socket
import sys

def receive_file(port, filename):
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', port))
    
    # Open file for writing
    with open(filename, 'wb') as file:
        while True:
            # Receive packet
            
            packet, addr = s.recvfrom(1027)
            
            # Extract sequence number and EoF flag from header
            sequence_number = int.from_bytes(packet[:2], 'big')
            eof_flag = int.from_bytes(packet[2:3], 'big')
            # Write data to file (excluding header)
            file.write(packet[3:])
            
            # Check for EoF flag
            if eof_flag == 1:
                break
            

    s.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 Receiver1.py <Port> <Filename>")
        sys.exit(1)

    port = int(sys.argv[1])
    filename = sys.argv[2]

    receive_file(port, filename)