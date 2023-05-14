"""Tk drawables.

Implementation of the abstract drawables which can be used by Tkabstract_drawing_engine.
"""

import tkinter
from PIL import Image, ImageTk

from sliding_puzzle.drawables.abstract_drawables import Block, TextBox
from sliding_puzzle.utils import Position


class TkValueBlock(Block):
    """Implementation of the abstract Block class.

    This class is the implementation of the Block class, which can be used by the Tkabstract_drawing_engine. This is
    basically a tkinter label containing an image.
    """

    def __init__(self, image: Image, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes TkValueBlock object.

        Args:
            image (Image): image to be set as a Block value.
            width (int): block width.
            height (int): block height
            position (Position, optional): block position. Defaults to Position(0, 0).
        """
        Block.__init__(self, width, height, position)
        self.image = image
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.data = tkinter.Label(image=self.tk_image)

    def get_data(self) -> tkinter.Label:
        """Returns the data to be drawn by the Tkabstract_drawing_engine.

        Returns:
            tkinter.Label: underlying tkinter label object.
        """
        return super().get_data()


class TkBlankBlock(Block):
    """Implementation of the abstract Block class.

    This class is the implementation of the Block class, which can be used by the Tkabstract_drawing_engine. This is
    basically a tkinter label containing an empty (black) image.
    """

    def __init__(self, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes TkValueBlock object.

        Args:
            width (int): block width.
            height (int): block height
            position (Position, optional): block position. Defaults to Position(0, 0).
        """
        Block.__init__(self, width, height, position)
        self.image = Image.new("RGB", (width, height))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.data = tkinter.Label(image=self.tk_image)

    def get_data(self) -> tkinter.Label:
        """Returns the data to be drawn by the Tkabstract_drawing_engine.

        Returns:
            tkinter.Label: underlying tkinter label object.
        """
        return super().get_data()


class TkTextBox(TextBox):
    """Implementation of the abstract TextBox class.

    This class is the implementation of the TextBox class, which can be used by the Tkabstract_drawing_engine. This is
    basically a tkinter label containing a text.
    """

    def __init__(self, text, width: int, height: int, position: Position = Position(0, 0)) -> None:
        """Initializes TkTextBox object.

        Args:
            text (str): text to be put into text box.
            width (int): text box width.
            height (int): text box height.
            position (Position, optional): text box position. Defaults to Position(0, 0).
        """
        TextBox.__init__(self, text, width, height, position)
        self.data = tkinter.Label(text=text, width=width, height=height)

    def set_text(self, text: str) -> None:
        """Sets text of the TextBox.

        Args:
            text (str): text to be set.
        """
        TextBox.set_text(self, text)
        self.data.config(text=self.text)

    def get_data(self) -> tkinter.Label:
        """Returns the data to be drawn by the Tkabstract_drawing_engine.

        Returns:
            tkinter.Label: underlying tkinter label object.
        """
        return super().get_data()
