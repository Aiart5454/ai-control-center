# Architecture

## Components

### Ubuntu Control API
FastAPI service that exposes versioned endpoints. It owns the control policy and is the only component allowed to request service transitions.

### Android client
Kotlin + Jetpack Compose application. It displays telemetry and sends typed mode/service requests.

### Transport
Tailscale is the intended remote network. The API must not be exposed directly to the public Internet in the MVP.

## Modes

- `idle`: stop heavy AI workloads
- `agent`: Hermes + agent LLM
- `chat`: Open WebUI + chat LLM
- `code`: coding model/UI
- `media`: ComfyUI/image/video stack

Mode transitions are server-side workflows. The Android app does not decide which low-level processes to kill.

## API sketch

- `GET /api/v1/health`
- `GET /api/v1/status`
- `GET /api/v1/system`
- `GET /api/v1/services`
- `POST /api/v1/mode/{mode}`
- `POST /api/v1/services/{service}/start`
- `POST /api/v1/services/{service}/stop`
- `POST /api/v1/services/{service}/restart`

System-changing endpoints are not enabled until authentication and an explicit service allowlist are configured.
