#!/usr/bin/env python3
"""
Go-Back-N ARQ Simulation (Corrected)
- Logs batch sends, cumulative ACKs, first loss, retransmit range, and window slide.
- Can produce sequences like:
  Sending frames 0 3
  ACK 1 received
  Frame 2 lost , retransmitting frames 2 5
  ACK 5 received
  Window slides to 6 9
Usage:
  python go_back_n.py --frames 20 --win 4 --loss 0.2 --seed 7
"""
import argparse, random

def go_back_n(total_frames=20, window_size=4, loss_prob=0.2, rng=None):
    if rng is None:
        rng = random.Random()
    base = 0          # oldest unACKed
    next_seq = 0      # next seq num to send
    logs = []

    def log_send(a,b):
        logs.append(f"Sending frames {a} {b}")

    while base < total_frames:
        # 1) Fill window: send a burst
        send_to = min(base + window_size, total_frames)
        if next_seq < send_to:
            a, b = next_seq, send_to - 1
            log_send(a, b)
            next_seq = send_to

        # Outstanding frames are [base, next_seq-1]
        if base >= next_seq:
            continue

        # 2) Determine earliest loss among outstanding; everything before it ACKs cumulatively
        earliest_loss = None
        for f in range(base, next_seq):
            if rng.random() < loss_prob:
                earliest_loss = f
                break

        if earliest_loss is None:
            # All delivered: cumulative ACK to next_seq-1
            ack_to = next_seq - 1
            logs.append(f"ACK {ack_to} received")
            base = next_seq
            if base < total_frames:
                right = min(base + window_size - 1, total_frames - 1)
                logs.append(f"Window slides to {base} {right}")
            continue

        # Some loss occurred at 'earliest_loss'
        # If anything before loss arrived, we get a cumulative ACK to earliest_loss-1
        if earliest_loss > base:
            logs.append(f"ACK {earliest_loss-1} received")
            base = earliest_loss

            # After partial ACK, try to top-up the window (this can advance next_seq further),
            # which is why retransmit range may extend beyond the original send burst.
            send_to = min(base + window_size, total_frames)
            if next_seq < send_to:
                a2, b2 = next_seq, send_to - 1
                log_send(a2, b2)
                next_seq = send_to

        # Retransmit from the lost frame through the end of the outstanding queue
        logs.append(f"Frame {base} lost , retransmitting frames {base} {next_seq-1}")
        # Sender goes back to 'base' for retransmission
        next_seq = base

        # On the *next* loop iteration, the re-sent burst will be handled.
    return logs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=20)
    ap.add_argument("--win", type=int, default=4)
    ap.add_argument("--loss", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    logs = go_back_n(args.frames, args.win, args.loss, rng)
    for line in logs:
        print(line)

if __name__ == "__main__":
    main()
