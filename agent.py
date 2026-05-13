#!/usr/bin/env python3
"""Pulse agent: collect system metrics and report (console for now)."""

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

PULSE_URL = "http://localhost:8080/ingest"
PULSE_INTERVAL = 2.0
PULSE_USER = getpass.getuser()


@dataclass
class NetSample:
    bytes_sent: int
    bytes_recv: int


def disk_usage_root() -> str:
    """Root path for psutil.disk_usage: drive on Windows, / on Unix."""
    if sys.platform == "win32":
        return os.environ.get("SystemDrive", "C:") + os.sep
    return "/"


def collect_metrics(
    prev_net: NetSample | None,
) -> tuple[dict[str, float], NetSample]:
    """Collect metrics; net_*_mb are megabytes since the previous sample."""
    vm = psutil.virtual_memory()
    du = psutil.disk_usage(disk_usage_root())
    net = psutil.net_io_counters()

    cur = NetSample(bytes_sent=int(net.bytes_sent), bytes_recv=int(net.bytes_recv))

    if prev_net is None:
        sent_mb = 0.0
        recv_mb = 0.0
    else:
        ds = max(0, cur.bytes_sent - prev_net.bytes_sent)
        dr = max(0, cur.bytes_recv - prev_net.bytes_recv)
        sent_mb = ds / (1024 * 1024)
        recv_mb = dr / (1024 * 1024)

    metrics: dict[str, float] = {
        "cpu_percent": float(psutil.cpu_percent(interval=None)),
        "memory_percent": float(vm.percent),
        "memory_used_mb": float(vm.used) / (1024 * 1024),
        "disk_percent": float(du.percent),
        "net_sent_mb": sent_mb,
        "net_recv_mb": recv_mb,
    }
    return metrics, cur


def build_payload(
    hostname: str,
    username: str,
    metrics: dict[str, float],
) -> dict[str, Any]:
    ts_ms = int(time.time() * 1000)
    return {
        "appName": hostname,
        "username": username,
        "metrics": dict(metrics),
        "timestamp": ts_ms,
    }


def transmit(server_url: str, payload: dict[str, Any]) -> tuple[str, float]:
    """Send metrics to the server. Currently a no-op timing stub."""
    start = time.perf_counter()
    # Future: requests.post(server_url, json=payload, timeout=10)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return "OK (console)", elapsed_ms


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log = logging.getLogger("pulse")

    hostname = socket.gethostname()
    server_url = PULSE_URL
    interval = PULSE_INTERVAL
    username = PULSE_USER

    log.info(
        "started host=%s user=%s url=%s interval=%ss",
        hostname,
        username,
        server_url,
        interval,
    )

    prev_net: NetSample | None = None
    psutil.cpu_percent(interval=None)

    try:
        while True:
            metrics, prev_net = collect_metrics(prev_net)
            payload = build_payload(hostname, username, metrics)
            status, elapsed_ms = transmit(server_url, payload)

            log.info(
                "report %s %.2fms | cpu=%.1f%% mem=%.1f%% mem_used=%.0fMB "
                "disk=%.1f%% net_sent=%.2fMB net_recv=%.2fMB",
                status,
                elapsed_ms,
                metrics["cpu_percent"],
                metrics["memory_percent"],
                metrics["memory_used_mb"],
                metrics["disk_percent"],
                metrics["net_sent_mb"],
                metrics["net_recv_mb"],
            )
            time.sleep(interval)
    except KeyboardInterrupt:
        log.info("stopped")


if __name__ == "__main__":
    main()
