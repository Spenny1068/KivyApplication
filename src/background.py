import logging
logging.basicConfig(level=logging.critical)

import kivy
from kivy.uix.widget import Widget
kivy.require('1.10.1')

#####    INFINITE SCROLLING BACKGROUND    #####
class Background(Widget):
    scrollSpeed = 5     #Speed of background scroll

    #####    SCROLL SCREEN    #####
    def update(self):

        #logging.info('ceilingHeight: %s', str(self.pos[1]))
        self.pos[1] -= self.scrollSpeed
        if(self.pos[1] < -self.size[1]):
            self.pos = [0, 0]
