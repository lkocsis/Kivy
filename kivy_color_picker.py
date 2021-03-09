import kivy.uix.colorpicker as ColorPicker
from kivy.app import App
from kivy.uix.button import Button
#
class Button1(Button):
    pass
class ColorPicker1(ColorPicker):
    pass
    
class KivyColorApp(App):
    def build(self):
        clr_picker1 = ColorPicker1()
        button1 = Button()
        button1.add_widget(clr_picker1)
        clr_picker1.bind(color=on_color)
        # return a Button() as a root widget
        return button1(text='hello world: built in return')
        
    def on_color(self, value):
        print ("RGBA = ", str(value))  #  or instance.color
        print ("HSV = ", str(self.hsv))
        print ("HEX = ", str(self.hex_color))

# To monitor changes, we can bind to color property changes


