"""Curses drawing engine.

DrawingEngine implementation which uses curses as a drawing framework.
"""

import curses

from sliding_puzzle.drawing_engines.abstract_drawing_engine import DrawingEngine, Key
from sliding_puzzle.drawables.abstract_drawables import Drawable


class CursesDrawingEngine(DrawingEngine):
    """DrawingEngine implementation which uses curses as a drawing framework"""

    def __init__(self) -> None:
        """Initializes CursesDrawingEngine

        Initializes CursesDrawingEngine object and sets all the needed options of the curses framework.
        """
        super().__init__()
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.curs_set(False)
        curses.cbreak()

        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.refresh()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def _refresh_screen(self) -> None:
        """Refreshes(redraws) the screen

        Overrides the method from the DrawingEngine
        """
        self.stdscr.refresh()

    def _draw(self, drawable: Drawable):
        """Implementation of the abstract _draw method from the DrawingEngine.

        Args:
            drawable (Drawable): Drawable to be put on the screen.
        """
        if drawable.visible:
            for y in range(drawable.height):
                try:
                    self.stdscr.addstr(
                        drawable.position.y + y, drawable.position.x, drawable.get_data()[y], curses.color_pair(1)
                    )
                except:
                    pass

    def _update(self):
        """Waits for button press and executes the callback.

        Overrides the method from the DrawingEngine
        """
        key_mapping = {
            27: Key.ESCAPE,
            10: Key.ENTER,
            curses.KEY_DOWN: Key.ARROW_DOWN,
            curses.KEY_UP: Key.ARROW_UP,
            curses.KEY_LEFT: Key.ARROW_LEFT,
            curses.KEY_RIGHT: Key.ARROW_RIGHT,
        }

        key = self.stdscr.getch()

        try:
            self._callbacks[key_mapping[key]]()
        except KeyError:
            pass

    def __del__(self):
        curses.reset_shell_mode()
        curses.endwin()
