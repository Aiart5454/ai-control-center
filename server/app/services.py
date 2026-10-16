import subprocess

from .models import ServiceState


SERVICE_ALLOWLIST: dict[str, tuple[str, str]] = {
    "llama": ("llama-server.service", "llama.cpp"),
    "hermes": ("hermes.service", "Hermes"),
    "open_webui": ("open-webui.service", "Open WebUI"),
    "comfyui": ("comfyui.service", "ComfyUI"),
}


def _systemctl_is_active(unit: str) -> str:
    try:
        result = subprocess.run(
            ["systemctl", "is-active", unit],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"

    value = result.stdout.strip()
    if value == "active":
        return "running"
    if value in {"inactive", "deactivating"}:
        return "stopped"
    if value == "failed":
        return "failed"
    return "unknown"


def list_services() -> list[ServiceState]:
    return [
        ServiceState(id=service_id, display_name=display_name, state=_systemctl_is_active(unit))
        for service_id, (unit, display_name) in SERVICE_ALLOWLIST.items()
    ]
