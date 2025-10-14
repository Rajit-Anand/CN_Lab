#!/usr/bin/env python3
"""
Go-Back-N ARQ Simulation
Usage:
    python go_back_n.py --frames 20 --win 4 --loss 0.2 --seed 123
"""
import argparse, random

def simulate(total_frames=20, window_size=4, loss_prob=0.2, rng=None):
    if rng is None:
        rng = random.Random()
    base = 0                # oldest unacknowledged frame
    next_seq = 0            # next frame to send
    logs = []
    while base < total_frames:
        # Send frames in window
        send_upto = min(base + window_size, total_frames)
        if next_seq < send_upto:
            frames_to_send = list(range(next_seq, send_upto))
            logs.append(f"Sending frames {frames_to_send[0]} {frames_to_send[-1]}")
            next_seq = send_upto

        # Determine the fate of each outstanding frame
        lost_index = None
        for f in range(base, next_seq):
            # If already ACKed (by prior iteration), skip
            if f < base:
                continue
            # First loss in the window
            if lost_index is None and rng.random() < loss_prob:
                lost_index = f
                break

        if lost_index is not None:
            # Retransmit from lost_index to next_seq-1
            logs.append(f"Frame {lost_index} lost , retransmitting frames {lost_index} {next_seq-1}")
            # Go-back-N: move next_seq back to lost_index
            next_seq = lost_index
            continue
        else:
            # Cumulative ACK up to next_seq - 1
            ack_frame = next_seq - 1
            logs.append(f"ACK {ack_frame} received")
            base = next_seq
            if base < total_frames:
                logs.append(f"Window slides to {base} {min(base + window_size - 1, total_frames - 1)}")
    return logs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=20)
    ap.add_argument("--win", type=int, default=4)
    ap.add_argument("--loss", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=123)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    logs = simulate(args.frames, args.win, args.loss, rng)
    for line in logs:
        print(line)

if __name__ == "__main__":
    main()
