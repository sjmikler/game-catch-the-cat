import threading
import time

import colorama

from .common import FLAGS
from .objects import GameObject, MovableObject, VisibleObject, World


class Camera(MovableObject):
    def __init__(self, height, width, control_keys, instructions=""):
        super().__init__(0, 0, control_keys=control_keys)
        self.height = height
        self.width = width

        self.BACKGROUND_COLOR = colorama.Back.BLUE
        self.CURSOR_ROW = 0

        self.display_thread = None
        self.follow_object = None
        self.follow_distance_x = int(0.4 * self.width)
        self.follow_distance_y = int(0.4 * self.height)
        self.instructions = instructions

    def move_cursor(self, new_row):
        offset = new_row - self.CURSOR_ROW
        if offset > 0:
            return FLAGS.CURSOR_DOWN * offset
        if offset < 0:
            return FLAGS.CURSOR_UP * (-offset)
        return ""

    def set_world(self, world: World):
        world.add_object(self)
        self.world = world

    def follow(self, object):
        self.follow_object = object

    def get_follow_coordinates(self):
        if isinstance(self.follow_object, VisibleObject):
            return (
                self.follow_object.world_x + self.follow_object.width // 2,
                self.follow_object.world_y + self.follow_object.height // 2,
            )
        elif isinstance(self.follow_object, (list, tuple)):
            x = 0
            y = 0
            n = 0
            for obj in self.follow_object:
                x += obj.world_x + obj.width // 2
                y += obj.world_y + obj.height // 2
                n += 1
            return x // n, y // n
        else:
            raise ValueError("Invalid object to follow")

    def display(self, world):
        if self.follow_object is not None:
            obj_x, obj_y = self.get_follow_coordinates()

            left_edge_distance = obj_x - self.world_x
            if left_edge_distance < self.follow_distance_x:
                self.world_x = obj_x - self.follow_distance_x

            right_edge_distance = self.world_x + self.width - obj_x
            if right_edge_distance < self.follow_distance_x:
                self.world_x = obj_x + self.follow_distance_x - self.width

            top_edge_distance = obj_y - self.world_y
            if top_edge_distance < self.follow_distance_y:
                self.world_y = obj_y - self.follow_distance_y

            bottom_edge_distance = self.world_y + self.height - obj_y
            if bottom_edge_distance < self.follow_distance_y:
                self.world_y = obj_y + self.follow_distance_y - self.height

        # Move cursor to the beginning
        CURSOR_MOVEMENT = self.move_cursor(0)
        ROW_START = self.BACKGROUND_COLOR
        ROW_CLOSE = colorama.Style.RESET_ALL

        camera_view = [[" " for _ in range(self.width)] for _ in range(self.height)]

        visible_objects = [obj for obj in world.objects if isinstance(obj, VisibleObject)]
        for obj in sorted(visible_objects, key=lambda x: -x.z_index):
            for sprite_y, row in enumerate(obj.sprite):
                camera_y = obj.world_y - self.world_y + sprite_y
                if camera_y >= self.height or camera_y < 0:
                    continue
                for px, symbol in enumerate(row):
                    if symbol == " ":
                        continue

                    camera_x = obj.world_x - self.world_x + px
                    if camera_x >= self.width or camera_x < 0:
                        continue
                    assert isinstance(symbol, str) and len(symbol) == 1
                    camera_view[camera_y][camera_x] = symbol

        camera_rows = ["".join(row) for row in camera_view]
        camera_view_str = "\r\n".join(camera_rows)
        camera_view_str = CURSOR_MOVEMENT + camera_view_str

        self.CURSOR_ROW = self.height
        print(ROW_START + camera_view_str + "\r" + self.instructions + ROW_CLOSE)

    def launch_display_thread(self):
        def _thread():
            while FLAGS.GAME_ON:
                t0 = time.time()
                self.display(self.world)

                display_time = time.time() - t0
                remaining_wait_time = FLAGS.DISPLAY_WAIT_TIME - display_time
                # log_to_file(f"Display time: {display_time:.4f} sec")
                time.sleep(max(0.0, remaining_wait_time))

        self.display_thread = threading.Thread(target=_thread)
        self.display_thread.start()
