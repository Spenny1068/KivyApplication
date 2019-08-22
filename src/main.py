#!/Usr/bin/env python3
import kivy
import sys
import logging
logging.basicConfig(level=logging.WARNING)

kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.window import Keyboard
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.config import Config 

Config.set('graphics', 'resizable', True)

import background
import player
import block

#####    TODO    #####
# why wont logging.debug work tf
# fix logging across multiple files
# figure out how to implement heightScore
# implement restart button to call the resetPlayScreen function
# fix key enable/disable
# needs code refactor for character-block collision
# should background scroll speed move at the same speed of player?
# height score is in relative to the bottom of the screen atm
# scroll is not happening at half way ???

#####    GLOBAL VARIABLES    #####
FPS = 30 # fps the game will run at 

#####    MAIN GAME CLASS   #####
class MarshmallowGame(Widget):
    background = ObjectProperty(None)
    ball = ObjectProperty(None)

    # keys should start out all enabled
    leftKeyEnable, rightKeyEnable, upKeyEnable, downKeyEnable = True, True, True, True

    # for character-block collision detection
    b_collision = None
    t_collision = None
    l_collision = None
    r_collision = None
    
    # percentage way up background when ball pos will scroll background
    scroll_pos = 1.0/2.0

    def __init__(self, *args, **kwargs):
        super(MarshmallowGame, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/FPS)
        self._keyboard = Window.request_keyboard(self.killKeyboard, self, 'text')   # request Keyboard
        self._keyboard.bind(on_key_down=self.keyPressed)    # key pressed event
        self._keyboard.bind(on_key_up=self.keyReleased)     # key release event
        self.initBlocks()   # initialize array of block.blocks
    
    
    @mainthread # delay function so kv file gets scanned first, making the ids list viable   
    def initBlocks(self):
        self.addBlock(block.NUM_BLOCKS)

    # adds a block to blocks[] and screen
    def addBlock(self, n):
        #logging.info('new block index %s', len(block.blocks))
        for x in range(0, n):
            blck = block.Block() 
            self.ids.blk.add_widget(blck)
            block.blocks.append(blck)   

    #####    RESET GAME    #####
    def resetPlayScreen(self):

        # move all block.blocks above screen and then empty array
        for b in block.blocks: b.pos[1] = 1500
        block.blocks.clear()
        self.addBlock(block.NUM_BLOCKS)

        # reset character position
        # reset score

    #####    MAIN UPDATE FUNCTION    #####
    def update(self, dt):

        #####    UPDATE CHARACTER   #####
        self.ball.update()
        self.ball.heightScore = (self.ball.height + self.background.scrollDistance) // 20
        #logging.info('playerPos[1]: %s', str(self.ball.pos[1]))

        # update character collision
        for index, b in enumerate(block.blocks):

            # for block-character collision detection
            b.block_bottom = b.pos[1] + b.size[1]
            b.block_right = b.pos[0] + b.size[0]

            self.b_collision = b.block_bottom - self.ball.pos[1]
            self.t_collision = self.ball.player_bottom - b.pos[1]
            self.l_collision = self.ball.player_right - b.pos[0]
            self.r_collision = b.block_right - self.ball.pos[0]

            # check player-block collision
            if(self.ball.playerCollision(block.blocks[index].pos[0], block.blocks[index].pos[1], block.blocks[index].size[0], block.blocks[index].size[1])):

                # check if player is below the block
                if((self.t_collision < self.b_collision) and (self.t_collision < self.l_collision) and (self.t_collision < self.r_collision)):

                    # restrict up movement
                    self.upKeyEnable = False
                    self.downKeyEnable = True

                    # bumping effect
                    self.ball.velocityY = -10

                    #####    GAME OVER CONDITION 1 - player squished    #####
                    #self.ball.squished(b.pos[1])

                    #logging.info('bottom side hit')
                    
                # check if player is above the block
                if((self.b_collision < self.t_collision) and (self.b_collision < self.l_collision) and (self.b_collision < self.r_collision)):

                    # restrict down movement
                    self.downKeyEnable = False
                    self.upKeyEnable = True

                    # make velocity = 0
                    self.ball.velocityY = 0
    
                    # player should never be able to pass through top of block
                    errorSpace = 9
                    self.ball.pos[1] = b.pos[1] + b.size[1] - errorSpace

                    #logging.info('top side hit')

                
                # check if player is to the left of block
                if((self.l_collision < self.r_collision) and (self.l_collision < self.t_collision) and (self.l_collision < self.b_collision)):

                    # restrict right movement
                    self.rightKeyEnable = False
                    self.leftKeyEnable = True

                    self.ball.velocityX = 0

                    #logging.info('left side hit')

                # check if player is to the right of block
                if((self.r_collision < self.l_collision) and (self.r_collision < self.t_collision) and (self.r_collision < self.b_collision)):

                    # restrict left movement
                    self.leftKeyEnable = False
                    self.rightKeyEnable = True

                    self.ball.velocityX = 0

                    #logging.info('right side hit')

            # no player-block collision
            else:

                # enable all keys
                self.downKeyEnable, self.upKeyEnable = True, True
                self.leftKeyEnable, self.rightKeyEnable = True, True
                #logging.info('no collsion')

        #####    UPDATE BLOCKS    #####
        #logging.info('len(blocks) = %s', len(block.blocks))

        for index, b in enumerate(block.blocks):
            
            #####    GAME OVER CONDITION 2 - max number of blocks    #####
            if (len(block.blocks) >= block.MAX_BLOCKS):
                sys.exit('Max blocks on screen reached')

            #logging.info('Index, blockCol: %s %s', index, b.blockCol)

            # check collision for all block.blocks
            for index2, b2 in enumerate(block.blocks):
                if (index2 != index and b.blockCollision(b2.pos[0], b2.pos[1], b2.size[0], b2.size[1])):
                    #logging.info('Collision: Block %s and %s', index, index2)
                    b.blockCol = True

            # update b.pos[1], b.stopped(fallSpeed = 0), b.ground,and b.invisible for every block in array 
            b.update()

            # When block is completely off screen, delete from array
            if (b.invisible): del block.blocks[index]

            # conditions to call addBlock()
            if (b.fallSpeed == 0 and b.spawnBlock):
                self.addBlock(1)
                b.spawnBlock = False

        #####    UPDATE BACKGROUND    #####
        if(self.ball.vCenter > Window.size[1] * self.scroll_pos):
            self.background.update()

            # when background is scrolling, blocks fall faster and blocks on ground fade off screen
            for b in block.blocks: 
                b.dissapear(self.background.scrollSpeed)
                b.inc = 5   # block fallSpeed gain

    #####    HANDLE INPUT   ######
    def keyPressed(self, keyboard, keycode, text, modifier):

        # horizontal movement
        if(keycode[1] == 'left'):
            self.ball.moveLeft(self.leftKeyEnable)
        if(keycode[1] == 'right'):
            self.ball.moveRight(self.rightKeyEnable)

        # vertical movement
        if(keycode[1] == 'up'): 
            self.ball.moveUp(self.upKeyEnable)

        # we need to make this into a reset button 
        if(keycode[1] == 'delete'):
            self.resetPlayScreen()

        # pressing escape will permanently unbind keyboard
        if(keycode[1] == 'escape'):
            self.killKeyboard()

        # return True to accept the key. Otherwise, it will be used by the system.
        return True

    # when a key is released
    def keyReleased(self, keyboard, keycode):
        if(keycode[1] == 'w'):
            #logging.info("%s released", keycode[1])
            pass

    # permanently Unbind keyboard
    def killKeyboard(self):
        logging.warning('Keyboard unbinded')
        self._keyboard.unbind(on_key_down=self.keyPressed)


#####    SCREENS CLASS    #####
class ScreenManager(ScreenManager):
    pass

#####    MAIN BUILD    #####
class MarshmallowApp(App):  
    def build(self):
        Window.size = (600, 600)
        return ScreenManager()

if __name__ == '__main__':
    MarshmallowApp().run()
