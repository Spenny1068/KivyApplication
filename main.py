#!/bin/python
import kivy
kivy.require('1.9.1')
from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '800')

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics.instructions import VertexInstruction
from kivy.core.window import Window
from kivy.core.window import Keyboard
from kivy.graphics import *
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.image import Image


#Dynamic background picture
class Background(Widget):
    size = [1000, 800]
    def update(self):
        self.pos[1] -= 10
        if(self.pos[1] < (-800)*2):
            self.pos = [0, 0]


#Character
class Ball(Widget):

    velocityX = 0   #pixels per frame
    velocityY = 0
    gravity = 1.5     #vertical drag
    dragX = 1.1      #Horizontal friction

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
        #position of ball will move by the velocity every frame
        self.pos[0] += self.velocityX
        self.pos[1] += self.velocityY

        #only if ball is moving horizontally, apply drag. Always apply gravity
        if(self.velocityX != 0):
            self.velocityX /=self.dragX
            self.velocityY -= self.gravity

        if(self.pos[0] > 800):
            self.pos[0] = 0
        elif(self.pos[0] < 0):
            self.pos[0] = 800

        #Floor Level
        if(self.pos[1] < 15):
            self.velocityY = 0


class MarshmallowGame(Widget):
    ball = ObjectProperty(None)
    background = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(MarshmallowGame, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/30.0)
        self._keyboard = Window.request_keyboard(self.killKeyboard, self, 'text')   #Request Keyboard
        self._keyboard.bind(on_key_down=self.keyPressed)    #key pressed event
        self._keyboard.bind(on_key_up=self.keyReleased)     #key release event

    def initializePlayer(self):
        self.ball.center = self.center

    def update(self, dt):
        self.ball.update()
        self.background.update()


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
        return ScreenManager()

if __name__ == '__main__':
    MarshmallowApp().run()
