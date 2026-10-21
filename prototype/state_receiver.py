"""Accept only newer remote player states."""

from prototype.player_state import PlayerState


class StateReceiver:
    def __init__(self) -> None:
        self.latest: PlayerState | None = None

    def accept(self, state: PlayerState) -> bool:
        state.validate()

        if self.latest is not None:
            if state.sequence <= self.latest.sequence:
                return False

        self.latest = state
        return True
