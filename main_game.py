from __future__ import annotations
# 3rd party modules
import ctypes
import gzip
import pickle
import random

import pygame
import tcod
import tcod.map

import assets
import camera
import config
# gamefiles
import constants
import game_map
import generator
import menu
import monster_gen
import render
from object_game import Game
from ui import Textfield, GuiContainer, FillBar


#     _______.___________..______       __    __    ______ .___________.
#    /       |           ||   _  \     |  |  |  |  /      ||           |
#   |   (----`---|  |----`|  |_)  |    |  |  |  | |  ,----'`---|  |----`
#    \   \       |  |     |      /     |  |  |  | |  |         |  |     
# .----)   |      |  |     |  |\  \----.|  `--'  | |  `----.    |  |
# |_______/       |__|     | _| `._____| \______/   \______|    |__|


class Preferences:
    def __init__(self):
        self.vol_sound = .5
        self.vol_music = .25




#  o         o   __o__
# <|>       <|>    |
# / \       / \   / \
# \o/       \o/   \o/
#  |         |     |
# < >       < >   < >
#  \         /     |
#   o       o      o
#   <\__ __/>    __|>_


#  _______      ___      .___  ___.  _______
# /  _____|    /   \     |   \/   | |   ____|
# |  |  __     /  ^  \    |  \  /  | |  |__
# |  | |_ |   /  /_\  \   |  |\/|  | |   __|
# |  |__| |  /  _____  \  |  |  |  | |  |____
# \______| /__/     \__\ |__|  |__| |_______|


def invoke_command(command):
    arguments = command.split()
    for c in arguments:
        print(c)
    if command[0] == "gen_dog":
        config.GAME.current_objects.append(monster_gen.gen_dog_dog(((int(arguments[1]), int(arguments[2])))))
    elif command[0] == "gen_item":
        generator.gen_item((int(arguments[1]), int(arguments[2])))


def game_main_loop():
    game_quit = False

    player_action = "no-action"

    while not game_quit:

        player_action = game_handle_keys(config.PLAYER)
        if player_action != "player autoexplored":
            config.AUTO_EXPLORING = False


        game_map.calculate_fov()

        if player_action == "QUIT":
            game_exit()

        for obj in config.GAME.current_objects:
            if obj.ai:
                if player_action != "no-action" and player_action != "console":
                    obj.ai.take_turn()
            if obj.structure:
                obj.structure.update()

        if config.PLAYER.state == "STATUS_DEAD" or config.PLAYER.state == "STATUS_WIN":
            game_quit = True

        # draw the game
        render.draw_game()
        config.GUI.update(None)
        config.GUI.draw()


        # update the display
        pygame.display.flip()

        config.CLOCK.tick(constants.GAME_FPS)


