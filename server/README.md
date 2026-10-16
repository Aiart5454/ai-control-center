# Ubuntu Control API

The current milestone is intentionally read-only.

## Local development

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --host 127.0.0.1 --port 9000
```

Then open:

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
- AMD/Linux DRM GPU busy/VRAM counters when exposed in `/sys/class/drm`.

Unavailable hardware fields are returned as empty/null rather than invented values.

`external_ip` is intentionally `null` in this stage because discovering it requires an outbound request to a third-party service. That can be enabled later as an explicit opt-in.

## Important

This code does not start/stop services yet. It only reads status. Write/control endpoints will be added after authentication + explicit service mapping are implemented.
