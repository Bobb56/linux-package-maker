#!/bin/bash
SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"

chmod +x "$SCRIPT_DIR/lpm-env/bin/python3"

if [[ "$1" == "build" ]]; then
    "$SCRIPT_DIR/lpm-env/bin/python3" "$SCRIPT_DIR/LPM.py" "$2"
else
    "$SCRIPT_DIR/lpm-env/bin/python3" "$SCRIPT_DIR/lpm-gui.py"
fi
