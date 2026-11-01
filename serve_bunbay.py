import http.server, socket, socketserver, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import glob
_found = sorted(glob.glob(os.path.join(HERE, "BUNBAY*.html")) + glob.glob(os.path.join(HERE, "*.html")))
if not _found:
    print("No HTML file found next to this script. Put the BUNBAY html file in the same folder.")
    input("Press Enter to close.")
    sys.exit(1)
PAGE = _found[0]
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

IP = lan_ip()

class H(http.server.BaseHTTPRequestHandler):
    def _send(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        path = self.path.split("?")[0].split("#")[0]
        if path in ("/", "/index.html"):
            with open(PAGE, "rb") as f:
                self._send(f.read(), "text/html; charset=utf-8")
        elif path == "/lan.json":
            host = self.headers.get("Host", "")
            port = host.rsplit(":", 1)[1] if ":" in host else str(PORT)
            self._send(json.dumps({"url": "http://%s:%s/" % (IP, port)}).encode(), "application/json")
        else:
            self.send_error(404)
    def log_message(self, *a):
        pass

class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

print("BUNBAY Royalty Club is running.")
print("On this computer:  http://localhost:%d/" % PORT)
print("On phones (same Wifi):  http://%s:%d/" % (IP, PORT))
print("Press Ctrl+C to stop.")
try:
    S(("0.0.0.0", PORT), H).serve_forever()
except OSError:
    print("Port %d is busy. Close the other window or run: python serve_bunbay.py 8001" % PORT)
    input("Press Enter to close.")