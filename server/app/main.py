from fastapi import FastAPI

from .models import HealthResponse, StatusResponse, SystemInfo
from .services import list_models, list_services
from .telemetry import get_system_info

app = FastAPI(
    title="AI Control Center",
    version="0.3.0",
    docs_url="/docs",
    redoc_url=None,
)


@app.get("/api/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(ok=True, version="0.3.0")


@app.get("/api/v1/system", response_model=SystemInfo)
def system_info() -> SystemInfo:
    return get_system_info()


@app.get("/api/v1/status", response_model=StatusResponse)
def status() -> StatusResponse:
    services = list_services()
    models = list_models()

    hermes_running = any(item.id == "hermes" and item.state == "running" for item in services)
    loaded_models = [item for item in models if item.state == "loaded"]
    mode = "agent" if hermes_running and loaded_models else "idle"

    return StatusResponse(
        mode=mode,
        system=get_system_info(),
        services=services,
        models=models,
    )
