import os
import time
from pathlib import Path
from threading import Thread

import playsound

SOUND_LOCATION = "sounds/"

LAST_SOUND = 0


def _play(sound):
    playsound.playsound(sound, block=True)


class SoundManager:
    def __init__(self, location=SOUND_LOCATION):
        self.sound_files = os.listdir(location)
        self.sounds = {}

        for name in self.sound_files:
            path = os.path.join(location, name)
            self.sounds[Path(name).stem] = path

    def play(self, name):
        global LAST_SOUND
        t0 = time.time()
        if t0 - LAST_SOUND > 0.1:
            t = Thread(target=_play, args=[self.sounds[name]])
            t.start()
        LAST_SOUND = t0


if __name__ == "__main__":
    # For testing - this will not be executed on import
    manager = SoundManager()

    print(f"Available sprites:")
    for name in manager.sounds:
        print(f"* {name}")
        manager.play(name)
