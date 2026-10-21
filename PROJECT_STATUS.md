## Project goal

Develop a free online co-op prototype for Resident Evil 2 Remake (2019),
building on the existing Local Couch Co-op mod where possible.

## Environment

- Developer OS: Pop!_OS 24.04 LTS
- Game: Steam version, running through Proton
- Other player: Windows 11, Steam
- Repository: ~/re2-online-coop
- Branch: main
- Development tools and services must be free.

## Safety rules

- Do not modify installed game files or saves without explicit permission.
- Keep experiments and development files inside this repository.
- Do not add third-party mod source to Git until its licensing and
  redistribution permissions are understood.
- Do not test internet connectivity or router forwarding until that
  stage is explicitly planned.
- Use one terminal task per instruction and inspect its actual output.
- Prefer small, testable changes with Git checkpoints.
- Preserve existing Local Couch Co-op gameplay logic where possible.

## Completed

- [x] Initialized a local Git repository.
- [x] Created a UDP echo server and client prototype.
- [x] Tested local UDP communication successfully.
- [x] Copied the existing Local Couch Co-op Lua script into reference/.
- [x] Inspected the virtual gamepad and Player 2 input update logic.
- [x] Created prototype/player_state.py.
- [x] Validated sequence numbers, button masks, stick values, and triggers.
- [x] Added JSON serialization and deserialization for PlayerState.
- [x] Added StateReceiver to reject duplicate and stale sequence numbers.
- [x] Added MessageHandler for JSON validation and state reception.
- [x] Added tests for valid, malformed, and invalid player-state messages.
- [x] Added a bounded UDP state receiver on localhost port 37021 by default.
- [x] Added tests for packet size limits and malformed datagrams.
- [x] Ran the complete automated test suite: 13 tests passed.
- [x] Ran a local UDP loopback integration check successfully.
- [x] Saved the bounded UDP receiver and tests in commit 5a03913.
- [x] Inspected Lua PD.update(), st.set_p2(), and st.p2_choices().

## Current implementation

- prototype/server.py: UDP echo server bound to 0.0.0.0:37020.
  Do not run it for internet testing until that stage is planned.
- prototype/client.py: UDP test client.
- prototype/player_state.py: validated PlayerState dataclass with JSON serialization.
- prototype/state_receiver.py: accepts only strictly newer player states.
- prototype/message_handler.py: validates incoming JSON state messages.
- prototype/udp_receiver.py: bounded UDP receiver; binds to localhost by default.
- tests/: automated tests for message handling and UDP receiver.
- reference/local-couch-co-op/re2coop_main.lua: local reference copy of the
  third-party mod; intentionally not tracked by Git.

## Lua integration findings

- PD.vpad is the existing virtual gamepad used by Player 2.
- PD.update() updates its buttons, sticks, and triggers.
- st.set_p2() selects the local input source and assigns the virtual pad.
- st.p2_choices() populates the existing local input selection menu.
- No direct socket API was found in the searched Lua source. This does not
  prove that no networking option exists in the wider REFramework environment.
- A local Python-to-Lua bridge is one option to investigate, not yet implemented.
- No Lua source changes or installed-game changes have been made.

## Git and reference-source rules

- Check `git status --short` before each commit.
- Keep reference/ untracked until redistribution rights are understood.
- Never stage reference/ when committing project code or documentation.
- Keep project notes current so development can resume after a break.

## Next steps

1. Verify this documentation update and inspect the working tree.
2. Commit the documentation update.
3. Continue evaluating a safe local Python-to-Lua bridge without launching the game.
4. Define freshness, rate, and timeout requirements for remote input.
5. Design the Lua integration only after the bridge approach is justified.
6. Plan two-computer testing later; do not test internet connectivity or router forwarding yet.

## Important limitations

- The UDP prototype is not yet integrated into the game.
- The project does not yet provide online co-op.
- Packet validation and local loopback tests do not establish internet reliability,
  latency, security, or compatibility with the game.
- Third-party source licensing and redistribution permissions remain unresolved.
