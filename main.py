#!/bin/python
import kivy
import random
import logging
logging.basicConfig(level=logging.CRITICAL)

kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.window import Keyboard
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.clock import mainthread

#### TODO ####
#Why wont logging.debug work tf
#Figure out how to implement heightScore
#Implement restart button so we don't have to CTRL+C every time
#Implement character-block collision


#Global variables
NUM_BLOCKS = 3 #Remember theres 1 extra block not in array above screen
blocks = [] * NUM_BLOCKS

#Infinite vertical scrolling background
class Background(Widget):
    scrollSpeed = 2     #Speed of background scroll

    def update(self):
        self.pos[1] -= self.scrollSpeed
        if(self.pos[1] < -self.size[1]):
            self.pos = [0, 0]

#Array of falling blocks
class Block(Widget):
    ground = None        #boolean True if block.pos[1] < 0 
    invisible = None     #boolean True if block.pos[1] < -block.size[1]
    spawnBlock = None    #boolean True if block has never had ground = True
    blockCol = None      #boolean True if block has collided with any other widget
    playerCol = None     #boolean True if block has collided with player widget

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
            while(self.Collision(blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])):
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
            self.Collision(blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])


    #Axis-aligned bounding box collision detection
    def Collision(self, x, y, width, height):
        if ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y)):
            return True 

        else:
            return False
    
    #If block is on ground, it should dissapear only when character is increasing height
    def dissapear(self, speed):
        if (self.ground or self.fallSpeed == 0):
            self.pos[1] -= speed


#Main Character
class Ball(Widget):
    heightScore = NumericProperty(0)
    vCenter = None  #Vertical center of character
    hCenter = None  #Horizontal center of character

    def __init__(self, *args, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.velocityX = 0   #pixels per frame  
        self.velocityY = 0
        self.gravity = 1.5   #vertical drag
        self.dragX = 1.1     #Horizontal friction
            
    def move(self, keycode):
        if(keycode == 'left'):
            self.velocityX = -10
        if(keycode == 'right'):
            self.velocityX = 10
        if(keycode == 'up'):
            self.velocityY = 15
        if(keycode == 'down'):
            self.velocityY = -10


    def update(self):
        #update vCenter and hCenter
        self.vCenter = self.pos[1] + (self.size[1] / 2) 
        self.hCenter = self.pos[0] + (self.size[0] / 2)
        
        #position of ball will move by the velocity every frame
        self.pos[0] += self.velocityX
        self.pos[1] += self.velocityY

        #only if ball is moving horizontally, apply drag. Always apply gravity
        if(self.velocityX != 0):
            self.velocityX /=self.dragX
            self.velocityY -= self.gravity

        if(self.pos[0] > 1000):
            self.pos[0] = 0
        elif(self.pos[0] < 0):
            self.pos[0] = 1000

        #Floor Level
        if(self.pos[1] < 5):
            self.velocityY = 0


#Main game class
class MarshmallowGame(Widget):
    background = ObjectProperty(None)
    ball = ObjectProperty(None)
    
    #Percentage way up background when ball pos will scroll background
    scroll_pos = 1.0/2.0

    def __init__(self, *args, **kwargs):
        super(MarshmallowGame, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/30.0)
        self._keyboard = Window.request_keyboard(self.killKeyboard, self, 'text')   #Request Keyboard
        self._keyboard.bind(on_key_down=self.keyPressed)    #key pressed event
        self._keyboard.bind(on_key_up=self.keyReleased)     #key release event
        self.initBlocks()   #initialize array of blocks
    
    
    @mainthread #delay function so kv file gets scanned first, making the ids list viable   
    def initBlocks(self):
        self.addBlock(NUM_BLOCKS)

    def addBlock(self, n):
        #logging.info('new block index %s', len(blocks))
        for x in range(0, n):
            block = Block() 
            self.ids.blk.add_widget(block)
            blocks.append(block)   

    #So we don't have to CTRL+C everytime to reset game
    def resetPlayScreen(self):

        #Move all blocks above screen and then empty array
        for b in blocks: b.pos[1] = 1500
        blocks.clear()
        self.addBlock(NUM_BLOCKS)

        #Reset character position


        #Reset score
        


    def update(self, dt):

        #### UPDATE BALL ####
        self.ball.update()

        #### UPDATE BLOCKS ####
        #logging.info('len(blocks) = %s', len(blocks))

        for index, b in enumerate(blocks):
            #logging.info('Index, blockCol: %s %s', index, b.blockCol)

            #Check collision for all blocks
            for index2, b2 in enumerate(blocks):
                if (index2 != index and b.Collision(b2.pos[0], b2.pos[1], b2.size[0], b2.size[1])):
                    #logging.info('Collision: Block %s and %s', index, index2)
                    b.blockCol = True

            #update b.pos[1], b.stopped(fallSpeed = 0), b.ground,and b.invisible for every block in array 
            b.update()

            #When block is completely off screen, delete from array
            if (b.invisible): del blocks[index]

            #Conditions to call addBlock()
            if (b.fallSpeed == 0 and b.spawnBlock):
                self.addBlock(1)
                b.spawnBlock = False

        #### UPDATE BACKGROUND ####
        if(self.ball.vCenter > self.size[1] * self.scroll_pos):
            self.background.update()
            for b in blocks: b.dissapear(self.background.scrollSpeed)


    #####     HANDLE INPUT    #######

    #When a key is pressed
    def keyPressed(self, keyboard, keycode, text, modifier):
        #Horizontal movement
        if(keycode[1] == 'left' or keycode[1] == 'right' or keycode[1] == 'up' or keycode[1] == 'down'):
            self.ball.move(keycode[1])

        #We need to make this into a reset button 
        if(keycode[1] == 'delete'):
            self.resetPlayScreen()

        #Pressing escape will permanently unbind keyboard
        if(keycode[1] == 'escape'):
            self.killKeyboard()
        #Return True to accept the key. Otherwise, it will be used by the system.
        return True

    #When a key is released
    def keyReleased(self, keyboard, keycode):
        if(keycode[1] == 'w'):
            #logging.info("%s released", keycode[1])
            pass

    #Permanently Unbind keyboard
    def killKeyboard(self):
        logging.warning('Keyboard unbinded')
        self._keyboard.unbind(on_key_down=self.keyPressed)


class ScreenManager(ScreenManager):
    pass

class MarshmallowApp(App):  
    def build(self):
        Window.size = (600, 600)
        return ScreenManager()

if __name__ == '__main__':
    MarshmallowApp().run()
