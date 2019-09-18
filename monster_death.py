import tcod
from creature import Creature
import death
import constants
import ai
from actor import Actor
import casting
from item import Item
import config


def gen_snake_anaconda(coords):
    x, y = coords

    max_health = tcod.random_get_int(None, 15, 20)
    base_attack = tcod.random_get_int(None, 3, 6)

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=40, base_evasion=0, xp_gained=300,
                            dead_animation=config.ASSETS.S_FLESH_SNAKE,
                            dead_animation_key="S_FLESH_SNAKE"
                            )
    ai_com = ai.AiChase()

    snake = Actor(x, y, "Anaconda", animation_key="A_SNAKE_ANACONDA", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com)

    return snake


def gen_snake_cobra(coords):
    x, y = coords

    max_health = tcod.random_get_int(None, 5, 10)
    base_attack = tcod.random_get_int(None, 1, 3)

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=80, base_evasion=10, xp_gained=300,
                            dead_animation=config.ASSETS.S_FLESH_SNAKE,
                            dead_animation_key="S_FLESH_SNAKE")
    ai_com = ai.AiChase()

    snake = Actor(x, y, "Cobra", animation_key="A_SNAKE_COBRA", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com)

    return snake


def gen_mouse(coords):
    x, y = coords

    max_health = 1
    base_attack = 0

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_evasion=60,
                            dead_animation=config.ASSETS.S_FLESH_EAT,
                            dead_animation_key="S_FLESH_EAT")
    ai_com = ai.AiFlee()

    item_com = Item(use_function=casting.cast_heal, value=2, pickup_text="Rat Carcass")

    mouse = Actor(x, y, "Mouse", animation_key="A_MOUSE_01", depth=constants.DEPTH_CREATURE, creature=creature_com,
                  ai=ai_com, item=item_com)

    return mouse


def gen_slime_small(coords):
    x, y = coords

    max_health = 4
    base_attack = 1
    hit_chance = 70
    doge_value = 0
    xp_granted = 30

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=base_attack,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiChase()

    small_slime = Actor(x, y, "Small slime", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                        creature=creature_com,
                        ai=ai_com)

    return small_slime


def gen_critter_dog(coords):
    x, y = coords

    max_health = 8
    attack = 2
    defence = 1
    hit_chance = 75
    doge_value = 5
    xp_granted = 40

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiChase()

    dog = Actor(x, y, "Dog", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                creature=creature_com,
                ai=ai_com)

    return dog


def gen_pest_snail(coords):
    x, y = coords

    max_health = 5
    attack = 2
    defence = 2
    hit_chance = 70
    doge_value = 10
    xp_granted = 40

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiChase()

    snail = Actor(x, y, "Snail", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                  creature=creature_com,
                  ai=ai_com)

    return snail


def gen_pest_small_spider(coords):
    x, y = coords

    max_health = 10
    attack = 4
    defence = 0
    hit_chance = 70
    doge_value = 10
    xp_granted = 60

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, custom_death=None, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiChase()

    small_spider = Actor(x, y, "Small Spider", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                         creature=creature_com,
                         ai=ai_com)

    return small_spider


def gen_pest_small_scorpion(coords):
    x, y = coords

    max_health = 10
    attack = 4
    defence = 2
    hit_chance = 70
    doge_value = 10
    xp_granted = 70

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, custom_death=None, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiChase()

    small_scorpion = Actor(x, y, "Small Scorpion", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                           creature=creature_com,
                           ai=ai_com)

    return small_scorpion


def gen_pest_worm(coords):
    x, y = coords

    max_health = 12
    attack = 3
    defence = 2
    hit_chance = 85
    doge_value = 15
    xp_granted = 70

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, custom_death=death.death_worm, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiChase()

    worm = Actor(x, y, "Worm", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                 creature=creature_com,
                 ai=ai_com)

    return worm


def pest_gen_flying_snake(coords):
    x, y = coords

    max_health = 15
    attack = 4
    defence = 1
    hit_chance = 85
    doge_value = 25
    xp_granted = 100

    creature_name = tcod.namegen_generate("Celtic female")

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiChase()

    flying_snake = Actor(x, y, "Flying Snake", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                         creature=creature_com,
                         ai=ai_com)

    return flying_snake


def humanoid_goblin(coords):
    x, y = coords

    max_health = 13
    attack = 5
    defence = 1
    hit_chance = 85
    doge_value = 15
    xp_granted = 100

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, custom_death=death.death_humanoid, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiChase()

    goblin = Actor(x, y, "Goblin", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                   creature=creature_com,
                   ai=ai_com)

    return goblin


def misc_monkey(coords):
    x, y = coords

    max_health = 10
    attack = 0
    defence = 0
    hit_chance = 0
    doge_value = 50
    xp_granted = 150

    creature_name = tcod.namegen_generate("Celtic male")

    creature_com = Creature(creature_name, hp=max_health, base_atk=attack,
                            base_def=defence,
                            base_hit_chance=hit_chance, base_evasion=doge_value, xp_gained=xp_granted)
    ai_com = ai.AiFlee()

    monkey = Actor(x, y, "Scared Monkey", animation_key="A_SNAKE_02", depth=constants.DEPTH_CREATURE,
                   creature=creature_com,
                   ai=ai_com)

    return monkey
