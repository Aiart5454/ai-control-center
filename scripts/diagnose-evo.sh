#!/usr/bin/env bash
set -u

section() {
  printf '\n===== %s =====\n' "$1"
}

section "HOST"
hostnamectl 2>/dev/null || true
uname -a

section "MEMORY"
free -h 2>/dev/null || true

section "NETWORK"
ip -brief -4 address 2>/dev/null || true
if command -v tailscale >/dev/null 2>&1; then
  printf '\nTailscale IPv4:\n'
  tailscale ip -4 2>/dev/null || true
else
  echo "tailscale: command not found"
fi

section "SYSTEM SERVICES (AI-related)"
systemctl list-units --type=service --all --no-pager --no-legend 2>/dev/null \
  | grep -Ei 'llama|hermes|open.?webui|comfy|ollama|ai.?control|code' || true

section "USER SERVICES (AI-related)"
systemctl --user list-units --type=service --all --no-pager --no-legend 2>/dev/null \
  | grep -Ei 'llama|hermes|open.?webui|comfy|ollama|ai.?control|code' || true

section "AI PROCESSES (names only)"
ps -eo pid=,comm= 2>/dev/null \
  | grep -Ei 'llama|hermes|open.?webui|comfy|ollama|python|uvicorn' || true

section "TEMPERATURE SENSORS"
if command -v sensors >/dev/null 2>&1; then
  sensors 2>/dev/null || true
else
  echo "sensors: command not found (not an error)"
fi

section "DRM GPU METRICS"
for card in /sys/class/drm/card[0-9]*; do
  [ -d "$card/device" ] || continue
  echo "-- $(basename "$card") --"
  for f in gpu_busy_percent mem_info_vram_used mem_info_vram_total; do
    if [ -r "$card/device/$f" ]; then
      printf '%s=' "$f"
      cat "$card/device/$f"
    fi
  done
done

section "LLAMA API"
if command -v curl >/dev/null 2>&1; then
  curl --max-time 2 -fsS http://127.0.0.1:8080/v1/models 2>/dev/null \
    | head -c 1200 || echo "llama API unavailable on 127.0.0.1:8080"
  echo
fi

section "DONE"
echo "Read-only diagnostics completed. No services were changed."
