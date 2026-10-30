#!/usr/bin/env bash
# Install cofa-skills into Codex skill folders.
#   bash install.sh              -> $HOME/.agents/skills   (user scope, not part of the workspace)
#   bash install.sh --project    -> ./.agents/skills       (repo scope, current directory)
#   add --with-pstack            -> also copy a small subset of pstack principle skills (MIT, backnotprop/pstack)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dest="$HOME/.agents/skills"
with_pstack=0
for a in "$@"; do
  case "$a" in
    --project) dest="$PWD/.agents/skills" ;;
    --with-pstack) with_pstack=1 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done
mkdir -p "$dest"
for d in "$here"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "${dest:?}/$name"
  cp -R "$d" "$dest/$name"
  echo "installed $name"
done
if [ "$with_pstack" = 1 ]; then
  tmp="$(mktemp -d)"
  git clone -q --depth 1 https://github.com/backnotprop/pstack "$tmp/pstack"
  for s in principle-prove-it-works principle-explain-the-number principle-fix-root-causes \
           principle-laziness-protocol principle-subtract-before-you-add in-your-own-words; do
    rm -rf "${dest:?}/$s"
    cp -R "$tmp/pstack/skills/$s" "$dest/$s"
    echo "installed pstack/$s"
  done
  rm -rf "$tmp"
fi
echo "done -> $dest  (restart codex if skills do not show in /skills)"
