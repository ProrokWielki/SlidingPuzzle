"""Grid

This module defines Grid class. Grid class is a container which assigns each stored object an x,y coordinate.
"""

from sliding_puzzle.drawables.abstract_drawables import Block
from sliding_puzzle.utils import Position


class Grid:
    """Container which assigns each stored object an x,y coordinate."""

    def __init__(self, grid_width: int, objects: list[Block]) -> None:
        """Initializes Grid object.

        Args:
            grid_width (int): number of columns of the grid.
            objects (list[Block]): objects to be stored in the grid.
        """
        self.grid_width = grid_width
        self.grid = objects

    def __call__(self, position: Position) -> Block:
        """Return object stored at given position.

        Args:
            position (Position): grid position from which to return stored object.

        Returns:
            Block: block stored at the given position.
        """
        return self.grid[position.y * self.grid_width + position.x]

    def get_position(self, object: Block) -> Position:
        """Returns position of the given object, throws if it is not in the grid.

        Args:
            object (Block): object which position will be returned.

        Returns:
            Position: position of the provided object.
        """
        index = self.grid.index(object)
        return Position(index % self.grid_width, int(index / (len(self.grid) / self.grid_width)))

    def swap(self, lhs: Position, rhs: Position) -> None:
        """Swaps object at the given positions.

        Args:
            lhs (Position): position of the object to be swapped.
            rhs (Position): position of the object to be swapped with.
        """
        tmp = self.grid[self._to_index(lhs)]
        self.grid[self._to_index(lhs)] = self.grid[self._to_index(rhs)]
        self.grid[self._to_index(rhs)] = tmp

        tmp = self.grid[self._to_index(lhs)].position
        self.grid[self._to_index(lhs)].position = self.grid[self._to_index(rhs)].position
        self.grid[self._to_index(rhs)].position = tmp

    def _to_index(self, position: Position) -> int:
        """Converts position to index - from x,y coordinates to index on the list.

        Args:
            position (Position): position to be converted to index.

        Returns:
            int: index calculated from the given position.
        """
        return position.y * self.grid_width + position.x
