from pynput import keyboard

CALLBACKS_ON_PRESS = []
CALLBACKS_ON_RELEASE = []

PRESSED_NOW = {}


def is_pressed(key):
    if isinstance(key, str):
        assert len(key) == 1
        key = keyboard.KeyCode(char=key)

    return PRESSED_NOW.get(key, False)


def global_key_listener_on_press(key):
    global PRESSED_NOW
    PRESSED_NOW[key] = True

    for callback in CALLBACKS_ON_PRESS:
        callback(key)


def global_key_listener_on_release(key):
    global PRESSED_NOW
    PRESSED_NOW[key] = False

    for callback in CALLBACKS_ON_RELEASE:
        callback(key)


def add_press_callback(callback):
    CALLBACKS_ON_PRESS.append(callback)


def add_release_callback(callback):
    CALLBACKS_ON_RELEASE.append(callback)


def start_keyboard_listener(supress_keys):
    listener = keyboard.Listener(
        on_press=global_key_listener_on_press,
        on_release=global_key_listener_on_release,
        suppress=supress_keys,
    )
    listener.start()
