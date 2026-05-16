#!/usr/bin/env python3
from __future__ import annotations
import getpass
import logging
import os
import socket
import sys
import time
from dataclasses import dataclass
from typing import Any
import psutil

# Change config here
PULSE_URL = "http://localhost:8080/ingest"
PULSE_INTERVAL = 2.0
PULSE_USER = getpass.getuser()

# Represents a piece of network data for a particular time
# This is because psutil.net_io_counters() returns the total amount of bytes since machine booted 
# Always increasing, no reset. So we need to some quick subtraction to get the network sample at that time 
@dataclass
class NetSample:
    bytes_sent: int
    bytes_recv: int

# Grab the correct path for disk usage
def disk_usage_root() -> str:
    if sys.platform == "win32":
        return os.environ.get("SystemDrive", "C:") + os.sep
    return "/"

# Main function to collect metrics -> returns a dict with all the metric details
def collect_metrics(prev_net: NetSample | None) -> tuple[dict[str, float], NetSample]:
    virtual_memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage(disk_usage_root())
    total_net = psutil.net_io_counters()
    current_net = NetSample(bytes_sent=int(total_net.bytes_sent), bytes_recv=int(total_net.bytes_recv))

    # First case running network sample
    if prev_net is None:
        sent_mb = 0.0
        recv_mb = 0.0
    else:
        ds = max(0, current_net.bytes_sent - prev_net.bytes_sent)
        dr = max(0, current_net.bytes_recv - prev_net.bytes_recv)
        sent_mb = ds / (1024 * 1024)
        recv_mb = dr / (1024 * 1024)

    # Assemble metrics into a dictionary
    metrics: dict[str, float] = {
        "cpu_percent": float(psutil.cpu_percent(interval=None)),
        "memory_percent": float(virtual_memory.percent),
        "memory_used_mb": float(virtual_memory.used) / (1024 * 1024),
        "disk_percent": float(disk_usage.percent),
        "net_sent_mb": sent_mb,
        "net_recv_mb": recv_mb,
    }

    # Return the assembled metric, and also the current net sample for next time
    return metrics, current_net

# Returns a simple json based on arguments
def build_payload(hostname: str, username: str, metrics: dict[str, float]) -> dict[str, Any]:
    ts_ms = int(time.time() * 1000)
    return {
        "appName": hostname,
        "username": username,
        "metrics": dict(metrics),
        "timestamp": ts_ms,
    }

# Sends payload to the specified url, and logs how much time it took.
def transmit(server_url: str, payload: dict[str, Any]) -> tuple[str, float]:
    start = time.perf_counter()
    # requests.post(server_url, json=payload, timeout=10)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return "OK (console)", elapsed_ms

# Main driver function
def main() -> None:
    interval_sec = float(PULSE_INTERVAL)

    # Set up logging and create a log object
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log = logging.getLogger("pulse")

    # Initial log message
    hostname = socket.gethostname()
    server_url = PULSE_URL
    username = PULSE_USER
    log.info(
        "LOGGING AS %s@%s, POST TO %s, EVERY %ss", 
        username,
        hostname,
        server_url,
        interval_sec,
    )
    prev_net: NetSample | None = None
    psutil.cpu_percent(interval=None)

    # Driving while loop
    while True:
        metrics, prev_net = collect_metrics(prev_net)
        payload = build_payload(hostname, username, metrics)
        status, elapsed_ms = transmit(server_url, payload)
        # NOT USING STATUS Rn

        # Big log message
        log.info(
            "%s@%s - %.2fms POST | cpu=%.1f%% mem=%.1f%% mem_used=%.0fMB disk=%.1f%% net_sent=%.2fMB net_recv=%.2fMB",
            username,
            hostname,
            elapsed_ms,
            metrics["cpu_percent"],
            metrics["memory_percent"],
            metrics["memory_used_mb"],
            metrics["disk_percent"],
            metrics["net_sent_mb"],
            metrics["net_recv_mb"],
        )
        time.sleep(interval_sec)

if __name__ == "__main__":
    main()