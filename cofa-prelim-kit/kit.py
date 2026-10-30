#!/usr/bin/env python3
"""COFA local task helper. No network or model connection on normal commands."""
from kitlib.cli import main

if __name__ == '__main__':
    raise SystemExit(main())
