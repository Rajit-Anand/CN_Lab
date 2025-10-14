#!/usr/bin/env python3
"""
Stop-and-Wait ARQ Simulation
Usage:
    python stop_and_wait.py --frames 10 --loss 0.2 --timeout 2.0 --seed 42
"""
import argparse, random, time

def simulate(frames=10, loss_prob=0.2, timeout=2.0, rng=None):
    if rng is None:
        rng = random.Random()
    logs = []
    for frame in range(frames):
        sent = False
        attempts = 0
        while not sent:
            attempts += 1
            logs.append(f"Sending Frame {frame}")
            # Frame lost?
            if rng.random() < loss_prob:
                logs.append(f"Frame {frame} lost , retransmitting ...")
                # emulate waiting for timeout (no actual sleep to keep run fast)
                continue
            # ACK lost?
            if rng.random() < loss_prob:
                logs.append(f"ACK {frame} lost , retransmitting ...")
                continue
            logs.append(f"ACK {frame} received")
            sent = True
    return logs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=10)
    ap.add_argument("--loss", type=float, default=0.2)
    ap.add_argument("--timeout", type=float, default=2.0)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    logs = simulate(args.frames, args.loss, args.timeout, rng)
    for line in logs:
        print(line)

if __name__ == "__main__":
    main()
