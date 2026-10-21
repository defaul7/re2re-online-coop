"""Validate incoming player-state messages and reject stale states."""

from prototype.player_state import PlayerState
from prototype.state_receiver import StateReceiver


class MessageHandler:
    """Process JSON player-state messages without performing network I/O."""

    def __init__(self) -> None:
        self.receiver = StateReceiver()

    def handle(self, payload: str) -> bool:
        """Return True if a valid, newer player state was accepted."""
        try:
            state = PlayerState.from_json(payload)
        except (ValueError, TypeError):
            return False

        return self.receiver.accept(state)
