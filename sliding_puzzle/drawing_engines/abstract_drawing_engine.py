"""Abstract drawing engine.

This is an abstraction on a any piece of code which can be used to put stuff on the screen. It also abstracts user
inputs. The implementation of the DrawingEngine has to know how to put object of the Drawable class on the screen.
"""

import abc
import asyncio
from enum import Enum, auto
from typing import Callable

from sliding_puzzle.drawables.abstract_drawables import Drawable


class Key(Enum):
    """Keys enum"""

    ENTER = auto()
    ESCAPE = auto()
    ARROW_UP = auto()
    ARROW_DOWN = auto()
    ARROW_LEFT = auto()
    ARROW_RIGHT = auto()


class DrawingEngine(abc.ABC):
    """Abstract DrawingEngine class.

    This class abstracts drawing things on the screen. It also abstracts handling user inputs. The Drawable objects
    can be added to the canvas, which will be drawn when the draw method is called.
    """

    def __init__(self) -> None:
        """Initializes DrawingEngine object."""
        self._canvas = []

        self._callbacks = {}

    def add_to_canvas(self, drawable: Drawable) -> None:
        """Adds drawable to canvas.

        Args:
            drawable (Drawable): drawable to be put on to the canvas.
        """
        self._canvas.append(drawable)

    async def draw(self, refresh_rate: float = 1 / 30) -> None:
        """Method for drawing Drawables on the screen.

        This method shell be called in a separate thread to redraw elements on the screen.
        Args:
            refresh_rate (float, optional): refresh rate at which the draw shell be called. Defaults to 1/30.
        """
        while True:
            for drawable in self._canvas:
                self._draw_child_drawables(drawable)
            self._refresh_screen()
            self._update()

            await asyncio.sleep(refresh_rate)

    def set_callback(self, key: Key, callback: Callable) -> None:
        """Assigns callback to a Key.

        Args:
            key (Key): Key for which th callback will be set.
            callback (Callable): function to be called when the key is pressed.
        """
        self._callbacks[key] = callback
        self._bind()

    @abc.abstractmethod
    def _draw(self, drawable: Drawable) -> None:
        """_summary_

        Args:
            drawable (_type_): _description_
        """

    def _update(self) -> None:
        """Method called at the start of the draw method.

        Some implementations of the DrawingEngine have to do something before calling draw (eg. wait for button press).
        This method can be overwritten by such class.
        """

    def _bind(self) -> None:
        """Method called after set_callback.

        Some implementations of the DrawingEngine have to do something after setting the callbacks to make them work.
        This method can be overwritten by such class.
        """

    def _refresh_screen(self) -> None:
        """Method called at the end of the draw method.

        Some implementations of the DrawingEngine have to do something after calling draw (eg. refresh the screen).
        This method can be overwritten by such class.
        """

    def _draw_child_drawables(self, drawable: Drawable):
        """Puts Drawable and its children on the screen.

        Args:
            drawable (Drawable): Drawable to be drawn (including its children).
        """
        self._draw(drawable)
        for next_drawable in drawable.get_drawables():
            self._draw_child_drawables(next_drawable)
