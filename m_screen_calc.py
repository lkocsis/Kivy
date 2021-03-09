# https://stackoverflow.com/questions/56134865/kivy-multiple-screen-management
import os, sys
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
#
class Calculator(GridLayout):
    def calculate(self, calculation):
        if calculation:
            try:
                self.display.text = str(eval(calculation))
            except Exception:
                self.display.text = "Error"

class MenuScreen(Screen):
    pass

class CalculatorScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

# print(os.path.dirname(os.path.abspath(__file__)))
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Builder.load_file("m_screen_calc_kv_.kv")

class m_screen_calcApp(App):
    Window.clearcolor = .3, .3, .3, 1
    title = 'LKL@'+platform
    kv_file = 'm_screen_calc_kv_.kv'
    print ('kv is loaded')
    def build(self):
        return ScreenManagement()

if __name__ == '__main__':
    m_screen_calcApp().run()