import argparse


class FLAGS:
    LOGGING_FILE = None
    CURSOR_UP = "\033[A"
    CURSOR_DOWN = "\n"

    ACTION_FPS = 60
    ACTION_WAIT_TIME = 1 / ACTION_FPS

    DISPLAY_FPS = 60
    DISPLAY_WAIT_TIME = 1 / DISPLAY_FPS

    # Disables all sounds in the game - for compatibility purposes
    SILENT = False

    # Makes game very easy for debug purposes
    EASY = False

    # Setting this to False means exiting the game
    GAME_ON = True


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--logging", type=str, default=None)
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--easy", action="store_true")
    parser.add_argument("--silent", action="store_true")
    parser.add_argument("--dont-block-keys", action="store_true")
    args = parser.parse_args()

    FLAGS.LOGGING_FILE = args.logging
    FLAGS.silent = args.silent
    FLAGS.easy = args.easy
    return args


def log_to_file(*msg, **kwds):
    if isinstance(FLAGS.LOGGING_FILE, str):
        with open(FLAGS.LOGGING_FILE, "a") as f:
            print(*msg, **kwds, file=f)
