# Rohit Alen s2210057
import socket
import sys

def send_file(remote_host, port, filename):
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Read the file
    with open(filename, 'rb') as file:
        sequence_number = 0
        eof_flag = 0
        while True:
            # Read 1024 bytes of data from the file
            data = file.read(1024)
            if len(data) < 1024:
               eof_flag = 1  # Set EOF flag
            else:
               eof_flag = 0 
            
            # Create header with sequence number and EoF flag
            header = sequence_number.to_bytes(2, 'big') + eof_flag.to_bytes(1, 'big')
            
            # Combine header and data
            packet = header + data
            
            # Send packet to the receiver
            s.sendto(packet, (remote_host, port))
            if (eof_flag) ==1:
                break
            # Increment sequence number
            sequence_number += 1

    s.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 Sender1.py <RemoteHost> <Port> <Filename>")
        sys.exit(1)

    remote_host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    send_file(remote_host, port, filename)
    