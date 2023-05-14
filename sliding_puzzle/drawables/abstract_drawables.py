"""Abstract drawables.

This module defines the abstract drawables. Drawables can be drown. Each drawable "knows" where is
it placed, what size it is and if it is visible. Each drawable can contain more drawables, which
will be drawn on top of it. Child drawable position is relative to parent's top left corner. Only
the part of the child drawable which fits inside the parent drawable will be drawn.
"""

import abc
from typing import Any

from sliding_puzzle.utils import Position


class Drawable(abc.ABC):
    """Abstract drawable class

    Represents the object which cen be drawn.
    """

    def __init__(self, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes Drawable object.

        Args:
            width (int): width of drawable.
            height (int): height of drawable.
            position (Position, optional): position of drawable. Defaults to Position(0, 0).
        """
        self.position = position
        self._width = width
        self._height = height

        self.visible = True

        self.data = None

        self.drawables = []

    def add_drawable(self, drawable, position: Position = Position(0, 0)) -> None:
        """Adds child drawable

        Args:
            drawable (_type_): child drawable.
            position (Position, optional): position of the added drawable, relative to the parent's
                                           top left corner. Defaults to Position(0, 0).
        """
        drawable.position = position
        self.drawables.append(drawable)

    def get_drawables(self) -> list["Drawable"]:
        """Returns all child drawables.

        Returns:
            list[Drawable]: list of child drawables.
        """
        return self.drawables

    @property
    def position(self) -> Position:
        """Returns drawable's position.

        Returns:
            Position: drawable's position.
        """
        return self._position

    @position.setter
    def position(self, position: Position) -> None:
        """Sets drawable's position.

        Args:
            position (Position): drawable's position.
        """
        self._position = position

    @property
    def width(self) -> int:
        """Returns drawable's width

        Returns:
            int: width of the drawable.
        """
        return self._width

    @property
    def height(self) -> int:
        """Returns drawables' height

        Returns:
            int: height of the drawable.
        """
        return self._height

    @abc.abstractmethod
    def get_data(self) -> Any:
        """Returns underlying data of the drawable.

        Returns:
            Any: underlying data used for drawing.
        """
        return self.data

    @property
    def visible(self) -> bool:
        """Allows to check if the drawable is visible.

        Returns:
            bool: visibility of the drawable - true: visible, false: not visible.
        """
        return self._visible

    @visible.setter
    def visible(self, visible: bool) -> None:
        """Allows setting visibility of the drawable.

        Args:
            visible (bool): visibility value to be set.
        """
        self._visible = visible


class Block(Drawable, abc.ABC):
    """Abstract drawable block object.

    The block object is just a rectangular drawable.
    """

    def __init__(self, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes a block object

        Args:
            width (int): block width
            height (int): block height
            position (Position, optional): block position. Defaults to Position(0, 0).
        """
        Drawable.__init__(self, width, height, position)


class TextBox(Drawable, abc.ABC):
    """Abstract text box drawable.

    Text box is a drawable used for drawing text. The text is put into the rectangle box.
    """

    def __init__(self, text: str, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes text box object.

        Args:
            text (str): text of the text box.
            width (int): width of the text box.
            height (int): height of the text box.
            position (Position, optional): text box position. Defaults to Position(0, 0).
        """
        Drawable.__init__(self, width, height, position)
        self.text = text

    @abc.abstractmethod
    def set_text(self, text: str) -> None:
        """Allows changing the text of the text box.

        Args:
            text (str): new text to be put into textbox.
        """
        self.text = text
