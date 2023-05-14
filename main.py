import argparse
import asyncio
import signal
from PIL import Image, UnidentifiedImageError

from sliding_puzzle.drawing_engines.abstract_drawing_engine import Key
from sliding_puzzle.drawing_engines.curses_drawing_engine import CursesDrawingEngine
from sliding_puzzle.drawing_engines.tk_drawing_engine import TkDrawingEngine
from sliding_puzzle.game_engine import GameEngine
from sliding_puzzle.game_data_builders import TkGameDataBuilder, CursesGameDataBuilder


def valid_size(size: int) -> int:
    """Validator for the size argument of the SlidingPuzzle game.

    Args:
        size (int): size to be checked.

    Raises:
        argparse.ArgumentTypeError: raised exception when the size is invalid.

    Returns:
        int: valid size.
    """
    size = int(size)
    if size < 2:
        raise argparse.ArgumentTypeError("Minimum SIZE is 2")
    return size


def valid_file(file: str) -> str:
    """Validator for the image file argument of the SlidingPuzzle game.

    Args:
        file (str): file path to be validated.

    Raises:
        argparse.ArgumentTypeError: raised exception when the file path or file is invalid.

    Returns:
        str: valid file path.
    """
    try:
        Image.open(file)
    except (FileNotFoundError, UnidentifiedImageError) as exc:
        raise argparse.ArgumentTypeError(f"{file} is not a valid image file.") from exc
    return file


async def main():
    """main function of the SlidingPuzzle game."""
    parser = argparse.ArgumentParser(prog="sliding_puzzle", description="SlidingPuzzle game.")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--curses", action="store_true", help="Use curses to play the game.")
    group.add_argument("--tk", dest="image_path", type=valid_file, help="Use tkinter to play the game")

    parser.add_argument(
        "SIZE", metavar="SIZE", type=valid_size, help="number of columns and rows (game board size is SIZE x SIZE)"
    )

    args = parser.parse_args()

    if args.curses:
        drawing_engine = CursesDrawingEngine()
        game_data = CursesGameDataBuilder.get(range(1, args.SIZE * args.SIZE), args.SIZE)

    elif args.image_path:
        drawing_engine = TkDrawingEngine()

        image = Image.open(args.image_path)
        image.thumbnail((800, 600))

        game_data = TkGameDataBuilder.get(image, args.SIZE)

    drawing_engine.add_to_canvas(game_data.blank_block)
    for i in game_data.blocks:
        drawing_engine.add_to_canvas(i)
    drawing_engine.add_to_canvas(game_data.text_box)

    game_engine = GameEngine(args.SIZE, game_data)

    drawing_engine.set_callback(Key.ARROW_LEFT, game_engine.move_blank_block_left)
    drawing_engine.set_callback(Key.ARROW_RIGHT, game_engine.move_blank_block_right)
    drawing_engine.set_callback(Key.ARROW_UP, game_engine.move_blank_block_up)
    drawing_engine.set_callback(Key.ARROW_DOWN, game_engine.move_blank_block_down)
    drawing_engine.set_callback(Key.ENTER, game_engine.handle_enter)
    drawing_engine.set_callback(Key.ESCAPE, game_engine.handle_escape)

    signal.signal(signal.SIGINT, game_engine.handle_escape)

    await asyncio.wait(
        [asyncio.create_task(game_engine.run()), asyncio.create_task(drawing_engine.draw())],
        return_when=asyncio.FIRST_COMPLETED,
    )


if __name__ == "__main__":
    asyncio.run(main())
