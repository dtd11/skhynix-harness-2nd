# Editing this toolkit

This repository is a reusable public tool kit, not an exam solution. Keep task data out of it.
Runtime task instructions are installed from `assets/AGENTS-block.md` into a separate project.
The `upstream/` snapshots are unmodified reference material. Do not run their installers, hooks or provider setup commands.
After changing a distributable file, rebuild `bundle-lock.json` with `python scripts/build_manifest.py` and run the meaningful CLI tests.
Use only local processes in tests; never use browser automation or upload participant files.
Do not modify global agent configuration.
