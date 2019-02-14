import kivy
kivy.require('1.10.1')
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget

import logging
logging.basicConfig(level=logging.CRITICAL)

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

    def playerCollisionX(self, x, y, width, height):
        if ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y) and self.velocityX > 0):
            return True
            print ("left side hit")
            
        elif ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y) and self.velocityX < 0):
            print ("right side hit")
            return False

    def playerCollisionY(self, x, y, width, height):
        if ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y) and self.velocityY < 0):
            print ("top side hit")
            return True
            
        elif ((self.pos[0] < x + width) and (self.pos[0] + self.size[0] > x) and \
            (self.pos[1] < y + height) and (self.size[1] + self.pos[1] > y) and self.velocityX >= 0):
            print ("bottom side hit")
            return False

    def update(self):
        #update vCenter and hCenter
        self.vCenter = self.pos[1] + (self.size[1] / 2) 
        self.hCenter = self.pos[0] + (self.size[0] / 2)
        
        #position of ball will move by the velocity every frame
        self.pos[0] += self.velocityX
        self.pos[1] += self.velocityY

        #only if ball is moving horizontally, apply drag. Always apply gravity
        self.velocityY -= self.gravity
        if(self.velocityX != 0):
            self.velocityX /=self.dragX

        if(self.pos[0] > 1000):
            self.pos[0] = 0
        elif(self.pos[0] < 0):
            self.pos[0] = 1000

        #Floor Level
        if(self.pos[1] < 5):
            self.velocityY = 0

