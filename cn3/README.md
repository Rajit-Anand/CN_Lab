# CN Lab Assignment 3 — HTTP Caching & Cookies (Python)

This repo contains two independent demos:

- **part1_http_cache/** — an HTTP server using `http.server` that implements **ETag** and **Last‑Modified** with conditional requests (`If-None-Match`, `If-Modified-Since`).
- **part2_cookie_raw_sockets/** — a minimal HTTP server built on **raw TCP sockets** that demonstrates **cookie** issuance and recognition across requests.

> Based on the assignment brief in the provided PDF.

## Quickstart

### Part 1 — Caching server
```bash
cd part1_http_cache
python3 server.py
# open http://127.0.0.1:8080 in your browser
```
- First load returns **200 OK** with `ETag` and `Last-Modified`.
- Subsequent refreshes return **304 Not Modified** (no body) until you edit `index.html`.

### Part 2 — Cookie server (raw sockets)
```bash
cd part2_cookie_raw_sockets
python3 cookie_server.py
# open http://127.0.0.1:9090 in your browser
```
- First visit sets `Set-Cookie: session_id=...` and shows a welcome message.
- Refresh or revisit sends `Cookie: session_id=...` and you’ll see “Welcome back!”.

## Files
```
part1_http_cache/
  ├── server.py
  └── index.html
part2_cookie_raw_sockets/
  └── cookie_server.py
```

## Notes
- No third‑party deps required (only Python 3.8+ standard library).
- The caching demo uses MD5 purely as a fast content hash for ETag (acceptable for this learning use‑case).
- The cookie demo is intentionally simple and **not** production grade.
