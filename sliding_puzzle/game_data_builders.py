"""Game data builders.

This module contains game builders. GameData is class storing all drawables needed fot the SlidingPuzzle game.
GameDataBuilders fill the GameData object with the drawables for particular DrawingEngine implementation.
"""

from PIL import Image

from sliding_puzzle.drawables.curses_drawables import CursesBlankBlock, CursesValueBlock, CursesTextBox

from sliding_puzzle.utils import Position


class GameData:
    """Stores all drawables needed for SlidingPuzzle Game."""

    blank_block = None
    blocks = None
    text_box = None


class CursesGameDataBuilder:
    """Creates GamaData object for suitable for CursesDrawingEngine."""

    @staticmethod
    def get(block_numbers: list[int], num_of_blocks_in_line: int) -> GameData:
        """Creates GamaData object for suitable for TkDrawingEngine.

        Args:
            block_numbers (list[int]):list of numbers to be used as data for ValueBlocks.
            num_of_blocks_in_line (int): number of blocks in one line.

        Returns:
            GameData: GameData object suitable for CursesDrawingEngine.
        """
        block_width = int(100 / num_of_blocks_in_line)
        block_height = int(70 / num_of_blocks_in_line)

        game_data = GameData()
        game_data.blocks = []
        game_data.blank_block = CursesBlankBlock(block_width, block_height)

        i = 0
        for y in range(num_of_blocks_in_line):
            for x in range(num_of_blocks_in_line):
                if x != 0 or y != 0:
                    game_data.blocks.append(
                        CursesValueBlock(
                            str(block_numbers[i]),
                            block_width,
                            block_height,
                            Position(x * block_width, y * block_height),
                        )
                    )
                    i += 1

        game_data.text_box = CursesTextBox(
            "",
            int((block_width * num_of_blocks_in_line) / 2),
            int((block_height * num_of_blocks_in_line) / 2),
            Position(
                int(block_width * num_of_blocks_in_line / 4),
                int(block_height * num_of_blocks_in_line / 4),
            ),
        )

        return game_data
