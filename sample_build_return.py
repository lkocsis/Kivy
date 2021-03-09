'''
Application example using build() + return
==========================================

An application can be built if you return a widget on build(), or if you set
self.root.
'''

import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
class Button1(Button):
    background_color= (1,1,0,1)
    text='hello world: built in return'   

class TestApp(App):
    def build(self):
        btn = Button1()
        # return a Button() as a root widget
        return btn


if __name__ == '__main__':
    app= TestApp()
    app().run()