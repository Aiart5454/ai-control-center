import ipaddress
from pathlib import Path
import socket
import time

import psutil

from .models import (
    DiskInfo,
    GpuInfo,
    MemoryInfo,
    NetworkInfo,
    SystemInfo,
    TemperatureSensor,
)


_BOOT_TIME = psutil.boot_time()


def _read_int(path: Path) -> int | None:
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def _network_info() -> NetworkInfo:
    local_ipv4: set[str] = set()
    tailscale_ipv4: set[str] = set()

    for interface, addresses in psutil.net_if_addrs().items():
        for address in addresses:
            if address.family != socket.AF_INET:
                continue
            try:
                ip = ipaddress.ip_address(address.address)
            except ValueError:
                continue
            if ip.is_loopback or ip.is_link_local:
                continue
            if interface.lower().startswith("tailscale"):
                tailscale_ipv4.add(str(ip))
            elif ip.is_private:
                local_ipv4.add(str(ip))

    # External IP deliberately stays unavailable in the read-only/offline MVP.
    # It requires an explicit outbound request to a trusted service.
    return NetworkInfo(
        local_ipv4=sorted(local_ipv4),
        tailscale_ipv4=sorted(tailscale_ipv4),
        external_ip=None,
    )


def _temperatures() -> list[TemperatureSensor]:
    result: list[TemperatureSensor] = []
    try:
        groups = psutil.sensors_temperatures(fahrenheit=False)
    except (AttributeError, OSError):
        return result

    for group_name, entries in sorted(groups.items()):
        for index, entry in enumerate(entries):
            label = entry.label.strip() if entry.label else f"{group_name}:{index}"
            result.append(
                TemperatureSensor(
                    label=label,
                    current_c=float(entry.current),
                    high_c=float(entry.high) if entry.high is not None else None,
                    critical_c=float(entry.critical) if entry.critical is not None else None,
                )
            )
    return result


def _gpus() -> list[GpuInfo]:
    result: list[GpuInfo] = []
    drm_root = Path("/sys/class/drm")
    if not drm_root.exists():
        return result

    for card in sorted(drm_root.glob("card[0-9]*")):
        device = card / "device"
        if not device.exists():
            continue

        busy = _read_int(device / "gpu_busy_percent")
        vram_used = _read_int(device / "mem_info_vram_used")
        vram_total = _read_int(device / "mem_info_vram_total")

        # Ignore display devices that expose none of the metrics we can read safely.
        if busy is None and vram_used is None and vram_total is None:
            continue

        result.append(
            GpuInfo(
                id=card.name,
                busy_percent=float(busy) if busy is not None else None,
                vram_used_bytes=vram_used,
                vram_total_bytes=vram_total,
            )
        )
    return result


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
        temperatures=_temperatures(),
        network=_network_info(),
        gpus=_gpus(),
    )
