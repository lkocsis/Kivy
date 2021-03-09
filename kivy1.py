#!/usr/bin/env python
# Created: 2020-12-20 13:42:49
# https://www.w3schools.com/colors/colors_names.asp
# https://www.w3schools.com/colors/colors_groups.asp
##############################  set BASICS  ########################################
#$ CWD
import os, sys, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PyFilePath  = os.path.dirname(os.path.abspath(__file__))
PyPrgName   = os.path.basename(__file__).split('.')[0]
#$ Log
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from pyIniLib import setLog, log
PyLogFile = setLog(__file__, g=globals, l= locals)
P='p'
#
#$ PyLib
if os.path.exists(os.path.abspath(__file__).split('.')[0]+'Ext.py'):
    try:  exec('from '+os.path.basename(__file__).split('.')[0]+'Ext import *')
    except ImportError: print('ERROR: ...Ext.py does not exist', sys.exc_info())
from pyIniLib import (G, setLog, log, pylibfolder, dtStamp, dateStamp, getPyParam,
                        rgba_float)
setattr(G,'pyLibFolder', pylibfolder())
#$ PyParam
import json
PyParam, PyParamFile = getPyParam(__file__)
########################################################################################
#$ Kivy 
import webcolors
from kivy.config import Config
# Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.properties import ( NumericProperty, StringProperty, BooleanProperty, ListProperty, 
                        ReferenceListProperty, ObjectProperty )
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.base import runTouchApp
from functools import partial
import webbrowser
import webcolors
########################################################################################
class MainScreen(Screen):
    # btn2 = ObjectProperty()
    # self.ids.btn1.bind(on_press = self.btn1_press)
    def __init__(self, *args,**kwargs):
        self.spinner1_values = ['Languages', "Python", "Java", "C++", "C", "C#", "PHP"]
        # self.ids.btn_exit.bind(on_release = self.btn1_press())
        super(MainScreen, self).__init__(*args, **kwargs)

    def btn1_press(self):
        print(self.ids.btn1.text)

    def btn2_press(self):
        print(self.ids.btn2.text)
    
    def selected(self, item):
        print(item)

    def on_spinner_select(self, text):
        print (text)
    
    def onExit(self):
        webbrowser.open_new_tab('https://www.prageru.com/')
        App.get_running_app().stop()

class Kivy1App(App):
    # https://www.w3schools.com/colors/colors_groups.asp
    title = 'Kivy1Title'
    kv_directory = 'templates'
    def build(self):
        Window.clearcolor = (rgba_float('BlanchedAlmond')) # RGBA
        return MainScreen()
    
if __name__ == '__main__':
# https://www.w3schools.com/colors/colors_names.asp

    # runTouchApp(MyListView())
    # subprocess.call('clear' if os.name =='posix' else 'clear')
    # log('--------------------------- Label1 ----------')
    # log(Label1)
    # log('--------------------------- Button1 ----------')
    # log(Button1)
    # app = Kivy1App() # app.run()
    Kivy1App().run()
"""
    canvas.before:
        Color:
            rgba: 1, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size

        canvas.before:
            Color:
                rgb: 1, 1, 1
    #        Rectangle:
    #            size: self.size
    #            pos: self.pos
    #            source: 'data/background.png'
            size_hint: .3, .2
        dropdown = Kivy1DropDown()
    log('--------------------------- Kivy1DropDown ----------')
    log(Kivy1DropDown)
    mainbutton = Button(text='Hello', size_hint=(None, None))
    mainbutton.bind(on_release=dropdown.open)
    dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
    runTouchApp(mainbutton())

      

"""