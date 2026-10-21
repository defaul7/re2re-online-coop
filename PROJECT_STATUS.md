# RE2 Online Co-op — Project Status

## Project goal

Develop a free online co-op prototype for Resident Evil 2 Remake (2019),
building on the existing Local Couch Co-op mod where possible.

## Environment

- Developer OS: Pop!_OS 24.04 LTS
- Game: Steam version, running through Proton
- Other player: Windows 11, Steam
- Repository: ~/re2-online-coop
- Branch: main

## Safety rules

- Do not modify installed game files or saves without explicit permission.
- Keep experiments and development files inside this repository.
- Do not add third-party mod source to Git until its licensing and
  redistribution permissions are understood.
- Do not test internet connectivity or router forwarding until that
  stage is explicitly planned.
- Use one terminal task per instruction and inspect its actual output.

## Completed

- [x] Initialized a local Git repository.
- [x] Created a UDP echo server and client prototype.
- [x] Tested local UDP communication successfully.
- [x] Copied the existing Local Couch Co-op Lua script into reference/.
- [x] Inspected the virtual gamepad and Player 2 input update logic.
- [x] Created prototype/player_state.py.
- [x] Verified valid player state values.
- [x] Verified rejection of invalid stick, trigger, sequence, and button values.

## Current implementation

- prototype/server.py: UDP echo server; HOST was changed to 0.0.0.0
  and this change is not yet committed.
- prototype/client.py: local UDP test client.
- prototype/player_state.py: validated PlayerState dataclass.
- reference/local-couch-co-op/re2coop_main.lua: local reference copy;
  not tracked by Git.

## Current Git state at last inspection

- Modified: prototype/server.py
- Untracked: prototype/player_state.py
- Untracked: reference/
- Python cache files are excluded by .gitignore.

## Next steps

1. Add Python cache exclusions to .gitignore.
2. Review and test the player state module.
3. Design and test JSON serialization for player state.
4. Define network message handling and stale-packet protection.
5. Inspect the existing mod's input integration points further.
6. Only later plan safe integration and two-computer testing.

## Important limitations
cd ~/re2-online-coop && cat > .gitignore <<'EOF'
# Python-generated files
__pycache__/
*.py[cod]

# Virtual environments
.venv/
venv/

# Local environment and secrets
.env
.env.*
!.env.example
