from fastapi import FastAPI

from .models import HealthResponse, StatusResponse
from .services import list_services
from .telemetry import get_system_info

app = FastAPI(
    title="AI Control Center",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)


@app.get("/api/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(ok=True, version="0.1.0")


@app.get("/api/v1/status", response_model=StatusResponse)
def status() -> StatusResponse:
    # Until the mode controller is enabled, report idle rather than pretending
    # that a specific workload is active.
    return StatusResponse(
        mode="idle",
        system=get_system_info(),
        services=list_services(),
    )
