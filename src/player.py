import sys
import logging
logging.basicConfig(level=logging.CRITICAL)

import kivy
from kivy.properties import ObjectProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
kivy.require('1.10.1')

#####    MAIN CHARACTER    #####
class Ball(Widget):
    heightScore = NumericProperty(0)
    vCenter = None  # vertical center of character
    hCenter = None  # horizontal center of character
    player_bottom = None
    player_right = None
    heightScore = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.velocityX = 0   # pixels per frame  
        self.velocityY = 0
        self.gravity = 3   # vertical drag
        self.dragX = 1.1     # Horizontal friction
        self.pos = (Window.size[0] / 2, 0)
            
    #####    MOVE FUNCTIONS    #####
    def moveLeft(self, enabled):
        if (enabled): self.velocityX = -10

    def moveRight(self, enabled):
        if (enabled): self.velocityX = 10

    def moveUp(self, enabled):
        if (enabled): self.velocityY = 35

    ######    COLLISION DETECTION    #####
    def playerCollision(self, x, y, width, height):
        if ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y)):
            return True     

    def squished(self, blockFloor):
        playerHeight = self.size[1]
        distance = blockFloor - self.pos[1]
        headRoom = 25

        # if distance between the blocks floor and the players floor is < than player height
        if (distance < playerHeight - headRoom):
            sys.exit('Squished - Game Over')

    def wrapCoordinates(self):
        if(self.pos[0] > Window.size[0]): self.pos[0] = 0
        elif(self.pos[0] < 0): self.pos[0] = Window.size[0]

    def maxHeight(self):
        if (self.pos[1] > self.heightScore):
            self.heightScore = self.pos[1]

    ##### PLAYER UPDATE #####
    def update(self):
        # update vCenter and hCenter
        self.vCenter = self.pos[1] + (self.size[1] / 2) 
        self.hCenter = self.pos[0] + (self.size[0] / 2)
        
        # update edges of player widget
        self.player_bottom = self.pos[1] + self.size[1]
        self.player_right = self.pos[0] + self.size[0]

        # position of ball will move by the velocity every frame
        self.pos[0] += self.velocityX
        self.pos[1] += self.velocityY

        # only if ball is moving horizontally, apply drag. Always apply gravity
        self.velocityY -= self.gravity
        if(self.velocityX != 0):
            self.velocityX /=self.dragX

        # wrap player coordinates
        self.wrapCoordinates()

        # update score
        self.maxHeight()

        # floor Level
        if(self.pos[1] < 0):
            self.velocityY = 0

            # player should always stay above or equal to floor level
            self.pos[1] = 0
            assert (self.pos[1] >= 0), "Player is below floor level"

