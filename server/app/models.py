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


class TemperatureSensor(BaseModel):
    label: str
    current_c: float
    high_c: float | None = None
    critical_c: float | None = None


class NetworkInfo(BaseModel):
    local_ipv4: list[str]
    tailscale_ipv4: list[str]
    external_ip: str | None = None


class GpuInfo(BaseModel):
    id: str
    busy_percent: float | None = None
    vram_used_bytes: int | None = None
    vram_total_bytes: int | None = None


class ModelRuntime(BaseModel):
    id: str
    state: str
    context_length: int | None = None


class SystemInfo(BaseModel):
    hostname: str
    uptime_seconds: float
    cpu_percent: float
    memory: MemoryInfo
    disks: list[DiskInfo]
    temperatures: list[TemperatureSensor]
    network: NetworkInfo
    gpus: list[GpuInfo]


class ServiceState(BaseModel):
    id: str
    display_name: str
    scope: Literal["system", "user"]
    unit: str
    state: Literal["running", "stopped", "failed", "unknown", "unavailable"]


class StatusResponse(BaseModel):
    mode: Mode
    system: SystemInfo
    services: list[ServiceState]
    models: list[ModelRuntime]
