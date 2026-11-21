import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from app.shop import calculate_total


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/health":
            return self._send(200, {"status": "ok"})
        if url.path == "/total":
            q = parse_qs(url.query)
            try:
                items = [{"price": float(q["price"][0]), "qty": int(q["qty"][0])}]
                discount = float(q.get("discount", ["0"])[0])
                return self._send(200, {"total": calculate_total(items, discount)})
            except (KeyError, ValueError):
                return self._send(400, {"error": "invalid input"})
        return self._send(404, {"error": "not found"})

    def log_message(self, *args):
        pass


def run(port=8000):
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    run()
