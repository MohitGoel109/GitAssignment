import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest

from app.server import Handler


@pytest.fixture(scope="module")
def base_url():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:%d" % server.server_port
    server.shutdown()


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_health_endpoint(base_url):
    status, body = get(base_url + "/health")
    assert status == 200
    assert body == {"status": "ok"}


def test_total_endpoint_applies_discount(base_url):
    status, body = get(base_url + "/total?price=50&qty=2&discount=10")
    assert status == 200
    assert body["total"] == 90.0


def test_total_endpoint_rejects_bad_input(base_url):
    status, _ = get(base_url + "/total?price=abc&qty=2")
    assert status == 400


def test_unknown_route_returns_404(base_url):
    status, _ = get(base_url + "/nope")
    assert status == 404
