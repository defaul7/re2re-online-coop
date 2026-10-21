"""Network-independent state representation for remote player input."""

from dataclasses import dataclass


@dataclass
class PlayerState:
    sequence: int = 0
    buttons: int = 0
    lx: float = 0.0
    ly: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    lt: float = 0.0
    rt: float = 0.0

    def validate(self) -> None:
        if self.sequence < 0:
            raise ValueError("sequence must be non-negative")

        if self.buttons < 0:
            raise ValueError("buttons must be non-negative")

        for name in ("lx", "ly", "rx", "ry", "lt", "rt"):
            value = getattr(self, name)
            if not -1.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between -1.0 and 1.0")

        if not 0.0 <= self.lt <= 1.0:
            raise ValueError("lt must be between 0.0 and 1.0")

        if not 0.0 <= self.rt <= 1.0:
            raise ValueError("rt must be between 0.0 and 1.0")
