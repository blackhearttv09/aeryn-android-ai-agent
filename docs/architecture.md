# Aeryn Architecture

This document describes the intended production architecture for Aeryn.

## 1. Runtime layers

### 1.1 Android native layer

- Foreground service for background execution
- Boot-time reinitialization via Termux:Boot
- User-based permission checks
- Lifecycle management and crash recovery

### 1.2 Device control layer

- Accessibility Service for UI tree inspection and interaction
- MediaProjection for screen capture / overlay observation
- Virtual mouse engine for pointer movement and actions
- Android InputManager / accessibility actions

### 1.3 Agent reasoning layer

- Gemini handles voice / natural language interaction
- Groq handles planning, decomposition, and quick reasoning
- Local LLM fallback logic may be added later

### 1.4 Memory and task layer

- SQLite local memory for tasks, context, and user preferences
- Task state machine with timeout / retry / recovery boundaries
- Evidence tracking for executed actions

## 2. Execution loop

The control loop is intentionally strict:

1. SEE
   - Observe screen
   - Detect active app and current focus
   - Extract UI tree or visual hints
2. UNDERSTAND
   - Identify the goal and relevant interface
   - Map UI elements to possible actions
3. PLAN
   - Convert intent into a task graph
   - Split complex tasks into substeps
4. CONTROL
   - Perform virtual input actions
   - Move pointer, tap, drag, scroll, type, navigate
5. VERIFY
   - Check if the expected state is reached
   - Gather evidence from the screen or app state
6. RECOVER
   - On failure, inspect context
   - Choose an alternative action or abort with explanation

## 3. Safety policy

Aeryn is permitted to operate only within:

- user-granted permissions
- visible and accessible UI surfaces
- actions that are consistent with user intent and confirmation rules

Aeryn must refuse or require confirmation for:

- sending messages/calls automatically
- payments and financial transactions
- security or account changes
- destructive file operations
- app uninstall or system modification

## 4. Boot and lifecycle

Aeryn should initialize on device boot using:

- Termux:Boot script
- foreground service restart
- state restoration from SQLite
- user session rehydration

## 5. Data model

- `tasks` table for active and completed tasks
- `events` table for each action and verification outcome
- `memory` table for semantic or user-specific context
- `screenshots` optionally stored for debugging or training

## 6. Extension path

This repo is designed to support:

- native Android companion app
- Python core runtime service
- more advanced computer-vision UI understanding
- voice pipeline improvements
- broader automation domain support

## 7. Caveat

This is a framework and architecture starter. Exact device-level actions depend on Android accessibility APIs, user permissions, and the target apps' compatibility. Aeryn is intended to be generic and safe, not invasive.
