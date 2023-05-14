"""Tkinter drawing engine.

DrawingEngine implementation which uses tkinter as a drawing framework.
"""

import tkinter
from threading import Thread

from sliding_puzzle.drawing_engines.abstract_drawing_engine import DrawingEngine, Key
from sliding_puzzle.drawables.abstract_drawables import Drawable


class TkDrawingEngine(DrawingEngine):
    """DrawingEngine implementation which uses tkinter as a drawing framework."""

    def __init__(self) -> None:
        """Initializes TkDrawingEngine

        Initializes TkDrawingEngine object. Starts separate thread for the tkinter mainloop method.
        """
        super().__init__()
        self.root = None
        self.thread = Thread(target=self._tk_inter_thread, daemon=True)
        self.thread.start()

    def _tk_inter_thread(self) -> None:
        """Thread for the tkinter mainloop method"""
        self.root = tkinter.Tk()
        self.root.geometry("800x600")
        self.root.resizable(0, 0)
        self.root.mainloop()

    def _bind(self):
        """Binds keys to the callbacks.

        Overrides method from the DrawingEngine.
        """
        key_mapping = {
            Key.ARROW_LEFT: "<Left>",
            Key.ARROW_RIGHT: "<Right>",
            Key.ARROW_UP: "<Up>",
            Key.ARROW_DOWN: "<Down>",
            Key.ENTER: "<Return>",
            Key.ESCAPE: "<Escape>",
        }

        for key, _ in self._callbacks.items():
            self.root.bind(key_mapping[key], self._callbacks[key])

        if Key.ESCAPE in self._callbacks:
            self.root.protocol("WM_DELETE_WINDOW", self._callbacks[Key.ESCAPE]),

    def _draw(self, drawable: Drawable):
        """Implementation of the abstract _draw method from the DrawingEngine.

        Args:
            drawable (Drawable): Drawable to be put on the screen.
        """
        if drawable.visible:
            drawable.get_data().place(
                x=drawable.position.x, y=drawable.position.y, height=drawable.height, width=drawable.width
            )
        else:
            drawable.get_data().place_forget()
