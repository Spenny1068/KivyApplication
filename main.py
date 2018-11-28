#!/bin/python
import kivy
import logging
import random

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
#Now blocks at bottom are not stopping when hitting other blocks already on ground
#Figure out how to implement heightScore


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

        #print("s.pos[0]: " + str(self.pos[0]) + " s.pos[1]: " + str(self.pos[1]) + " s.size[0]: " + str(self.size[0]) + " s.size[1]: " + str(self.size[0]))
        x = 0

        #Check for collisions. If there is one, reRoll self.pos[0]
        #TODO: Optimize this loop to check only for other blocks with a spawn y value
        while (x < len(blocks)):
            self.detectCollision(blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])
            #print("index: " + str(x) + " x: " + str(blocks[x].pos[0]) + " y: " + str(blocks[x].pos[1]) + " width: " + str(blocks[x].size[0]) + " height: " + str(blocks[x].size[1]))
            while(self.blockCol):
                #print("Block collision with index: " + str(x))
                self.reRoll()
                x = -1
            x += 1

        #print("index: " + str(len(blocks)) + " Final position = " + str(self.pos[0]))
        #print("\n")

    #Find a new block self.pos[0]
    def reRoll(self):
        self.pos = [random.randint(1, 900), 1200]
        print("reRoll: " + str(self.pos[0]))
        for x in range(0, len(blocks)):
            self.detectCollision(blocks[x].pos[0], blocks[x].pos[1], blocks[x].size[0], blocks[x].size[1])


    #Axis-aligned bounding box collision detection
    def detectCollision(self, x, y, width, height):
        if ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y)):
            self.blockCol = True

        else:
            self.blockCol = False
    
    #If block is on ground, it should dissapear only when character is increasing height
    def dissapear(self, speed):
        if (self.ground):
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
        for i in range(NUM_BLOCKS): #0 to (NUM_BLOCKS - 1)
            self.addBlock()

    def addBlock(self):
        block = Block() 
        self.ids.blk.add_widget(block)
        blocks.append(block)   
        print("new block index" + str(len(blocks)))

    def update(self, dt):
        #Update Ball
        self.ball.update()

        #Update Blocks
        for index, b in enumerate(blocks):
            print("Index, blockCol = " + str(index) + str(b.blockCol))
            b.update()
            if (b.invisible): del blocks[index]
            if (b.ground and b.spawnBlock):
                self.addBlock()
                b.spawnBlock = False

            #Check collision for all blocks
            for index2, b2 in enumerate(blocks):
                if (index2 != index): 
                    b.detectCollision(b2.pos[0], b2.pos[1], b2.size[0], b2.size[1])


        #TODO: figure out way to smooth transition
        #Update Background
        if(self.ball.vCenter > self.size[1] * self.scroll_pos):
            self.background.update()
            for b in blocks: b.dissapear(self.background.scrollSpeed)


    #####     HANDLE INPUT    #######

    #When a key is pressed
    def keyPressed(self, keyboard, keycode, text, modifier):
        #Horizontal movement
        if(keycode[1] == 'left' or keycode[1] == 'right' or keycode[1] == 'up' or keycode[1] == 'down'):
            self.ball.move(keycode[1])

        #Pressing escape will permanently unbind keyboard
        if(keycode[1] == 'escape'):
            self.killKeyboard()
        #Return True to accept the key. Otherwise, it will be used by the system.
        return True

    #When a key is released
    def keyReleased(self, keyboard, keycode):
        if(keycode[1] == 'w'):
            print(str(keycode[1]) + " released")

    #Permanently Unbind keyboard
    def killKeyboard(self):
        print('Keyboard unbinded')
        self._keyboard.unbind(on_key_down=self.keyPressed)


class ScreenManager(ScreenManager):
    pass

class MarshmallowApp(App):  
    def build(self):
        Window.size = (600, 600)
        return ScreenManager()

if __name__ == '__main__':
    MarshmallowApp().run()
