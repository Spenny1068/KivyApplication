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

import background
import player
import block

#### TODO ####
#Why wont logging.debug work tf
#Figure out how to implement heightScore
#Implement restart button so we don't have to CTRL+C every time
#Implement character-block collision

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
        self.initBlocks()   #initialize array of block.blocks
    
    
    @mainthread #delay function so kv file gets scanned first, making the ids list viable   
    def initBlocks(self):
        self.addBlock(block.NUM_BLOCKS)

    def addBlock(self, n):
        #logging.info('new block index %s', len(block.blocks))
        for x in range(0, n):
            blck = block.Block() 
            self.ids.blk.add_widget(blck)
            block.blocks.append(blck)   

    #So we don't have to CTRL+C everytime to reset game
    def resetPlayScreen(self):

        #Move all block.blocks above screen and then empty array
        for b in block.blocks: b.pos[1] = 1500
        block.blocks.clear()
        self.addBlock(block.NUM_BLOCKS)

        #Reset character position


        #Reset score
        


    def update(self, dt):

        #### UPDATE BALL ####
        self.ball.update()

        for index, b in enumerate(block.blocks):

            #check player collision
            if(self.ball.playerCollisionX(b.pos[0], b.pos[1], b.size[0], b.size[1])):
                #restrict right movement
                pass
                
                #if(self.ball.velocityX > 0): self.ball.velocityX = 0
            else:
                #restrict left movement
                #if(self.ball.velocityX < 0): self.ball.velocityX = 0
                pass

            if(self.ball.playerCollisionY(b.pos[0], b.pos[1], b.size[0], b.size[1])):
                #restrict down movement
                #if(self.ball.velocityY < 0): self.ball.velocityY = 0
                pass

            else:
                #restrict up movement
                #if(self.ball.velocityY > 0): self.ball.velocityY = 0
                pass


        #### UPDATE BLOCKS ####
        #logging.info('len(block.blocks) = %s', len(block.blocks))

        for index, b in enumerate(block.blocks):

            if (len(block.blocks) >= block.MAX_BLOCKS):
                exit()

            #logging.info('Index, blockCol: %s %s', index, b.blockCol)

            #Check collision for all block.blocks
            for index2, b2 in enumerate(block.blocks):
                if (index2 != index and b.blockCollision(b2.pos[0], b2.pos[1], b2.size[0], b2.size[1])):
                    #logging.info('Collision: Block %s and %s', index, index2)
                    b.blockCol = True

            #update b.pos[1], b.stopped(fallSpeed = 0), b.ground,and b.invisible for every block in array 
            b.update()

            #When block is completely off screen, delete from array
            if (b.invisible): del block.blocks[index]

            #Conditions to call addBlock()
            if (b.fallSpeed == 0 and b.spawnBlock):
                self.addBlock(1)
                b.spawnBlock = False

        #### UPDATE BACKGROUND ####
        if(self.ball.vCenter > self.size[1] * self.scroll_pos):
            self.background.update()
            for b in block.blocks: b.dissapear(self.background.scrollSpeed)


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
