import kivy
import random
import logging
logging.basicconfig(level=logging.critical)

kivy.require('1.10.1')

from kivy.uix.widget import Widget

#####    GLOBAL VARIABLES    #####
NUM_BLOCKS = 3 #Remember theres 1 extra block not in array above screen
MAX_BLOCKS = 30 #Maximum number of blocks allowed on screen
blocks = [] * NUM_BLOCKS #Blocks array


#####    ARRAY OF FALLING BLOCKS    #####
class Block(Widget):
    ground = None        #boolean True if block.pos[1] < 0 
    invisible = None     #boolean True if block.pos[1] < -block.size[1]
    spawnBlock = None    #boolean True if block has never had ground = True
    blockCol = None      #boolean True if block has collided with any other widget
    block_bottom = None
    block_right = None

    #Each blocks has its own random xpos, fallSpeed
    def __init__(self, *args, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.ground, self.invisible, self.spawnBlock, self.blockCol = False, False, True, False
        self.fallSpeed = 6
        self.findPos()

        #hardcode positions for testing
        #self.pos[0] = 20
        #self.pos[1] = 1200

    def update(self):
        self.pos[1] -= self.fallSpeed
        if (self.pos[1] < 0):
            self.fallSpeed = 0 
            self.ground = True
        if (self.blockCol):
            self.fallSpeed = 0
        if (self.pos[1] < -self.size[1]):
            self.invisible = True

    #Find spawn xpos such that its not inside another block
    def findPos(self):
        self.pos = [random.randint(1, 900), 1200]

        #logging.info('s.pos[0]: %s s.pos[1]: %s s.size[0]: %s s.size[1]: %s', str(self.pos[0]), str(self.pos[1]), str(self.size[1]), str(self.size[0]))
        x = 0

        #Check for collisions. If there is one, reRoll self.pos[0]
        #TODO: Optimize this loop to check only for other blocks with a spawn y value
        while (x < len(blocks)):
            #logging.info('index: %s x: %s y: %s width: %s height: %s', x, blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])
            while(self.blockCollision(blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])):
                #logging.info('%s Block collision with index: ', x)
                self.reRoll()
                x = -1
            x += 1

        #logging.info('index: %s Final position = %s', len(blocks), self.pos[0])
        #logging.info('\n')

    #Find a new block self.pos[0]
    def reRoll(self):
        self.pos = [random.randint(1, 900), 1200]
        #logging.info('reRoll: %s', self.pos[0])
        for x in range(0, len(blocks)):
            self.blockCollision(blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])


    #Axis-aligned bounding box collision detection
    def blockCollision(self, x, y, width, height):
        if ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y)):
            return True 

        else:
            return False
    
    #If block is on ground, it should dissapear only when character is increasing height
    def dissapear(self, speed):
        if (self.ground or self.fallSpeed == 0):
            self.pos[1] -= speed

