# Aeryn — Universal Autonomous Android Voice AI Agent

Aeryn is an Android-first autonomous agent that can operate a device using a valid, user-granted permission model. It is designed to be a generic screen-control AI system rather than a hardcoded app automation bot.

## Goals

- Voice-first interaction using Gemini for natural conversation.
- Fast planning and task decomposition using Groq.
- Real-time screen observation and UI understanding.
- Virtual mouse / pointer control for generic device interaction.
- Secure local memory using SQLite.
- Recovery-aware execution loop to handle failures and retries.
- Reboot-safe initialization using Termux:Boot and Android foreground service.
- Confirmation gates for sensitive actions.

## Core architecture

- Termux + Python Aeryn Core
- Native Android companion service
- Accessibility Service for UI introspection and controls
- MediaProjection for generic screen capture / inspection
- Virtual Mouse Engine for pointer and input actions
- Gemini + Groq orchestration
- SQLite local memory

## Execution loop

SEE → UNDERSTAND → PLAN → CONTROL → VERIFY → RECOVER

## Security model

- API keys stored in environment variables / secure config only.
- No hardcoded secrets.
- Sensitive operations require explicit confirmation.
- No attempt to bypass Android sandbox or user permission boundaries.
- All control is limited to user-granted permissions and visible system access.

## Repository structure

- `aeryn_core/` — Python runtime, planning, agent orchestration, memory, config
- `android/` — Android app scaffold for companion service and accessibility integration
- `scripts/` — Termux boot and startup scripts
- `docs/` — architecture and implementation notes

## Quick start

1. Copy `.env.example` to `.env` and fill in API keys.
2. Install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the agent core:

   ```bash
   python main.py
   ```

## Sensitive actions policy

Aeryn must confirm before performing irreversible or risky actions, including:

- payment or financial action
- direct message or call sending
- account/security changes
- destructive file operations
- app uninstall or system-level modification

## Production direction

This repo is structured as a modular foundation for later conversion into a full Android APK or packaged app. It is intentionally split into clear domains so each layer can evolve independently.

## License

MIT
