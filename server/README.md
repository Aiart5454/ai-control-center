# Ubuntu Control API

The current milestone is intentionally read-only.

## Local development

Do not install dependencies with the system `pip`. Ubuntu protects the system Python via PEP 668.

From the repository root:

```bash
bash scripts/bootstrap-local.sh
bash scripts/run-local.sh
```

The bootstrap creates `server/.venv`, installs dependencies only there, and runs tests.
The run script always invokes uvicorn through that virtual environment, so it cannot accidentally use `/usr/bin/uvicorn`.

If Ubuntu reports that venv support is missing, install it once:

```bash
sudo apt install python3-venv
```

Then rerun `bash scripts/bootstrap-local.sh`.

Open:

- `http://127.0.0.1:9000/api/v1/health`
- `http://127.0.0.1:9000/api/v1/system`
- `http://127.0.0.1:9000/api/v1/status`
- `http://127.0.0.1:9000/docs`

## Telemetry

The API reads:

- CPU load;
- RAM usage;
- mounted disk usage;
- temperature sensors exposed by Linux/psutil;
- local IPv4 and Tailscale IPv4;
- AMD/Linux DRM GPU busy/VRAM counters when exposed in `/sys/class/drm`;
- llama.cpp model registry from `127.0.0.1:8080/v1/models`.

Unavailable hardware fields are returned as empty/null rather than invented values.

`external_ip` is intentionally `null` in this stage because discovering it requires an outbound request to a third-party service. That can be enabled later as an explicit opt-in.

## Verified EVO-X2 mappings

Read-only diagnostics on the target host identified:

- system service: `llama-server.service`
- user service: `hermes-gateway.service`
- llama.cpp API: `http://127.0.0.1:8080/v1/models`

Open WebUI and ComfyUI systemd units have not yet been verified, so their configured IDs remain placeholders and will report unavailable until a real unit is found.

## Important

This code does not start/stop services yet. It only reads status. Write/control endpoints will be added after authentication + explicit service mapping are implemented.
