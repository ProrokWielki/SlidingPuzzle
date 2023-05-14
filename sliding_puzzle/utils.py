"""Container for utils"""

from enum import Enum, auto
from dataclasses import dataclass


class Direction(Enum):
    """Enumeration representing direction"""

    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


@dataclass(frozen=False, eq=True)
class Position:
    """Class representing position - in euclidean space"""

    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)
