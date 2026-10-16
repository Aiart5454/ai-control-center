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
- `http://127.0.0.1:9000/api/v1/status`
- `http://127.0.0.1:9000/docs`

## Important

This code does not start/stop services yet. It only reads status. Write/control endpoints will be added after authentication + explicit service mapping are implemented.
