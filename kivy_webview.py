# https://stackoverflow.com/questions/44489331/python-kivy-app-that-open-url-in-a-native-web-browser/44531229
# https://pyjnius.readthedocs.io/en/stable/installation.html

import kivy
kivy.require('1.9.2')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# MICHAEL'S CODE
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass
from android.runnable import run_on_ui_thread # PyJnius

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.renpy.android.PythonActivity').mActivity

class Wv(Widget):
    def __init__(self, **kwargs):
        super(Wv, self).__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        wvc = WebViewClient();
        webview.setWebViewClient(wvc);
        activity.setContentView(webview)
        webview.loadUrl('http://www.google.com/')
# END OF MICHAEL'S CODE

Builder.load_string('''

<ScreenOne>:
    BoxLayout:
        Label:
            text: "SCREEN 1"
        Button:
            text: "GO GO GO TO GOOGLE !"
            on_press: root.open_browser()

<ScreenTwo>:
    BoxLayout:
        Label:
            text: "SCREEN 2"
        Button:
            text: "GO GO GO TO SCREEN 1"
            on_press:
                root.manager.transition.direction = "right"
                root.manager.transition.duration = 1
                root.manager.current = "screen_one"

''')

class ScreenOne(Screen):
    def open_browser(self):
        return Wv()

class ScreenTwo(Screen):
    pass

screen_manager = ScreenManager()

screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))


class BrowserApp(App):
    def build(self):
        return screen_manager

app = BrowserApp()
app.run()