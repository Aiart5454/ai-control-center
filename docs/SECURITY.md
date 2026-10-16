# Security model

## Trust boundary

The Ubuntu service is trusted. The phone is an authenticated remote client. LLM output is never treated as executable control input.

## MVP rules

- bind to loopback by default;
- remote access via Tailscale;
- bearer token authentication before write endpoints are enabled;
- rate-limit state-changing requests;
- no arbitrary command execution;
- service names are server-defined IDs, never raw systemd unit names from clients;
- audit every requested mode/service transition;
- do not return environment variables, secrets or full process command lines by default.

## Later hardening

- short-lived device tokens;
- TLS/Tailscale HTTPS;
- per-device revocation;
- request signing/replay protection;
- Android secure credential storage;
- optional biometric gate for destructive actions.
