# CN Lab Assignment 4 — UDP Video Streaming (Python)

This submission implements **video streaming over UDP** using Python, OpenCV, and NumPy.

## Features
- Frame JPEG encoding with adjustable quality.
- Packetization with a compact binary header (marker bit for last packet).
- Reassembly on client with out-of-order handling.
- FPS pacing and optional scaling on the server.
- Graceful shutdown with `Ctrl+C` and `q` to quit on client.

## Project Structure
```
cn4-udp-streaming/
├─ server.py          # UDP video server
├─ client.py          # UDP video client
├─ common.py          # Shared header & helpers
├─ requirements.txt   # Python dependencies
└─ README.md          # This guide
```

## Quick Start

### 1) Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Start the client (receiver)
```bash
python client.py --bind 0.0.0.0 --port 5000
```
- Press **q** to quit the client.

### 3) Start the server (sender)
```bash
# Stream a video file (recommended)
python server.py --video sample.mp4 --host 127.0.0.1 --port 5000 --jpeg-quality 70 --scale 1.0

# Or use webcam (device 0) if available
python server.py --video 0 --host 127.0.0.1 --port 5000
```

> Tip: If streaming across machines, set `--host` on the server to the **client's IP** and allow UDP in your firewall.

## Header & Packetization
Each UDP packet uses a **14-byte header**:
- `magic` (2 bytes): `b"VS"`
- `version` (1 byte): `1`
- `flags` (1 byte): bit0 = `marker` (1 for last packet of the frame)
- `frame_id` (uint32)
- `packet_idx` (uint16)
- `total_packets` (uint16)
- `payload_size` (uint16)

This allows the client to reconstruct frames and detect the final packet for a frame.

## Notes / Limitations
- **UDP is unreliable:** packets can be dropped or arrive out of order. This demo **does not** retransmit missing packets.
- If a frame is incomplete, the client will skip it after a timeout and continue.
- Display requires desktop OpenCV; in headless environments use `opencv-python-headless` (no GUI window).

## Tested With
- Python 3.10–3.12
- OpenCV 4.x
- NumPy 1.26+

---

**Author:** UDP Streaming Assignment Implementation
