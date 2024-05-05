import threading
import time

from .common import FLAGS
from .controls import is_pressed
from .sounds import SoundManager

sound_manager = SoundManager()


class World:
    def __init__(self):
        self.objects = []
        self.movable_objects = []
        self.world_finished = False

        self.move_objects_thread = None
        self.tick = 0

        self.launch_move_object_thread()

    def add_object(self, object):
        self.objects.append(object)

    def move_objects(self):
        self.tick += 1
        is_moving_y = self.tick % 2

        num_hero_finished = 0
        num_hero_total = 0

        for obj in self.objects:
            next_world_y = obj.world_y
            next_world_x = obj.world_x
            obj_moved = False

            if isinstance(obj, HeroObject):
                num_hero_total += 1

                if obj.hero_finished:
                    num_hero_finished += 1

            if isinstance(obj, MovableObject):
                obj.maybe_move(self.tick)
                next_world_y = obj.world_y + obj.move_y
                next_world_x = obj.world_x + obj.move_x
                obj_moved = True

            if isinstance(obj, GravityObject):
                next_world_y = obj.world_y + 1
                obj_moved = True

            if isinstance(obj, JumpingObject):
                obj.maybe_jump(self.tick)

                if obj.jump_ticks > 0:
                    next_world_y = obj.world_y - 1
                    obj.jump_ticks -= 1
                    obj_moved = True

            if isinstance(obj, VisibleObject) and obj_moved:
                collided = False

                if obj.can_move(next_world_y, obj.world_x, colliders=self.objects):
                    obj.world_y = next_world_y
                else:
                    collided = True

                if obj.can_move(obj.world_y, next_world_x, colliders=self.objects):
                    obj.world_x = next_world_x
                else:
                    collided = True

                if isinstance(obj, AnimatedObject):
                    if collided:
                        obj.set_sprite("idle")
                    else:
                        obj.set_sprite("jump")

                if collided and isinstance(obj, JumpingObject):
                    obj.can_jump = True
                    obj.jump_ticks = 0
                else:
                    obj.can_jump = False
            else:
                obj.world_y = next_world_y
                obj.world_x = next_world_x

        if num_hero_finished == num_hero_total and num_hero_total > 0:
            if self.world_finished is False:
                sound_manager.play("level_finished")
                time.sleep(1.0)
            self.world_finished = True

    def launch_move_object_thread(self):
        def _thread():
            while FLAGS.GAME_ON:
                t0 = time.time()
                self.move_objects()
                remaining_wait_time = FLAGS.ACTION_WAIT_TIME - (time.time() - t0)
                time.sleep(max(0.0, remaining_wait_time))

        self.move_objects_thread = threading.Thread(target=_thread)
        self.move_objects_thread.start()


class GameObject:
    def __init__(self, y, x):
        self.world_y = y
        self.world_x = x


class VisibleObject(GameObject):
    def __init__(self, y, x, sprite, z_index=1):
        GameObject.__init__(self, y, x)

        self.sprite = sprite
        self.z_index = z_index
        self.height = len(sprite)
        self.width = len(sprite[0])

    def get_pixel_at(self, py, px):
        y = py - self.world_y
        x = px - self.world_x
        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            return " "
        return self.sprite[y][x]

    def can_move(self, world_y, world_x, colliders):
        # Check if the object can move to the new position without collision

        for sprite_y in range(self.height):
            for sprite_x in range(self.width):
                if self.sprite[sprite_y][sprite_x] == " ":
                    continue

                for obj in colliders:
                    dist_x = abs(obj.world_x - world_x)
                    if dist_x > self.width + obj.width:
                        continue
                    dist_y = abs(obj.world_y - world_y)
                    if dist_y > self.height + obj.height:
                        continue

                    if not isinstance(obj, VisibleObject):
                        continue
                    if obj == self:
                        continue
                    if obj.get_pixel_at(world_y + sprite_y, world_x + sprite_x) != " ":
                        if isinstance(self, HeroObject) and isinstance(obj, GoalObject):
                            if not self.hero_finished:
                                sound_manager.play("hero_finished")
                                time.sleep(0.5)
                            self.hero_finished = True
                        return False
        return True


class GoalObject(VisibleObject):
    pass


class AnimatedObject(VisibleObject):
    def __init__(self, y, x, sprites: dict, z_index=1):
        VisibleObject.__init__(self, y, x, sprite=sprites["idle"], z_index=z_index)
        self.sprites = sprites

    def set_sprite(self, key):
        self.sprite = self.sprites[key]


class MovableObject(GameObject):
    def __init__(self, y, x, control_keys="wsad"):
        GameObject.__init__(self, y, x)
        self.move_y = 0
        self.move_x = 0

        assert len(control_keys) == 4, "Control keys must be a list of 4 keys"
        self.control_keys = control_keys

    def maybe_move(self, game_tick):
        self.move_y = 0
        self.move_x = 0

        if is_pressed(self.control_keys[0]):
            self.move_y = -1
        if is_pressed(self.control_keys[1]):
            self.move_y = 1
        if is_pressed(self.control_keys[2]):
            self.move_x = -1
        if is_pressed(self.control_keys[3]):
            self.move_x = 1

        new_y = self.world_y + self.move_y
        new_x = self.world_x + self.move_x


class JumpingObject(MovableObject):
    def __init__(self, y, x, control_keys, jump_height, jump_sound=None):
        MovableObject.__init__(self, y, x, control_keys=control_keys)
        self.jump_ticks = 0
        self.can_jump = False
        self.jump_height = jump_height
        self.jump_sound = jump_sound
        self.last_jump_tick = 0

    def maybe_jump(self, game_tick):
        if self.can_jump and is_pressed(self.control_keys[0]):
            if game_tick - self.last_jump_tick < 10:
                return

            self.jump_ticks = self.jump_height
            self.can_jump = False
            self.last_jump_tick = game_tick

            if self.jump_sound:
                sound_manager.play(self.jump_sound)


class GravityObject(GameObject):
    def __init__(self, y, x):
        GameObject.__init__(self, y, x)


class HeroObject(GravityObject, JumpingObject, AnimatedObject):
    def __init__(self, y, x, sprites, control_keys, jump_height, jump_sound, z_index=1):
        GravityObject.__init__(self, y, x)
        JumpingObject.__init__(self, y, x, control_keys=control_keys, jump_height=jump_height, jump_sound=jump_sound)
        AnimatedObject.__init__(self, y, x, sprites=sprites, z_index=z_index)
        self.hero_finished = False
