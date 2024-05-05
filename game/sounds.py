import os
from pathlib import Path

import simpleaudio

SOUND_LOCATION = "sounds/"


class SoundManager:
    def __init__(self, location=SOUND_LOCATION):
        self.sound_files = os.listdir(location)
        self.sounds = {}

        for name in self.sound_files:
            path = os.path.join(location, name)
            path = Path(path).absolute()
            self.sounds[Path(name).stem] = path

    def play(self, name):
        with open(self.sounds[name], "rb") as f:
            simpleaudio.WaveObject.from_wave_file(f).play()


if __name__ == "__main__":
    # For testing - this will not be executed on import
    manager = SoundManager()

    print(f"Available sprites:")
    for name in manager.sounds:
        print(f"* {name}")
        manager.play(name)
