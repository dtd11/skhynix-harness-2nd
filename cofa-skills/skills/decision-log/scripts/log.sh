#!/usr/bin/env bash
# Append one row to DECISIONS.md (markdown table). Usage: log.sh <phase> <decision> <why> <evidence> <result>
set -euo pipefail
f="${DECISIONS_FILE:-DECISIONS.md}"
if [ ! -f "$f" ]; then
  printf '| 시각 | 단계 | 결정 | 이유 | 근거 | 결과 |\n|---|---|---|---|---|---|\n' > "$f"
fi
clean() { printf '%s' "$1" | tr '\n\t' '  ' | sed 's/|/\\|/g'; }
printf '| %s | %s | %s | %s | %s | %s |\n' "$(date '+%H:%M')" "$(clean "${1:-}")" "$(clean "${2:-}")" "$(clean "${3:-}")" "$(clean "${4:-}")" "$(clean "${5:-}")" >> "$f"
echo "logged to $f"
