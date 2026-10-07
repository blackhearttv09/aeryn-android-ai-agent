#!/usr/bin/env bash
set -euo pipefail

# This script is intended to be invoked by Termux:Boot after device boot.
# It should start the Android companion service or reconnect the Python runtime.

mkdir -p "$HOME/.aeryn"
log_file="$HOME/.aeryn/aeryn-boot.log"

(
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Aeryn boot sequence started"
  cd "$HOME" || exit 1
  if [ -d "$HOME/aeryn-android-ai-agent" ]; then
    cd "$HOME/aeryn-android-ai-agent"
    if [ -f scripts/start_aeryn.sh ]; then
      bash scripts/start_aeryn.sh
    fi
  fi
) >> "$log_file" 2>&1
