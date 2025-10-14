# Task 2: Go-Back-N ARQ (Corrected)

Run:
```bash
python go_back_n.py --frames 20 --win 4 --loss 0.2 --seed 7 > go_back_n_output.txt
```
Notes:
- Cumulative ACKs before the first loss each round.
- After a partial ACK, window is topped up, so retransmission may span a larger range (e.g., 2–5).
Generated: 2025-10-14T09:15:56.720378Z
