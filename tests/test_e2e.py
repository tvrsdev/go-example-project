import subprocess
import time
import requests
import signal
import os
import pytest

SERVER_CMD = ["make", "run"]
SERVER_URL = "http://127.0.0.1:8080"
START_TIMEOUT = 15.0  

def start_server():
    env = os.environ.copy()
    env["GIN_MODE"] = "release"           # optional: quieter logs for Gin
    proc = subprocess.Popen(SERVER_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return proc

def wait_for_server(url, timeout=START_TIMEOUT):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, params={"x": 1}, timeout=1)
            # Accept 200 as ready
            if r.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(0.2)
    return False

def normalize_map_keys_to_int(d):
    return {int(k): v for k, v in d.items()}

def normalize_list_of_maps(arr):
    return [{int(k): v for k, v in m.items()} for m in arr]

@pytest.fixture(scope="session")
def server():
    proc = start_server()
    try:
        ok = wait_for_server(SERVER_URL + "/correct")
        if not ok:
            # try to capture logs to help debugging
            try:
                out, err = proc.communicate(timeout=1)
            except Exception:
                proc.kill()
                out, err = proc.communicate(timeout=1)
            raise RuntimeError(f"server did not start within timeout.\nstdout:\n{out.decode(errors='ignore')}\nstderr:\n{err.decode(errors='ignore')}")
        yield SERVER_URL
    finally:
        # terminate gracefully then force kill if necessary
        try:
            proc.send_signal(signal.SIGINT)
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
            proc.wait(timeout=3)

# --- test cases (extendable) ---
CORRECT_CASES = [
    (1, {250: 1}),
    (250, {250: 1}),
    (500, {500: 1}),
    (750, {500: 1, 250: 1}),
    (1000, {1000: 1}),
    (12001, {5000: 2, 2000: 1, 250: 1}),
    (4999, {2000: 2, 1000: 1}),
    (5001, {5000: 1, 250: 1}),
]

INCORRECT_CASES = [
    (1, [{5000: 1}, {2000: 1}, {1000: 1}, {500: 1}]),
    (251, [{5000: 1}, {2000: 1}, {1000: 1}, {250: 2}]),
    (501, [{5000: 1}, {2000: 1}, {1000: 1}, {500: 2}, {250: 3}]),
    (12001, [{5000: 3}, {2000: 7}, {1000: 13}, {500: 25}, {250: 49}]),
]

def test_correct_endpoint(server):
    for ordered, want in CORRECT_CASES:
        resp = requests.get(f"{server}/correct", params={"x": ordered}, timeout=10)
        assert resp.status_code == 200, f"status {resp.status_code}, body: {resp.text}"
        data = resp.json()
        packs = data["data"]["packs"]
        got = normalize_map_keys_to_int(packs)
        assert got == want, f"/correct?x={ordered} => {got}, want {want}"

def test_incorrect_endpoint(server):
    for ordered, want_list in INCORRECT_CASES:
        resp = requests.get(f"{server}/incorrect", params={"x": ordered}, timeout=10)
        assert resp.status_code == 200, f"status {resp.status_code}, body: {resp.text}"
        data = resp.json()
        packs = data["data"]["packs"]
        got = normalize_list_of_maps(packs)
        assert got == want_list, f"/incorrect?x={ordered} => {got}, want {want_list}"

def test_validation_errors(server):
    # missing x
    r = requests.get(f"{server}/correct", timeout=3)
    assert r.status_code == 400

    # non-integer
    r = requests.get(f"{server}/correct", params={"x": "abc"}, timeout=3)
    assert r.status_code == 400

    # negative
    r = requests.get(f"{server}/correct", params={"x": -1}, timeout=3)
    assert r.status_code == 400