def game_initialize():
    """Das hier startet Pygame und das Hauptfenster"""

    # makes window start at top left corner
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "30,30"
    # disable scaling of windows
    ctypes.windll.user32.SetProcessDPIAware()

    # initialize Pygame
    pygame.init()
    pygame.display.set_caption("Roguelike")

    pygame.key.set_repeat(50, 100)

    try:
        preferences_load()
    except:
        config.PREFERENCES = Preferences()

    tcod.namegen_parse("data/namegen/jice_celtic.cfg")

    # looks for resolution of the display of the user

    config.SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH, constants.CAMERA_HEIGHT))

    config.SURFACE_MAP = pygame.Surface(
        (constants.MAP_WIDTH * constants.CELL_WIDTH, constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    config.ASSETS = assets.Assets()
    config.CAMERA = camera.Camera()

    config.CLOCK = pygame.time.Clock()

    # Random Engine
    config.RANDOM_ENGINE = random.SystemRandom()

    config.FOV_CALCULATE = True

    config.CONSOLE = Textfield(
        config.SURFACE_MAIN, pygame.Rect(5, constants.CAMERA_HEIGHT - 30, constants.CAMERA_WIDTH / 1.2, 25), "console",
        constants.COLOR_GREY,
        constants.COLOR_WHITE, constants.COLOR_YELLOW_DARK_GOLD, auto_active=False, focus_key=pygame.K_o
    )

    config.PLAYER = generator.gen_player((0,0), "dieter")

    health_bar = FillBar(config.SURFACE_MAIN, pygame.Rect(0,0,constants.CAMERA_WIDTH,30), "health_bar",
                         constants.COLOR_RED_LIGHT, constants.COLOR_WHITE, "Health", config.PLAYER.creature.maxhp,
                         constants.COLOR_BLACK)

    config.GUI = GuiContainer(config.SURFACE_MAIN, pygame.Rect(0,0,0,0), "GUI", health_bar)





def game_handle_keys(player):
    # get player input
    keys_list = pygame.key.get_pressed()
    events_list = pygame.event.get()

    # Check for mid key
    MOD_KEY = (keys_list[pygame.K_RSHIFT] or keys_list[pygame.K_LSHIFT])

    # process input

    for event in events_list:

        if config.CONSOLE.active:
            if config.CONSOLE.react(event):
                command = config.CONSOLE.text_ready
                invoke_command(command)
            return "console"
        if config.CONSOLE.update_activate(event):
            return "console"
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "QUIT"

            if event.key in constants.MOVEMENT_DICT.keys():
                dx,dy = constants.MOVEMENT_DICT[event.key]
                player.move(dx,dy)
                config.FOV_CALCULATE = True
                return "player moved"

            if event.key == pygame.K_a:
                menu.debug_tile_select_pathing()
                return "debug"


            if event.key == pygame.K_g:
                objects_at_player = game_map.objects_at_coords(config.PLAYER.x, config.PLAYER.y)

                for obj in objects_at_player:
                    if obj.item:
                        print(obj.name_object)
                        obj.item.pick_up(config.PLAYER)
                return "picked up"

            if event.key == pygame.K_d:
                if len(player.container.inventory) > 0:
                    player.container.inventory[-1].item.drop(config.PLAYER.x, config.PLAYER.y)
                return "drop"

            if event.key == pygame.K_p:
                config.GAME.game_message("Game resumed", constants.COLOR_WHITE)
                menu.menu_pause()
                return "pause"

            if event.key == pygame.K_i:
                menu.menu_inventory()
                return "inventory"

            if event.key == pygame.K_l:
                menu.menu_tile_select()
                return "tile select"


            if event.key == pygame.K_m:
                generator.gen_and_append_enemy((player.x, player.y))
                return "debug"

            if event.key == pygame.K_x:
                menu.debug_tile_select()
                return "debug"

            if event.key == pygame.K_s:
                config.GAME.transition_next()
                return "debug"

            if event.key == pygame.K_b:
                game_save(display_message=True)
                game_load()
                return "debug"

            if MOD_KEY and event.key == pygame.K_PERIOD:
                list_of_objs = game_map.objects_at_coords(config.PLAYER.x, config.PLAYER.y)
                for obj in list_of_objs:
                    if obj.structure:
                        obj.structure.use()
                return "used"

            if event.key == pygame.K_BACKQUOTE:
                game_map.start_auto_explore()



    if config.AUTO_EXPLORING:

        x,y = next(config.GAME.auto_explore_path, (0,0))

        config.AUTO_EXPLORING = game_map.check_contine_autoexplore()
        if not config.AUTO_EXPLORING:
            return "stopped autoexploring"
        if (x,y) == (0,0):
            if game_map.autoexplore_new_goal():
                 x, y = next(config.GAME.auto_explore_path, (0, 0))
            else:
                return "stopped autoexploring"



        player.move_towards_point(x,y)
        config.FOV_CALCULATE = True
        return "player autoexplored"





    return "no-action"


def game_new(player_name="Player"):

    # starts a nre game and map
    config.GAME = Game()
    config.PLAYER = generator.gen_player((0, 0), player_name=player_name)
    config.GAME.current_objects.append(config.PLAYER)

    game_map.place_objects(config.GAME.current_rooms)


def game_exit():
    game_save()

    # quit the game
    pygame.quit()
    exit()


def game_save(display_message=False):
    if display_message:
        config.GAME.game_message("Saved Game", constants.COLOR_WHITE)

    for obj in config.GAME.current_objects:
        obj.animation_destroy()

    with gzip.open("data/userdata/savegame", "w+b") as file:
        pickle.dump([config.GAME, config.PLAYER], file)


def game_load():
    with gzip.open("data/userdata/savegame", "rb") as file:
        config.GAME, config.PLAYER = pickle.load(file)

    for obj in config.GAME.current_objects:
        obj.animation_init()

    game_map.make_fov(config.GAME.current_map)
    config.FOV_CALCULATE = True
    game_map.calculate_fov()


def preferences_save():
    with gzip.open("data/userdata/pref", "wb") as file:
        pickle.dump(config.PREFERENCES, file)


def preferences_load():
    with gzip.open("data/userdata/pref", "rb") as file:
        config.PREFERENCES = pickle.load(file)


if __name__ == '__main__':
    config.PLAYER = None
    game_initialize()
    config.MAIN_MENU = menu.MainMenu(game_exit, game_load, game_new, game_main_loop, preferences_save)
    config.MAIN_MENU.show_menu()

#              .7
#            .'/
#           / /
#          / /
#         / /
#        / /
#       / /
#      / /
#     / /         
#    / /          
#  __|/
# ,-\__\
# |f-"Y\|
# \()7L/
# cgD                            __ _
# |\(                          .'  Y '>,
#  \ \                        / _   _   \
#   \\\                       )(_) (_)(|}
#    \\\                      {  4A   } /
#     \\\                      \uLuJJ/\l
#      \\\                     |3    p)/
#       \\\___ __________      /nnm_n//
#       c7___-__,__-)\,__)(".  \_>-<_/D
#                  //V     \_"-._.__G G_c__.-__<"/ ( \
#                         <"-._>__-,G_.___)\   \7\
#                        ("-.__.| \"<.__.-" )   \ \
#                        |"-.__"\  |"-.__.-".\   \ \
#                        ("-.__"". \"-.__.-".|    \_\
#                        \"-.__""|!|"-.__.-".)     \ \
#                         "-.__""\_|"-.__.-"./      \ l
#                          ".__""">G>-.__.-">       .--,_
#                              ""  G
