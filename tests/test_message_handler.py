import json
import unittest

from prototype.message_handler import MessageHandler
from prototype.player_state import PlayerState


class MessageHandlerTests(unittest.TestCase):
    def setUp(self):
        self.handler = MessageHandler()

    def test_accepts_valid_state(self):
        payload = PlayerState(sequence=1, buttons=1).to_json()
        self.assertTrue(self.handler.handle(payload))

    def test_rejects_malformed_json(self):
        self.assertFalse(self.handler.handle("{broken json"))

    def test_rejects_invalid_axis(self):
        data = json.loads(PlayerState(sequence=1).to_json())
        data["lx"] = 5.0
        self.assertFalse(self.handler.handle(json.dumps(data)))

    def test_accepts_newer_state(self):
        self.assertTrue(self.handler.handle(PlayerState(sequence=1).to_json()))
        self.assertTrue(self.handler.handle(PlayerState(sequence=2).to_json()))

    def test_rejects_stale_and_duplicate_states(self):
        self.assertTrue(self.handler.handle(PlayerState(sequence=3, buttons=3).to_json()))
        self.assertFalse(self.handler.handle(PlayerState(sequence=2, buttons=2).to_json()))
        self.assertFalse(self.handler.handle(PlayerState(sequence=3, buttons=4).to_json()))

    def test_rejected_messages_do_not_change_latest_state(self):
        self.handler.handle(PlayerState(sequence=3, buttons=3).to_json())
        self.handler.handle("{broken json")
        self.handler.handle(PlayerState(sequence=2, buttons=2).to_json())

        latest = self.handler.receiver.latest
        self.assertIsNotNone(latest)
        self.assertEqual(latest.sequence, 3)
        self.assertEqual(latest.buttons, 3)


if __name__ == "__main__":
    unittest.main()
