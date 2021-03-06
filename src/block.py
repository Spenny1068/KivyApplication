import sys
import logging
import random
logging.basicConfig(level=logging.critical)

import kivy
from kivy.uix.widget import Widget
from kivy.core.window import Window

#####    GLOBAL VARIABLES    #####
NUM_BLOCKS = 3 # remember theres 1 extra block not in array above screen
MAX_BLOCKS = 50 # maximum number of blocks allowed on screen
blocks = [] * NUM_BLOCKS # blocks array

#####    ARRAY OF FALLING BLOCKS    #####
class Block(Widget):
    ground = None        # boolean True if block.pos[1] < 0 
    invisible = None     # boolean True if block.pos[1] < -block.size[1]
    spawnBlock = None    # boolean True if block has never had ground = True
    blockCol = None      # boolean True if block has collided with any other widget
    block_bottom = None
    block_right = None

    # each blocks has its own random xpos, fallSpeed
    def __init__(self, *args, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.ground, self.invisible, self.spawnBlock, self.blockCol = False, False, True, False
        self.fallSpeed = 10
        self.inc = 0
        self.findPos()

    #####    UPDATE BLOCKS    #####
    def update(self):

        if (self.fallSpeed != 0):
            self.pos[1] -= self.fallSpeed + self.inc
        self.inc = 0

        if (self.pos[1] > Window.size[1] and self.fallSpeed == 0):
            sys.exit("height limit reached")

        # if block hits ground
        if (self.pos[1] < 0):
            self.fallSpeed = 0 
            self.ground = True

        # if block hits another block
        if (self.blockCol):
            self.fallSpeed = 0

        # if block is completely off screen
        if (self.pos[1] < -self.size[1]):
            self.invisible = True

    # find spawn xpos such that its not inside another block
    def findPos(self):
        self.pos = [random.randint(1, Window.size[0] - self.size[0]), Window.size[1]]

        #logging.info('s.pos[0]: %s s.pos[1]: %s s.size[0]: %s s.size[1]: %s', str(self.pos[0]), str(self.pos[1]), str(self.size[1]), str(self.size[0]))
        x = 0

        # check for collisions. If there is one, reRoll self.pos[0]
        # TODO: Optimize this loop to check only for other blocks with a spawn y value
        while (x < len(blocks)):
            #logging.info('index: %s x: %s y: %s width: %s height: %s', x, blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])
            while(self.blockCollision(blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])):
                #logging.info('%s Block collision with index: ', x)
                self.reRoll()
                x = -1
            x += 1

        #logging.info('index: %s Final position = %s', len(blocks), self.pos[0])
        #logging.info('\n')

    # find a new block self.pos[0]
    def reRoll(self):
        self.pos = [random.randint(1, Window.size[0] - self.size[0]), Window.size[1]]
        #logging.info('reRoll: %s', self.pos[0])
        for x in range(0, len(blocks)):
            self.blockCollision(blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])


    # axis-aligned bounding box collision detection
    def blockCollision(self, x, y, width, height):
        if ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y)):
            return True 

        else:
            return False

    # if block is on ground, it should dissapear only when character is increasing height
    def dissapear(self, speed):
        if (self.ground or self.fallSpeed == 0):
            self.pos[1] -= speed

