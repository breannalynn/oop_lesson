import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
PLAYER2 = None
######################

SQ_MOVES = 4
GAME_WIDTH = 12
GAME_HEIGHT = 10

#### Put class definitions here ####
class Selector(GameElement):
    IMAGE = "Selector"
    SOLID = False

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just aquired a gem! You have %d items!" % (len(player.inventory)))  

class OrangeGem(Gem):
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("ORANGE GEM!!")

class Character(GameElement):
    SOLID = True
    IMAGE = "Horns"
    moves = SQ_MOVES
    name = "Horns"
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y -1)
        elif direction == "down":
            return (self.x, self.y + 1)
        elif direction == "left":
            return (self.x -1 , self.y)
        elif direction == "right":
            return (self.x + 1, self.y)
        elif direction == "teleport":
            return (random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1))
        return None

####   End class definitions    ####

def initialize():
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 4, PLAYER)

    global PLAYER2
    PLAYER2 = Character()
    PLAYER2.IMAGE = "Girl"
    PLAYER2.name = "Girl"
    PLAYER2.moves = 0
    GAME_BOARD.register(PLAYER2)
    GAME_BOARD.set_el(11, 5, PLAYER2)

    rock_positions = []
    num_rocks = random.randint(6, 10)
    for x in range(num_rocks):
        rand_x = random.randint(0, GAME_WIDTH - 1)
        rand_y = random.randint(0, GAME_HEIGHT - 1)
        if not GAME_BOARD.get_el(rand_x, rand_y):
            rock_positions.append((rand_x, rand_y))

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    # gem = Gem()
    # GAME_BOARD.register(gem)
    # GAME_BOARD.set_el(3, 1, gem)

    # gem2 = OrangeGem()
    # gem2.IMAGE = "OrangeGem"
    # GAME_BOARD.register(gem2)
    # GAME_BOARD.set_el(1, 1, gem2)

    GAME_BOARD.draw_rightmessage("%s: %d  %s: %d" % (PLAYER.name, PLAYER.moves, PLAYER2.name, PLAYER2.moves))
    GAME_BOARD.draw_bottomrightmsg("Points")
    GAME_BOARD.draw_msg("Game Name Here")
   

def keyboard_handler():
    direction = None
    player = None

    if KEYBOARD[key.UP]:
        direction = "up"
        player = 1
    if KEYBOARD[key.DOWN]:
        direction = "down"
        player = 1
    if KEYBOARD[key.LEFT]:
        direction = "left"
        player = 1
    if KEYBOARD[key.RIGHT]:
        direction = "right"
        player = 1
    if KEYBOARD[key.L]:
        direction = "teleport"
        player = 1

    if KEYBOARD[key.W]:
        direction = "up"
        player = 2
    if KEYBOARD[key.S]:
        direction = "down"
        player = 2
    if KEYBOARD[key.A]:
        direction = "left"
        player = 2
    if KEYBOARD[key.D]:
        direction = "right"
        player = 2
    if KEYBOARD[key.T]:
        direction = "teleport"     
        player = 2       


    if direction and player == 1 and PLAYER.moves > 0:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x < (GAME_WIDTH) and next_x >= 0 and next_y < (GAME_HEIGHT) and next_y >= 0:
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER)

            if existing_el is None or not existing_el.SOLID:
                PLAYER.moves -= 1
                # GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                selector = Selector()
                selector.IMAGE = "Yellow_selector"
                GAME_BOARD.register(selector)
                GAME_BOARD.set_el(PLAYER.x, PLAYER.y, selector)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
                GAME_BOARD.draw_bottommsg("%s's turn. You have %d moves remaining." % (PLAYER.name, PLAYER.moves))  
                if PLAYER.moves == 0:
                    PLAYER2.moves = SQ_MOVES

    if direction and player == 2 and PLAYER2.moves > 0:
        next_location = PLAYER2.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x < (GAME_WIDTH) and next_x >= 0 and next_y < (GAME_HEIGHT) and next_y >= 0:
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER2)

            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER2.x, PLAYER2.y)
                selector = Selector()
                selector.IMAGE = "Pink_selector"
                GAME_BOARD.register(selector)
                GAME_BOARD.set_el(PLAYER2.x, PLAYER2.y, selector)
                GAME_BOARD.set_el(next_x, next_y, PLAYER2)
                PLAYER2.moves -= 1
                GAME_BOARD.draw_bottommsg("%s's turn. You have %d moves remaining." % (PLAYER2.name, PLAYER2.moves))  
                if PLAYER2.moves == 0:
                    PLAYER.moves = SQ_MOVES