# Reliable Data Transfer over UDP

This repository contains the implementation and evaluation of **end-to-end reliable data transfer protocols** at the application layer over UDP.

The goal of this coursework is to understand how reliable communication can be achieved over an unreliable transport protocol by implementing classic sliding window protocols and evaluating their performance under different network conditions.

---

## 📚 Implemented Protocols

The following protocols are implemented in Python using UDP sockets:

1. **Part 1 – Basic File Transfer**
   - Unreliable UDP-based file transfer
   - No retransmissions, no acknowledgements
   - Used as a baseline under ideal network conditions

2. **Part 2 – Stop-and-Wait (rdt3.0)**
   - Reliable data transfer using acknowledgements and timeouts
   - Duplicate detection using sequence numbers
   - Performance evaluation under packet loss

3. **Part 3 – Go-Back-N**
   - Sliding window protocol with configurable window size
   - Cumulative acknowledgements
   - Throughput evaluation under varying delay and window sizes

4. **Part 4 – Selective Repeat**
   - Sliding window protocol with per-packet acknowledgements
   - Out-of-order packet buffering at the receiver
   - Performance comparison with TCP (using iperf)
