# AI Control Center

Удалённое управление локальным AI-сервером: Ubuntu control service + Android-клиент.

## Цель MVP

- показывать CPU, RAM, диски, uptime и сетевые адреса;
- показывать состояние разрешённых AI-сервисов;
- переключать режимы: `agent`, `chat`, `code`, `media`, `idle`;
- работать через Tailscale;
- не давать телефону произвольный shell/root-доступ;
- все управляющие действия выполнять только через allowlist на Ubuntu.

## Архитектура

```text
Android app
    |
    | HTTPS/Tailscale
    v
AI Control API (Ubuntu)
    |
    +-- telemetry
    +-- service status
    +-- mode controller
    +-- audit log
    |
    +-- systemd allowlist
        +-- llama-server
        +-- hermes
        +-- open-webui
        +-- comfyui
        +-- code-server/model service
```

## Репозиторий

- `server/` — Ubuntu Control API (FastAPI)
- `android/` — Android-клиент (Kotlin + Jetpack Compose)
- `docs/` — архитектура, безопасность и контракт API

## Безопасность

Сервер по умолчанию слушает только `127.0.0.1`. Для удалённого доступа предполагается Tailscale. Управление сервисами будет ограничено фиксированным allowlist. Произвольные shell-команды через API не поддерживаются.

## Статус

Начат MVP. Реальная интеграция с systemd/AMD-метриками должна проверяться на целевой Ubuntu-машине отдельно; репозиторий не заявляет такие проверки до фактического запуска.
