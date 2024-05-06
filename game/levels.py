from .common import FLAGS
from .objects import GoalObject, HeroObject, VisibleObject, World
from .sounds import SoundManager
from .sprites import SpriteManager

sprite_manager = SpriteManager()
sound_manager = SoundManager()


def load_level_start_sound():
    sound_manager.play("start")


def level1():
    world = World()
    hero = HeroObject(
        0,
        0,
        sprites={"idle": sprite_manager.get("hero"), "jump": sprite_manager.get("hero_jump")},
        control_keys="wsad",
        jump_height=20,
        jump_sound="hero_jump",
    )
    world.add_object(hero)

    clouds = [
        (10, 100),
        (40, 130),
        (30, 180),
        (20, 210),
        (30, 240),
        (20, 270),
        (10, 300),
    ]

    for y, x in clouds:
        world.add_object(VisibleObject(y, x, sprite=sprite_manager.get("cloud")))

    medium_islands = [
        (40, 0),
        (60, 60),
        (80, 90),
        (70, 120),
        (60, 390),
        (50, 180),
        (60, 210),
        (70, 240),
        (80, 270),
        (60, 380),
    ]

    for y, x in medium_islands:
        world.add_object(VisibleObject(y, x, sprite=sprite_manager.get("island_medium")))

    large_islands = [
        (50, 270),
        (60, 30),
        (70, 460),
        (80, 520),
    ]

    for y, x in large_islands:
        world.add_object(VisibleObject(y, x, sprite=sprite_manager.get("island_large")))

    small_islands = [
        (50, 355),
        (60, 150),
        (40, 310),
    ]

    for y, x in small_islands:
        world.add_object(VisibleObject(y, x, sprite=sprite_manager.get("island_small")))

    goal = GoalObject(65, 537, sprite=sprite_manager.get("goal"))
    world.add_object(goal)
    if FLAGS.easy:
        goal = GoalObject(20, 10, sprite=sprite_manager.get("goal"))
        world.add_object(goal)
    load_level_start_sound()
    return world, hero


def level2():
    world = World()
    hero = HeroObject(
        10,
        0,
        sprites={"idle": sprite_manager.get("hero"), "jump": sprite_manager.get("hero_jump")},
        control_keys="wsad",
        jump_height=20,
        jump_sound="hero_jump",
    )
    world.add_object(hero)

    hero2 = HeroObject(
        0,
        0,
        sprites={"idle": sprite_manager.get("hero2"), "jump": sprite_manager.get("hero2_jump")},
        control_keys="ikjl",
        jump_height=20,
        jump_sound="hero_jump",
    )
    world.add_object(hero2)

    clouds = [
        (10, 100),
        (40, 130),
        (30, 180),
        (20, 210),
        (30, 240),
        (20, 270),
        (10, 300),
    ]

    for y, x in clouds:
        world.add_object(VisibleObject(y, x, sprite=sprite_manager.get("cloud")))

    medium_islands = [
        (40, 0),
        (60, 60),
        (80, 90),
        (70, 120),
        (60, 390),
        (50, 180),
        (60, 210),
        (70, 240),
        (80, 270),
        (60, 380),
    ]

    for y, x in medium_islands:
        world.add_object(VisibleObject(y, x, sprite=sprite_manager.get("island_medium")))

    large_islands = [
        (50, 270),
        (60, 30),
        (70, 460),
        (80, 520),
    ]

    for y, x in large_islands:
        world.add_object(VisibleObject(y, x, sprite=sprite_manager.get("island_large")))

    small_islands = [
        (50, 355),
        (60, 150),
        (40, 310),
    ]

    for y, x in small_islands:
        world.add_object(VisibleObject(y, x, sprite=sprite_manager.get("island_small")))

    goal = GoalObject(65, 537, sprite=sprite_manager.get("goal"))
    world.add_object(goal)
    if FLAGS.easy:
        goal = GoalObject(20, 10, sprite=sprite_manager.get("goal"))
        world.add_object(goal)
    load_level_start_sound()
    return world, (hero, hero2)


def level_game_clear():
    world = World()
    text = VisibleObject(0, 0, sprite=sprite_manager.get("game_clear"))
    world.add_object(text)
    return world, text


levels = [level1, level2, level_game_clear]
