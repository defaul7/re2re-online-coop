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
- [x] Added prototype/file_bridge.py for atomic JSON state-file updates.
- [x] Added six isolated FileBridge tests using temporary directories.
- [x] Ran the complete automated test suite: 19 tests passed.
- [x] Committed the Python file bridge prototype as 3e494ff.

## Current implementation

- prototype/server.py: UDP echo server bound to 0.0.0.0:37020.
  Do not run it for internet testing until that stage is planned.
- prototype/client.py: UDP test client.
- prototype/player_state.py: validated PlayerState dataclass with JSON serialization.
- prototype/state_receiver.py: accepts only strictly newer player states.
- prototype/message_handler.py: validates incoming JSON state messages.
- prototype/udp_receiver.py: bounded UDP receiver; binds to localhost by default.
- prototype/file_bridge.py: atomic JSON file bridge prototype for Python state files.
- tests/test_file_bridge.py: six file-bridge tests using temporary directories.
- tests/: automated tests for file bridge, message handling, and UDP receiver.
- reference/local-couch-co-op/re2coop_main.lua: local reference copy of the
  third-party mod; intentionally not tracked by Git.

## Lua integration findings

- PD.vpad is the existing virtual gamepad used by Player 2.
- PD.update() updates its buttons, sticks, and triggers.
- st.set_p2() selects the local input source and assigns the virtual pad.
- st.p2_choices() populates the existing local input selection menu.
- No direct socket API was found in the searched Lua source. This does not
  prove that no networking option exists in the wider REFramework environment.
- A Python file bridge prototype exists, but it has not been tested with REFramework.
- The actual REFramework data path and file-sharing behavior remain unverified.
- No Lua source changes or installed-game changes have been made.

## Git and reference-source rules

- Check `git status --short` before each commit.
- Keep reference/ untracked until redistribution rights are understood.
- Never stage reference/ when committing project code or documentation.
- Keep project notes current so development can resume after a break.

## Next steps

1. Verify this documentation update and inspect the working tree.
2. Commit the documentation update.
3. Evaluate safe file exchange and the REFramework data path without changing game files.
4. Define freshness, update-rate, and timeout requirements for remote input.
5. Design the Lua integration only after the bridge approach is justified.
6. Plan two-computer testing later; do not test internet connectivity or router forwarding yet.

## Important limitations

- The UDP prototype is not yet integrated into the game.
- The project does not yet provide online co-op.
- Packet validation and local loopback tests do not establish internet reliability,
  latency, security, or compatibility with the game.
- Third-party source licensing and redistribution permissions remain unresolved.

## File bridge research

- REFramework fs.read(filename) and fs.write(filename, data) are documented; relative paths resolve under reframework/data/ by default.
- The installed game has a reframework/data directory, but Python-to-Lua file exchange has not been tested.
- PD.vpad stores buttons, previous-frame buttons, two sticks, and two triggers; st.p2_dev reads the virtual pad.
- PD.update() runs once per game frame. Button-down and button-up depend on current and previous button masks.
- Existing PD.read_ext() throttles file reads; its source comments report 2 ms and occasional 16–20 ms stalls from frequent file reads.
- Do not read the bridge file every frame. A safe update interval, stale-input timeout, and path-sharing method must be established before Lua integration.
- No Lua or installed-game files have been modified.

## Native REFramework diagnostic plugin

- Added `prototype/reframework_plugin.cpp`, a minimal diagnostic plugin using the REFramework `v1.5.9.1` API header.
- The plugin declares `reframework_plugin_required_version` and `reframework_plugin_initialize`.
- The Lua-state callbacks are registered during initialization; they currently perform no game operations.
- Built `build/re2_online_coop.dll` with `x86_64-w64-mingw32-g++` using the `v1.5.9.1` headers.
- Verified that the output is a 64-bit Windows PE DLL and that both required exports are present.
- The DLL has NOT been loaded by REFramework yet. Runtime compatibility, callback behavior, and logging remain unverified.
- `build/` is ignored by Git. Do not copy the DLL into the installed game until a separate, explicit test plan is agreed.
- The diagnostic plugin is not an online-co-op implementation and does not exchange network or player-state data.
