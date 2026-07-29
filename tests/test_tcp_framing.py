import socket
import time


def _wait_for_log(rtnode, pattern: str, since: float, timeout: float = 5.0) -> str | None:
    deadline = time.monotonic() + timeout
    pattern = pattern.lower()
    while time.monotonic() < deadline:
        for line, timestamp in rtnode.log_lines:
            if timestamp >= since and pattern in line.lower():
                return line
        time.sleep(0.02)
    return None


def test_tcp_server_detects_hdlc_and_kiss_per_client(rtnode, rtnode_tcp_endpoint):
    host, port = rtnode_tcp_endpoint
    assert _wait_for_log(rtnode, f"Server listening on port {port}", 0, timeout=15.0), (
        "RTNode TCP server did not become ready"
    )

    for delimiter, expected in ((b"\x7e", "framing: HDLC"), (b"\xc0", "framing: KISS")):
        with socket.create_connection((host, port), timeout=5.0) as client:
            started = time.time()
            client.sendall(delimiter)
            assert _wait_for_log(rtnode, expected, started), (
                f"RTNode did not detect {expected} from first delimiter"
            )