"""Curses drawables.

Implementation of the abstract drawables which can be used by CursesDrawingEngine.
"""

import textwrap

from sliding_puzzle.utils import Position
from sliding_puzzle.drawables.abstract_drawables import Block, TextBox


class CursesValueBlock(Block):
    """Implementation of the abstract Block class.

    This class is the implementation of the Block class, which can be used by the CursesDrawingEngine. This is
    basically an "ascii art" version of the Block. It consist of border around its perimeter, and the value in the
    middle.
    """

    def __init__(self, value: str, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes the CursesValueBlock object.

        Args:
            value (str): value of the block.
            width (int): block width.
            height (int): block height.
            position (Position, optional): block position. Defaults to Position(0, 0).
        """
        Block.__init__(self, width, height, position)
        edge_line = " " + "-" * (width - 2) + " "
        middle_line = "|" + " " * (width - 2) + "|"
        text_line = "|" + value.center(width - 2) + "|"

        self.data = [edge_line] + [middle_line] * (height - 2) + [edge_line]

        self.data[int(height / 2)] = text_line

    def get_data(self) -> list[str]:
        """Returns the data to be drawn by the CursesDrawingEngine.

        Returns:
            list[str]: data of the Block.
        """
        return super().get_data()


class CursesBlankBlock(Block):
    """Implementation of the abstract Block class.

    This class is the implementation of the Block class, which can be used by the CursesDrawingEngine. This is
    basically an "ascii art" version of the Block. It consist of border around its perimeter, and spaces in the
    middle.
    """

    def __init__(self, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes the CursesValueBlock object.

        Args:
            width (int): block width.
            height (int): block height.
            position (Position, optional): block position. Defaults to Position(0, 0).
        """
        Block.__init__(self, width, height, position)
        middle_line = " " * width
        self.data = [middle_line] * height

    def get_data(self) -> list[str]:
        """Returns the data to be drawn by the CursesDrawingEngine.

        Returns:
            list[str]: data of the Block.
        """
        return super().get_data()


class CursesTextBox(TextBox):
    """Implementation of the abstract TextBox class.

    This class is the implementation of the TextBox class, which can be used by the CursesDrawingEngine. This is
    basically an "ascii art" version of the TextBox. It consist of text inside of an empty box.
    """

    def __init__(self, text: str, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes CursesTextBox object.

        Args:
            text (str): text to be put into text box.
            width (int): text box width.
            height (int): text box height.
            position (Position, optional): text box position. Defaults to Position(0, 0).
        """
        TextBox.__init__(self, text, width, height, position)
        self.set_text(text)

    def set_text(self, text: str) -> None:
        """Sets text of the TextBox.

        Args:
            text (str): text to be set.
        """
        super().set_text(text)

        self.data = ["#" * self.width]

        lines = text.split("\n")

        lines_2 = []
        for line in lines:
            if len(line) > self.width - 2:
                lines_2 += textwrap.wrap(line, self.width - 2)
            else:
                lines_2.append(line)

        for line in lines_2:
            self.data.append("#" + line.center(self.width - 2) + "#")
            if len(self.data) == self.height:
                break

        if len(self.data) < self.height:
            for _ in range(self.height - len(self.data)):
                self.data.append("#" + " ".center(self.width - 2) + "#")

        self.data[-1] = "#" * self.width

    def get_data(self) -> list[str]:
        """Returns the data to be drawn by the CursesDrawingEngine.

        Returns:
            list[str]: data of the Block.
        """
        return super().get_data()
