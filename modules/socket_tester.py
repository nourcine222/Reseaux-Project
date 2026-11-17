"""Single-destination TCP connectivity check."""

import socket
import time
import math


def test_tcp_connection(host: str, port: int, timeout: float = 3.0) -> float:
    """Connect once to a user-specified TCP endpoint and return elapsed seconds.

    Network errors are intentionally allowed to propagate to the caller.
    """
    host = host.strip()
    if not host:
        raise ValueError("Enter a hostname or IP address.")
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535.")
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Timeout must be greater than zero.")

    started = time.perf_counter()
    with socket.create_connection((host, port), timeout=timeout):
        return time.perf_counter() - started
