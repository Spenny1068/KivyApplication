import kivy
kivy.require('1.10.1')
from kivy.uix.widget import Widget

#Infinite vertical scrolling background
class Background(Widget):
    scrollSpeed = 2     #Speed of background scroll

    def update(self):
        self.pos[1] -= self.scrollSpeed
        if(self.pos[1] < -self.size[1]):
            self.pos = [0, 0]