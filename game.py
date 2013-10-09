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
GAME_WIDTH = 10
GAME_HEIGHT = 10
GAME_CYCLES = 6

#### Put class definitions here ####
class Selector(GameElement):
    IMAGE = "Selector"
    SOLID = False
    TILE = True


class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Gem(GameElement):
    IMAGE = None
    SOLID = False

    def __init__(self):
        self.NAME = ""
        self.POINT_VAL = 100

    def interact(self, player):
        player.points += self.POINT_VAL
        GAME_BOARD.draw_msg3("%s just aquired a %s! %s has +%d points!" % (player.name, self.NAME, player.name, self.POINT_VAL))
        GAME_BOARD.draw_msg6("Points:    %d        %d" % (PLAYER.points, PLAYER2.points))  

class BlueGem(Gem):
    def __init__(self):
        self.IMAGE = "BlueGem"
        self.POINT_VAL = 100
        self.NAME = "blue gem"

class OrangeGem(Gem):
    def __init__(self):
        self.IMAGE = "OrangeGem"
        self.POINT_VAL = 150
        self.NAME = "orange gem"

class Star(Gem):
    IMAGE = "Star"
    def interact(self, player):
        if player == PLAYER:
            player.points += 300
            GAME_BOARD.draw_msg3("%s just aquired a star! %s +300 points!" % (player.name, player.name))
            GAME_BOARD.draw_msg6("Points:    %d        %d" % (PLAYER.points, PLAYER2.points))  

class Heart(Gem):
    IMAGE = "Heart"
    def interact(self, player):
        if player == PLAYER2:
            player.points += 300
            GAME_BOARD.draw_msg3("%s just aquired a heart! %s +300 points!" % (player.name, player.name))
            GAME_BOARD.draw_msg6("Points:    %d        %d" % (PLAYER.points, PLAYER2.points))  

class Character(GameElement):
    SOLID = True
    moves = SQ_MOVES

    def __init__(self):
        GameElement.__init__(self)
        self.points = 0
        self.inventory = []
        self.IMAGE = "Horns"
        self.name = "Horns"
        self.selector_image = "Yellow_selector"

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

    def make_trail(self, x, y, nextx, nexty):
        if GAME_BOARD.get_el(nextx, nexty):
            element_img = GAME_BOARD.get_el(nextx, nexty).IMAGE
        else:
            element_img = None

        if element_img == "Pink" or element_img == "Yellow_selector":
            selector = Selector()
            if len(self.inventory) == 0:
                selector.IMAGE = self.selector_image
            else:
                selector.IMAGE = self.inventory.pop()

            GAME_BOARD.register(selector)
            GAME_BOARD.set_el(x, y, selector)
            self.inventory.append(element_img)
        else:
            self.points += 25
            selector = Selector()
            if len(self.inventory) == 0:
                selector.IMAGE = self.selector_image
            else:
                selector.IMAGE = self.inventory.pop()
            GAME_BOARD.register(selector)
            GAME_BOARD.set_el(x, y, selector)

        GAME_BOARD.draw_msg6("Points:    %d        %d" % (PLAYER.points, PLAYER2.points))

####   End class definitions    ####

def initialize():
    characterCreation()
    rockCreation()
    gemCreation(6, 10)

    GAME_BOARD.draw_msg4("%s  %s" % (PLAYER.name, PLAYER2.name))
    GAME_BOARD.draw_msg5("Moves:    %d        %d" % (PLAYER.moves, PLAYER2.moves))
    GAME_BOARD.draw_msg6("Points:    %d        %d" % (PLAYER.points, PLAYER2.points))
    GAME_BOARD.draw_msg1("Stars vs. Hearts")

def characterCreation():
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    rand_x = random.randint(0, GAME_WIDTH - 1)
    rand_y = random.randint(0, GAME_HEIGHT - 1)
    GAME_BOARD.set_el(rand_x,  rand_y, PLAYER)

    global PLAYER2
    PLAYER2 = Character()
    PLAYER2.IMAGE = "Girl"
    PLAYER2.name = "Girl"
    PLAYER2.moves = 0
    PLAYER2.selector_image = "Pink"
    GAME_BOARD.register(PLAYER2)
    while True:
        rand_x = random.randint(0, GAME_WIDTH - 1)
        rand_y = random.randint(0, GAME_HEIGHT - 1)
        if not GAME_BOARD.get_el(rand_x, rand_y):
            GAME_BOARD.set_el(rand_x, rand_y, PLAYER2)
            break

def rockCreation():
    rock_positions = []
    num_rocks = random.randint(14, 20)
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


def gemCreation(min, max):
    gem_type = [BlueGem, Star, Heart, OrangeGem, BlueGem, OrangeGem]

    gem_positions = []
    num_gem = random.randint(min, max)
    for x in range(num_gem):
        rand_x = random.randint(0, GAME_WIDTH - 1)
        rand_y = random.randint(0, GAME_HEIGHT - 1)
        if not GAME_BOARD.get_el(rand_x, rand_y):
            gem_positions.append((rand_x, rand_y))

    gems = []

    for pos in gem_positions:
        gem = gem_type[random.randint(0, 5)]()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        gems.append(gem)

def keyboard_handler():
    GAME_BOARD.draw_msg5("Moves:    %d        %d" % (PLAYER.moves, PLAYER2.moves))
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
    if KEYBOARD[key.ENTER]:
        changeCharacter(PLAYER, PLAYER.x, PLAYER.y)
    if KEYBOARD[key.SPACE]:
        changeCharacter(PLAYER2, PLAYER2.x, PLAYER2.y)


    if direction and player == 1 and PLAYER.moves > 0:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x < (GAME_WIDTH) and next_x >= 0 and next_y < (GAME_HEIGHT) and next_y >= 0:
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER)

            if existing_el is None or not existing_el.SOLID:

                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                PLAYER.moves -= 1
                PLAYER.make_trail(PLAYER.x, PLAYER.y, next_x, next_y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
                GAME_BOARD.draw_msg2("%s's turn. You have %d moves remaining." % (PLAYER.name, PLAYER.moves))  
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
                PLAYER2.make_trail(PLAYER2.x, PLAYER2.y, next_x, next_y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER2)
                PLAYER2.moves -= 1
                GAME_BOARD.draw_msg2("%s's turn. You have %d moves remaining." % (PLAYER2.name, PLAYER2.moves))  
                if PLAYER2.moves == 0:
                    game_count()

def game_count():
    global GAME_CYCLES
    GAME_CYCLES -= 1
    if GAME_CYCLES % 2 == 0:
        gemCreation(4, 8)
    if GAME_CYCLES == 0:
        if PLAYER.points > PLAYER2.points:
            GAME_BOARD.draw_msg7("Congratulations %s," % PLAYER.name)
            GAME_BOARD.draw_msg8("You win!")
        elif PLAYER.points < PLAYER2.points: 
            GAME_BOARD.draw_msg7("Congratulations %s," % PLAYER2.name)
            GAME_BOARD.draw_msg8("You win!")
        else:
            GAME_BOARD.draw_msg7("Tied! Good job everyone.")
        PLAYER.moves == 0
    else:
        PLAYER.moves = SQ_MOVES

def changeCharacter(player, x, y):
    characters = ["Princess", "Boy", "Cat", "Girl", "Horns"]
    index = random.randint(0,4)
    player.IMAGE = characters[index]
    player.name= characters[index]
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(x, y, player)
    GAME_BOARD.draw_msg4("%s  %s" % (PLAYER.name, PLAYER2.name))