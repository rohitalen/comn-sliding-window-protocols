# Rohit Alen s2210057
import socket
import sys
import os
import time
# add input validation --retry timeout should be positive
def send_file(remote_host, port, filename, retry_timeout):
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Read the file
    with open(filename, 'rb') as file:
        sequence_number = 0
        retransmissions = 0
        start_time = time.time()
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
            s.sendto(packet, (remote_host, port))
            while True:
                try:
                    # Set a timeout for receiving ACK
                    s.settimeout(retry_timeout/1000)  # Convert timeout to mseconds
                    # Receive ACK
                    ack_packet, addr = s.recvfrom(2)
                    ack_sequence_number = int.from_bytes(ack_packet[:2], 'big')
                    if sequence_number==ack_sequence_number:
                        sequence_number = 1 - sequence_number # Toggle sequence number
                        break
                except socket.timeout:
                    s.sendto(packet, (remote_host, port))
                    retransmissions+=1
            if (eof_flag) ==1:
                end_time=time.time()
                break
    
    s.close()
    
    # Calculate throughput
    file_size = os.path.getsize(filename)
    throughput = (file_size / 1024) / (end_time - start_time)
    
    print(f"{retransmissions} {throughput:.2f}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 Sender2.py <RemoteHost> <Port> <Filename> <RetryTimeout>")
        sys.exit(1)

    remote_host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
    retry_timeout = int(sys.argv[4])

    send_file(remote_host, port, filename, retry_timeout)