#!/bin/python
import kivy
import random

kivy.require('1.9.1')
from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '800')

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
#When block is off screen, remove from blocks[]
#addBlock function: when block hits ground, use addBlock() to add a new block
#Add collision detection and 'edges' to each block in blocks[]

#Infinite vertical scrolling background
class Background(Widget):
	scrollSpeed = 2     #Speed of background scroll

	def update(self):
		self.pos[1] -= self.scrollSpeed
		if(self.pos[1] < -self.size[1]):
			self.pos = [0, 0]

#Array of falling blocks
class Block(Widget):
	ground = None	#boolean True if fallSpeed = 0
	invisible = None	#boolean True if block.pos[1] < -block.size[1]

	#Each blocks has its own random xpos, fallSpeed
	def __init__(self, *args, **kwargs):
		super(Block, self).__init__(**kwargs)
		self.pos = [random.randint(1, 900), 800]
		self.fallSpeed = random.randint(5, 8)
		self.ground = False
		self.invisible = False

	def update(self):
		self.pos[1] -= self.fallSpeed
		if (self.pos[1] < 0):
			self.fallSpeed = 0 
			self.ground = True
		if (self.pos[1] < -self.size[1]):
			self.invisible = True
	
	#If block is on ground, it should dissapear only when character is increasing height
	def dissapear(self, speed):
		self.pos[1] -= speed


#Main Character
class Ball(Widget):
	vCenter = None	#Vertical center of character
	hCenter = None	#Horizontal center of character

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
	heightScore = NumericProperty(0)
	NUM_BLOCKS = 3  #number of blocks in array

	background = ObjectProperty(None)
	ball = ObjectProperty(None)
	blocks = [] * NUM_BLOCKS
	

    #Percentage way up background when ball pos will scroll background
	scroll_pos = 1.0/2.0

	def __init__(self, *args, **kwargs):
		super(MarshmallowGame, self).__init__(**kwargs)
		Clock.schedule_interval(self.update, 1.0/30.0)
		self._keyboard = Window.request_keyboard(self.killKeyboard, self, 'text')   #Request Keyboard
		self._keyboard.bind(on_key_down=self.keyPressed)    #key pressed event
		self._keyboard.bind(on_key_up=self.keyReleased)     #key release event
		self.initBlocks()	#initialize array of blocks
	
	@mainthread #delay function so kv file gets scanned first, making the ids list viable	
	def initBlocks(self):
		for i in range(self.NUM_BLOCKS):	#0 to (NUM_BLOCKS - 1)
			block = Block()
			self.ids.blk.add_widget(block)
			self.blocks.append(block)

	def addBlock(self):
		block = Block()	
		self.ids.blk.add_widget(block)
		self.blocks.append(block)

		
	def update(self, dt):
		self.ball.update()
		for b in self.blocks:
			b.update()
			#if (b.invisible):
			#	blocks.remove()

        #TODO: figure out way to smooth transition
		if(self.ball.vCenter > self.size[1] * self.scroll_pos):
			self.background.update()
			for b in self.blocks:
				if b.ground: b.dissapear(self.background.scrollSpeed)


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
