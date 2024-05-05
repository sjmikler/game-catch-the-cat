import os
import sys
import time

from pynput import keyboard

from .camera import Camera
from .common import FLAGS, parse_command_line_arguments
from .controls import add_press_callback, is_pressed, start_keyboard_listener
from .levels import levels

CURRENT_LEVEL = 0
RESTART = False


def monitor_exit_game():
    def _exit_game(key):
        if key == keyboard.Key.esc:
            game_stop()

    add_press_callback(_exit_game)

    def _reset_game(key):
        global RESTART
        if key == keyboard.KeyCode.from_char("r"):
            RESTART = True

    add_press_callback(_reset_game)

    def _next_level(key):
        global RESTART
        global CURRENT_LEVEL
        if is_pressed("q") and is_pressed("p"):
            CURRENT_LEVEL += 1
            RESTART = True

    add_press_callback(_next_level)


def game_stop():
    FLAGS.GAME_ON = False
    time.sleep(0.1)
    assert not camera.display_thread.is_alive()
    assert not camera.world.move_objects_thread.is_alive()
    del camera.world


def game_start():
    FLAGS.GAME_ON = True

    world, hero = levels[CURRENT_LEVEL](easy=args.easy)
    camera.set_world(world)
    camera.follow(hero)
    camera.launch_display_thread()


sys.stderr = open("error.log", "w")


if __name__ == "__main__":
    args = parse_command_line_arguments()

    instructions = [
        "WASD and IKJL to move the characters",
        "ARROWS to move the camera",
        "R to reset",
        "ESC to exit",
    ]

    arrows = [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]

    camera_width = args.width or os.get_terminal_size().columns - 1
    camera_height = args.height or os.get_terminal_size().lines - 1

    camera = Camera(
        camera_height,
        camera_width,
        control_keys=arrows,
        instructions=" | ".join(instructions),
    )
    start_keyboard_listener(supress_keys=not args.dont_block_keys)

    monitor_exit_game()

    world_finished = False

    world, hero = levels[CURRENT_LEVEL](easy=args.easy)
    camera.set_world(world)
    camera.follow(hero)
    camera.launch_display_thread()
    while True:
        if not FLAGS.GAME_ON:
            break

        if camera.world.world_finished:
            CURRENT_LEVEL += 1

        if camera.world.world_finished or RESTART:
            game_stop()
            game_start()
            RESTART = False
        time.sleep(0.1)
