import json
import unittest

from prototype.player_state import PlayerState
from prototype.udp_receiver import MAX_PACKET_SIZE, UDPStateReceiver


class UDPStateReceiverTests(unittest.TestCase):
    def setUp(self):
        self.receiver = UDPStateReceiver()

    def encode(self, state):
        return state.to_json().encode("utf-8")

    def test_accepts_valid_datagram(self):
        self.assertTrue(
            self.receiver.process_datagram(
                self.encode(PlayerState(sequence=1, buttons=1))
            )
        )

    def test_rejects_empty_datagram(self):
        self.assertFalse(self.receiver.process_datagram(b""))

    def test_rejects_malformed_json(self):
        self.assertFalse(self.receiver.process_datagram(b"{broken json"))

    def test_rejects_invalid_utf8(self):
        self.assertFalse(self.receiver.process_datagram(b"\xff\xfe"))

    def test_rejects_oversized_datagram(self):
        self.assertFalse(
            self.receiver.process_datagram(b"x" * (MAX_PACKET_SIZE + 1))
        )

    def test_rejects_invalid_player_state(self):
        data = json.loads(PlayerState(sequence=2).to_json())
        data["lx"] = 10
        self.assertFalse(
            self.receiver.process_datagram(json.dumps(data).encode("utf-8"))
        )

    def test_accepts_newer_and_rejects_stale_datagrams(self):
        self.assertTrue(
            self.receiver.process_datagram(
                self.encode(PlayerState(sequence=3, buttons=3))
            )
        )
        self.assertFalse(
            self.receiver.process_datagram(
                self.encode(PlayerState(sequence=2, buttons=2))
            )
        )

        latest = self.receiver.handler.receiver.latest
        self.assertIsNotNone(latest)
        self.assertEqual(latest.sequence, 3)
        self.assertEqual(latest.buttons, 3)


if __name__ == "__main__":
    unittest.main()
