import json
import subprocess
from urllib.error import URLError
from urllib.request import urlopen

from .models import ModelRuntime, ServiceState


SERVICE_ALLOWLIST: dict[str, tuple[str, str, str]] = {
    "llama": ("system", "llama-server.service", "llama.cpp"),
    "hermes": ("user", "hermes-gateway.service", "Hermes Gateway"),
    "open_webui": ("system", "open-webui.service", "Open WebUI"),
    "comfyui": ("system", "comfyui.service", "ComfyUI"),
}


def _systemctl_is_active(scope: str, unit: str) -> str:
    command = ["systemctl"]
    if scope == "user":
        command.append("--user")
    command.extend(["is-active", unit])

    try:
        result = subprocess.run(
            command,
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
    if value in {"unknown", "not-found"}:
        return "unavailable"
    return "unknown"


def list_services() -> list[ServiceState]:
    return [
        ServiceState(
            id=service_id,
            display_name=display_name,
            scope=scope,
            unit=unit,
            state=_systemctl_is_active(scope, unit),
        )
        for service_id, (scope, unit, display_name) in SERVICE_ALLOWLIST.items()
    ]


def list_models() -> list[ModelRuntime]:
    try:
        with urlopen("http://127.0.0.1:8080/v1/models", timeout=2) as response:
            payload = json.load(response)
    except (OSError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return []

    result: list[ModelRuntime] = []
    for item in payload.get("data", []):
        status = item.get("status") or {}
        result.append(
            ModelRuntime(
                id=str(item.get("id", "unknown")),
                state=str(status.get("value", "unknown")),
                context_length=item.get("context_length"),
            )
        )
    return result
