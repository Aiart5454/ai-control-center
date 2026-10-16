from typing import Literal

from pydantic import BaseModel


Mode = Literal["idle", "agent", "chat", "code", "media"]


class HealthResponse(BaseModel):
    ok: bool
    version: str


class MemoryInfo(BaseModel):
    total_bytes: int
    used_bytes: int
    available_bytes: int
    percent: float


class DiskInfo(BaseModel):
    mountpoint: str
    total_bytes: int
    used_bytes: int
    free_bytes: int
    percent: float


class SystemInfo(BaseModel):
    hostname: str
    uptime_seconds: float
    cpu_percent: float
    memory: MemoryInfo
    disks: list[DiskInfo]


class ServiceState(BaseModel):
    id: str
    display_name: str
    state: Literal["running", "stopped", "failed", "unknown", "unavailable"]


class StatusResponse(BaseModel):
    mode: Mode
    system: SystemInfo
    services: list[ServiceState]
