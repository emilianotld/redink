#!/usr/bin/env bash

set -e

PROJECT_NAME="redink"
CLI_NAME="redink"
MIN_PYTHON_VERSION="3.10"

echo "[*] Installing ${PROJECT_NAME}..."

# --- Check Python ---
if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] Python3 is required but not installed."
  exit 1
fi

PYTHON_VERSION=$(python3 - <<EOF
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
EOF
)

if [[ "$(printf '%s\n' "$MIN_PYTHON_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_PYTHON_VERSION" ]]; then
  echo "[!] Python >= ${MIN_PYTHON_VERSION} is required (found ${PYTHON_VERSION})."
  exit 1
fi

# --- Check pip ---
if ! command -v pip3 >/dev/null 2>&1; then
  echo "[!] pip3 is required but not installed."
  exit 1
fi

# --- Install project ---
echo "[*] Installing Python dependencies..."
pip3 install --user .

# --- Ensure ~/.local/bin is in PATH ---
LOCAL_BIN="$HOME/.local/bin"

if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
  echo "[*] Adding $LOCAL_BIN to PATH..."
  SHELL_RC=""
  if [[ -n "$BASH_VERSION" ]]; then
    SHELL_RC="$HOME/.bashrc"
  elif [[ -n "$ZSH_VERSION" ]]; then
    SHELL_RC="$HOME/.zshrc"
  fi

  if [[ -n "$SHELL_RC" ]]; then
    echo "export PATH=\"\$PATH:$LOCAL_BIN\"" >> "$SHELL_RC"
    echo "[*] PATH updated in $SHELL_RC (restart shell required)."
  else
    echo "[!] Please add $LOCAL_BIN to your PATH manually."
  fi
fi

# --- Verify installation ---
if command -v ${CLI_NAME} >/dev/null 2>&1; then
  echo "[✓] ${PROJECT_NAME} installed successfully."
  echo "[*] Run '${CLI_NAME} --help' to get started."
else
  echo "[!] Installation completed, but CLI not found in PATH."
  exit 1
fi
