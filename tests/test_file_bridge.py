import json
import tempfile
import unittest
from pathlib import Path

from prototype.file_bridge import FileBridge
from prototype.player_state import PlayerState


class FileBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.path = Path(self.temp_dir.name) / "player_state.json"
        self.bridge = FileBridge(self.path)

    def test_write_and_read_state(self):
        state = PlayerState(
            sequence=7,
            buttons=5,
            lx=0.25,
            ly=-0.5,
            lt=0.75,
        )

        self.bridge.write_state(state)
        result = self.bridge.read_state()

        self.assertEqual(result, state)

    def test_missing_file_returns_none(self):
        self.assertIsNone(self.bridge.read_state())

    def test_malformed_json_returns_none(self):
        self.path.write_text("{broken", encoding="utf-8")
        self.assertIsNone(self.bridge.read_state())

    def test_invalid_state_returns_none(self):
        data = json.loads(PlayerState().to_json())
        data["lx"] = 5
        self.path.write_text(json.dumps(data), encoding="utf-8")

        self.assertIsNone(self.bridge.read_state())

    def test_write_replaces_previous_state(self):
        self.bridge.write_state(PlayerState(sequence=1, buttons=1))
        self.bridge.write_state(PlayerState(sequence=2, buttons=4))

        result = self.bridge.read_state()

        self.assertIsNotNone(result)
        self.assertEqual(result.sequence, 2)
        self.assertEqual(result.buttons, 4)

    def test_write_rejects_invalid_state(self):
        state = PlayerState(sequence=-1)

        with self.assertRaises(ValueError):
            self.bridge.write_state(state)

        self.assertFalse(self.path.exists())


if __name__ == "__main__":
    unittest.main()
