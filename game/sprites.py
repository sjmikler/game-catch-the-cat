import os
from pathlib import Path

SPRITE_LOCATION = "sprites/"


class SpriteManager:
    def __init__(self, location=SPRITE_LOCATION):
        self.sprite_files = os.listdir(location)
        self.sprites = {}

        for name in self.sprite_files:
            with open(os.path.join(location, name), encoding="UTF-8") as f:
                sprite_name = Path(name).stem
                sprite = f.read().split("\n")
                sprite = self.add_padding(sprite)
                self.sprites[sprite_name] = sprite

    def add_padding(self, sprite):
        max_length = max([len(row) for row in sprite])
        return [row.ljust(max_length) for row in sprite]

    def get(self, name):
        return self.sprites[name]


if __name__ == "__main__":
    # For testing - this will not be executed on import
    manager = SpriteManager()

    print(f"Available sprites:")
    for name in manager.sprites:
        print(f"* {name}")

        for line in manager.get(name):
            print(">> " + line)
