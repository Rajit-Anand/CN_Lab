#!/usr/bin/env python3
"""
Simple HTTP server that demonstrates caching with ETag and Last-Modified.
- Serves index.html from the current directory.
- Computes ETag as MD5 of the file contents.
- Sends Last-Modified based on file mtime.
- Honors If-None-Match and If-Modified-Since conditional headers.
"""
import http.server
import socketserver
import os
import hashlib
from email.utils import formatdate, parsedate_to_datetime

HOST, PORT = "127.0.0.1", 8080
FILENAME = "index.html"

class CacheHandler(http.server.BaseHTTPRequestHandler):
    server_version = "CN3CacheServer/1.0"

    def do_GET(self):
        # Only serve root or /index.html
        if self.path not in ("/", "/index.html"):
            self.send_error(404, "Not Found")
            return

        if not os.path.exists(FILENAME):
            self.send_error(404, "index.html not found")
            return

        # Read file & compute metadata
        with open(FILENAME, "rb") as f:
            body = f.read()
        etag = hashlib.md5(body).hexdigest()
        mtime = os.path.getmtime(FILENAME)
        last_mod_http = formatdate(timeval=mtime, usegmt=True)

        # Check conditional headers
        inm = self.headers.get("If-None-Match")
        ims = self.headers.get("If-Modified-Since")
        not_modified = False

        if inm and inm.strip('"') == etag:
            not_modified = True
        elif ims:
            try:
                ims_dt = parsedate_to_datetime(ims)
                # If resource not modified since IMS time -> 304
                if mtime <= ims_dt.timestamp():
                    not_modified = True
            except Exception:
                pass

        if not_modified:
            self.send_response(304, "Not Modified")
            self.send_header("ETag", f'"{etag}"')
            self.send_header("Last-Modified", last_mod_http)
            self.send_header("Cache-Control", "max-age=0, must-revalidate")
            self.end_headers()
            return

        # Otherwise send full body
        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("ETag", f'"{etag}"')
        self.send_header("Last-Modified", last_mod_http)
        self.send_header("Cache-Control", "max-age=60, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # cleaner console logs
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), CacheHandler) as httpd:
        print(f"Serving {FILENAME} with caching on http://{HOST}:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
