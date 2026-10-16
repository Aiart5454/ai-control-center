import os
import socket
import time

import psutil

from .models import DiskInfo, MemoryInfo, SystemInfo


_BOOT_TIME = psutil.boot_time()


def get_system_info() -> SystemInfo:
    vm = psutil.virtual_memory()

    disks: list[DiskInfo] = []
    seen: set[str] = set()
    for part in psutil.disk_partitions(all=False):
        if part.mountpoint in seen:
            continue
        seen.add(part.mountpoint)
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        disks.append(
            DiskInfo(
                mountpoint=part.mountpoint,
                total_bytes=usage.total,
                used_bytes=usage.used,
                free_bytes=usage.free,
                percent=usage.percent,
            )
        )

    return SystemInfo(
        hostname=socket.gethostname(),
        uptime_seconds=max(0.0, time.time() - _BOOT_TIME),
        cpu_percent=psutil.cpu_percent(interval=0.1),
        memory=MemoryInfo(
            total_bytes=vm.total,
            used_bytes=vm.used,
            available_bytes=vm.available,
            percent=vm.percent,
        ),
        disks=disks,
    )
