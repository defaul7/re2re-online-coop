"""Atomic JSON file bridge prototype for player state."""

import json
import os
import tempfile
from pathlib import Path

from prototype.player_state import PlayerState


class FileBridge:
    """Write complete player states using an atomic file replacement."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def write_state(self, state: PlayerState) -> None:
        """Validate and atomically publish one player state."""
        payload = state.to_json()
        self.path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temp_file:
                temp_path = Path(temp_file.name)
                temp_file.write(payload)
                temp_file.flush()
                os.fsync(temp_file.fileno())

            os.replace(temp_path, self.path)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def read_state(self) -> PlayerState | None:
        """Read a complete state; return None for missing or invalid data."""
        try:
            payload = self.path.read_text(encoding="utf-8")
            return PlayerState.from_json(payload)
        except (OSError, UnicodeDecodeError, ValueError, TypeError):
            return None
