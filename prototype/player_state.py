"""Network-independent state representation for remote player input."""

import json
import math
from dataclasses import asdict, dataclass


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
        if type(self.sequence) is not int or self.sequence < 0:
            raise ValueError("sequence must be a non-negative integer")

        if type(self.buttons) is not int or self.buttons < 0:
            raise ValueError("buttons must be a non-negative integer")

        for name in ("lx", "ly", "rx", "ry", "lt", "rt"):
            value = getattr(self, name)

            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite number")

            if not -1.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between -1.0 and 1.0")

        if not 0.0 <= self.lt <= 1.0:
            raise ValueError("lt must be between 0.0 and 1.0")

        if not 0.0 <= self.rt <= 1.0:
            raise ValueError("rt must be between 0.0 and 1.0")

    def to_json(self) -> str:
        self.validate()
        return json.dumps(asdict(self), separators=(",", ":"), allow_nan=False)

    @classmethod
    def from_json(cls, payload: str) -> "PlayerState":
        data = json.loads(payload)

        if not isinstance(data, dict):
            raise ValueError("player state JSON must be an object")

        expected = set(cls.__dataclass_fields__)
        if set(data) != expected:
            raise ValueError("player state JSON has missing or unexpected fields")

        state = cls(**data)
        state.validate()
        return state
