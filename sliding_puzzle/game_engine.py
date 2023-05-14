"""Module containing main logic for the SlidingPuzzle game."""

import random
import asyncio
import time

from sliding_puzzle.grid import Grid
from sliding_puzzle.utils import Direction, Position
from sliding_puzzle.game_data_builders import GameData


class GameEngine:
    """Class responsible for the logic of the SlidingPuzzle game."""

    direction_to_offset = {
        Direction.DOWN: Position(0, -1),
        Direction.UP: Position(0, 1),
        Direction.LEFT: Position(1, 0),
        Direction.RIGHT: Position(-1, 0),
    }

    def __init__(self, num_of_blocks_in_line: int, game_data: GameData) -> None:
        """Creates GameEngine object

        Args:
            num_of_blocks_in_line (int): number of blocks in a line.
            game_data (GameData): GamaData to be used.
        """

        self.game_data = game_data

        self.size = num_of_blocks_in_line
        self.grid = Grid(num_of_blocks_in_line, [game_data.blank_block] + game_data.blocks)

        self.blank_block = self.grid.grid[0]
        self.correct_order = self.grid.grid[:]

        self.enter_pressed = False
        self.escape_pressed = False

        self._allow_moving = False

    def move_blank_block_down(self, *_) -> None:
        """Callback function to be called to move the blank block down."""
        self._move_blank_block(Direction.DOWN)

    def move_blank_block_up(self, *_) -> None:
        """Callback function to be called to move the blank block up."""
        self._move_blank_block(Direction.UP)

    def move_blank_block_left(self, *_) -> None:
        """Callback function to be called to move the blank block left."""
        self._move_blank_block(Direction.LEFT)

    def move_blank_block_right(self, *_) -> None:
        """Callback function to be called to move the blank block right."""
        self._move_blank_block(Direction.RIGHT)

    def handle_enter(self, *_) -> None:
        """Callback function to be called when enter is pressed."""
        self.enter_pressed = True

    def handle_escape(self, *_) -> None:
        """Callback function to be called when escape is pressed."""
        self.escape_pressed = True

    def _move_blank_block(self, direction: Direction) -> None:
        """Moves the blank block in a given direction.

        Args:
            direction (Direction): direction to which move the blank block.
        """
        if not self._is_valid_position(self.grid.get_position(self.blank_block) + self.direction_to_offset[direction]):
            return

        if not self._allow_moving:
            return

        if direction == Direction.DOWN:
            self.grid.swap(
                self.grid.get_position(self.blank_block), self.grid.get_position(self.blank_block) + Position(0, -1)
            )
        if direction == Direction.UP:
            self.grid.swap(
                self.grid.get_position(self.blank_block), self.grid.get_position(self.blank_block) + Position(0, +1)
            )
        if direction == Direction.LEFT:
            self.grid.swap(
                self.grid.get_position(self.blank_block), self.grid.get_position(self.blank_block) + Position(+1, 0)
            )
        if direction == Direction.RIGHT:
            self.grid.swap(
                self.grid.get_position(self.blank_block), self.grid.get_position(self.blank_block) + Position(-1, 0)
            )

    def _enter_pressed(self) -> bool:
        """Allows checking if enter was pressed.

        Returns:
            bool: true if enter was pressed since last call to _enter_pressed, false otherwise.
        """
        if self.enter_pressed:
            self.enter_pressed = False
            return True
        return False

    def _escape_pressed(self) -> bool:
        """Allows checking if escape was pressed.

        Returns:
            bool: true if escape was pressed since last call to _escape_pressed, false otherwise.
        """
        if self.escape_pressed:
            self.escape_pressed = False
            return True
        return False

    def _is_solved(self) -> bool:
        """Checks if puzzle is solved.

        Returns:
            bool: true if puzzle is solved, false otherwise.
        """
        return self.correct_order == self.grid.grid

    def _is_valid_position(self, blank_position: Position) -> bool:
        """Checks if given position is within the game boarders.

        Args:
            blank_position (Position): position to be checked.

        Returns:
            bool: true if given is within the game boarders, false otherwise.
        """
        return (
            blank_position.x >= 0
            and blank_position.x < self.size
            and blank_position.y >= 0
            and blank_position.y < self.size
        )

    def _shuffle_board(self) -> None:
        """Shuffles the board - guarantees solvability."""
        move_list = 3 * [Direction.DOWN] + 3 * [Direction.RIGHT] + 2 * [Direction.LEFT] + 2 * [Direction.UP]
        for _ in range(2000):
            self._move_blank_block(random.choice(move_list))

    async def run(self) -> None:
        """Main run function."""

        self.game_data.text_box.set_text(
            "Welcome to SlidingPuzzle\n"
            "Use arrow keys to move the empty tile.\n"
            "Press Escape to exit.\nPress Enter to start."
        )
        self.game_data.text_box.visible = True

        while not self._enter_pressed():
            if self._escape_pressed():
                return
            await asyncio.sleep(0.2)

        game_started = time.time()

        self.game_data.text_box.visible = False
        self._allow_moving = True

        self._shuffle_board()

        while not self._is_solved():
            if self._escape_pressed():
                return
            await asyncio.sleep(0.2)

        game_solved = time.time()

        self.game_data.text_box.set_text(
            f"Congratulations\nYou solved the puzzle in {int(game_solved - game_started)} seconds.\n"
            "Press enter to exit."
        )
        self.game_data.text_box.visible = True
        self._allow_moving = False

        while not self._enter_pressed():
            await asyncio.sleep(0.2)
