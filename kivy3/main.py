# usage of buildozer:
# cd /mnt/c/Users/laszl/OneDrive/Code/VSC/VSC20_10/Kivy/kivy3
# sudo apt update
# sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
# pip3 install --user --upgrade Cython==0.29.19 virtualenv  # the --user should be removed if you do this in a venv
import os, sys, datetime, ftplib, json
import webbrowser, socket, urllib3, urllib.request, urllib.parse # NO urllib
#
import kivy3_ini
from kivy3_ini import (dtStamp, Spinner1Items, PyPrgName0, PyFilePath, PyParams, PyParamFile,
                Platform, Colors, Ftp, ftp_store) 
from kivy3_ext import (prime_numbers_ext, fibonacci_numbers_ext, list_to_string_segmented, 
                    port_scanner_threaded, colors_RGBA_json_update) 
#
#$ Kivy
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty)
from kivy.network.urlrequest import UrlRequest
from kivy.logger import logging
from kivy.vector import Vector
from kivy.clock import Clock
#
#
class ScreenManagement(ScreenManager):
    pass
#
class CalculatorScreen(Screen):
    pass
#
class XandOScreen(Screen):
    game_in_screen = ObjectProperty(None)

    def __init__(self, **kw):
        self.game_dict = {"Player" : "_", "Mode":"_", "Layout" : "_"}
        self.arretori_msg_store(json.dumps(self.game_dict))
        super().__init__(**kw)

    def mode_x_o_game(self, mode):
        if self.game_dict["Mode"] != '_':
            return
        if mode == 'Single':
            self.ids.gmode.text= 'Single'
            self.game_dict['Mode'] = 'Single'
            self.arretori_msg_store(json.dumps(self.game_dict))
        else:
            self.ids.gmode.text= 'One2One'
            self.game_dict['Mode'] = 'One2One'
            self.arretori_msg_store(json.dumps(self.game_dict))

    def arretori_read_status(self, req, result):
        print('*** read arretori status: ', req.resp_status)
        print('*** read arretori result:\n', result)
        # for key, value in req.resp_headers.items(): s = f'{key}: {value}'
        pass

    def arretori_store_status(self, req, result):
        print('*** store arretori status: ', req.resp_status)
        print('*** store arretori result:\n', result)
        # for key, value in req.resp_headers.items(): s = f'{key}: {value}'
        pass
    
    def arretori_msg_store(self, gdict):
        # params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show', 'date:': dtStamp})
        params = gdict #"{'number': 12524, 'type': 'issue', 'date:': '210306'}"
        req = UrlRequest('http://www.arretori.hu/php/x_o/xo_store_msg.php', req_body=params,
                on_success= self.arretori_store_status, on_failure=self.arretori_store_status ) 
    
    def arretori_msg_read(self, gdict):
        req = UrlRequest('http://www.arretori.hu/php/x_o/xo_read_msg.php',
                on_success= self.arretori_read_status, on_failure=self.arretori_read_status) 
        req.wait(.01)
        gdict = json.loads(req.result.replace("'", '"').encode().decode('utf-8-sig'))
        return gdict

    def layout_x_o_game(self, size=3):
        self.ids.x_o_game.remove_widget(self.ids.lbl1)
        if self.game_dict["Layout"] != '_':
            return
        self.ids.glayout.text= str(size)+'x'+str(size)
        self.game_dict["Layout"] = str(size)
        self.game_dict["Player"] = self.ids.player.text
        self.rows = []
        for r in range(size):
            self.rows.append(RawLayout())
            self.ids.x_o_game.add_widget(self.rows[r])
            for c in range(size):
                btn = CustButton()
                btn.text= '_'
                btn.font_size: 36
                id= 'R'+str(r)+'C'+str(c)
                btn.id= id
                self.game_dict[id]='_'
                btn.bind(on_press= self.x_o_button_pushed)
                self.rows[r].add_widget(btn)
            # store initial status
        self.arretori_msg_store(json.dumps(self.game_dict))
    
    def x_o_button_pushed(self, instance):
        if self.ids.player.text == 'Choose Player': 
            return
        if self.ids.gmode.text == 'Choose Mode': 
            return
        if instance.text != '_': 
            return
        player = self.ids.player.text
        mode = self.ids.gmode.text
        if mode == 'One2One':
            return
        if self.game_dict['Mode'] == 'One2One':
            if player == self.arretori_msg_read({})['Player']: 
                print ('==')
                return
            print ('<>')
        self.game_dict = self.arretori_msg_read(self.game_dict)
        self.game_dict["Player"] = player
        self.game_dict[instance.id]= player
        instance.text= player
        self.arretori_msg_store(json.dumps(self.game_dict))
        if self.game_dict['Mode'] == 'Single':
            if player == 'X': 
                self.ids.player.text = 'O'
                self.game_dict["Player"] = 'O'
            else:
                self.ids.player.text = 'X'
                self.game_dict["Player"] = 'X'

    def player_choice(self, player):
        if self.game_dict["Player"] != '_':
            return 
        self.ids.player.text = player
        self.ids.player.background_color: Colors.get('Brown',(0,0,1,1))
        self.game_dict['Player'] = player
        self.arretori_msg_store(json.dumps(self.game_dict))

class RawLayout(BoxLayout):
    pass
class CustButton(Button):
    pass      
class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
#
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
#
class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    #
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
    #
    def update(self, dt):
        self.ball.move()
        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
    #
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
#
class PongScreen(Screen):
    game_in_screen = ObjectProperty(None)
    def start_pong_game(self):
        self.game_in_screen.serve_ball()
        Clock.schedule_interval(self.game_in_screen.update, 1.0 / 60.0)
    
    def stop_pong_game(self):
        Clock.unschedule(self.game_in_screen.update) 
#
class MainScreen(Screen):
    def __init__(self, **kw):
        self.spinner1_values = Spinner1Items
        super().__init__(**kw)
    #
    def btn1_press(self): 
        self.side_label.text += "*"
    #
    def on_spinner1_select(self, text):
        tmp = text
        self.ids.spinner1.text = 'Main'
        self.manager.current = tmp
    #
    def prime_numbers(self):
        lst = prime_numbers_ext(100)
        self.ids.msglbl.text= list_to_string_segmented('Prime Numbers 1-100:', lst, 53)
    #
    def fibonacci_numbers(self):
        lst = fibonacci_numbers_ext(100)
        self.ids.msglbl.text= list_to_string_segmented('Fibonacci Numbers 1-100:', lst, 53)
    #
    def webbrowse(self, link):
        if Platform != 'android':
            webbrowser.open_new_tab(link)
        else:
            self.ids.msglbl.text = 'Sorry, webbrowser is not yet available on Android'    
    #
    def os_environ(self):
        lst = []
        self.ids.msglbl.text = '[os.environ]\n'
        for k in os.environ:
            if k != 'PATH':
                s = '{:<11} {:<2} {:}\n'.format(k, ':', os.environ[k])
                lst.append(s)
                self.ids.msglbl.text += s
            else:
                self.ids.msglbl.text += 'SYS.PATH: ________________________ \n' 
    #  
    def sys_path(self):
        lst = []
        self.ids.msglbl.text = '[sys.path]\n'
        for k in sys.path:
            lst.append(k)
            self.ids.msglbl.text += '\n'+k
    #
    def sys_argv(self):
        lst = []
        self.ids.msglbl.text = '[sys.argv]\n'
        for k in sys.argv:
            lst.append(k)
            self.ids.msglbl.text += '\n'+k
    #
    def user_data_dir_wr(self):
        user_data_dir = App.get_running_app().user_data_dir
        self.ids.msglbl.text= 'App.get_running_app().user_data_dir: '+user_data_dir
        if not os.path.exists(user_data_dir):
            os.mkdir(user_data_dir)
            self.ids.msglbl.text += '\n created'
        else: 
            self.ids.msglbl.text += '\n exists'
            with open(user_data_dir+'/kivy3_UD.txt', 'w') as kf:
                kf.write('*** Hi stranger! UD Message from LKL Kivy. Dated: ' + dtStamp())
                self.ids.msglbl.text += '\n test file is created'
    #
    def read_UD_file(self):
        user_data_dir = App.get_running_app().user_data_dir
        test_file = user_data_dir+'/kivy3_UD.txt'
        self.ids.msglbl.text= test_file
        if not os.path.exists(test_file):
            self.ids.msglbl.text += ' does not exist'
        else: 
            self.ids.msglbl.text += ' exists: \n'
            with open(test_file, 'r') as kf:
                self.ids.msglbl.text += '\n'+kf.readline()
            ftp_store(test_file)
            self.ids.msglbl.text += '\n'+'File message is stored on FTP server in a HTML publication space.'
            self.ids.msglbl.text += '\n'+'Check out:'
            self.ids.msglbl.text += '\n'+PyParams['Ftp']['PublicLink']
            Clipboard.copy(PyParams['Ftp']['PublicLink'])
            self.popFtp = Popup(title='Below URL link is copied to Clipboard already, \nplease check it out in a Browser', 
                    content=Label(text='\n'+ PyParams['Ftp']['PublicLink']),
                    size_hint=(None, None), size=(500, 100))
            self.popFtp.open()
            # self.popup.dismiss()
    #
    def storage_dir_wr(self):
        if Platform != 'android': 
            self.ids.msglbl.text= 'Storage does not exists on '+Platform    
            return
        storage_dir = os.environ["ANDROID_STORAGE"]+'/kivy/kivy3'
        self.ids.msglbl.text= 'os.environ["ANDROID_STORAGE"]: '+storage_dir
        if not os.path.exists(storage_dir):
            os.mkdir(storage_dir)
            self.ids.msglbl.text += ' created'
        else: 
            self.ids.msglbl.text += ' exists'
            with open(storage_dir+'/kivy3_ST.txt', 'w') as kf:
                kf.write('*** Hi stranger! ST Message from LKL Kivy. Dated: ' + dtStamp())
                self.ids.msglbl.text += '\n test file is created'
    #
    def read_ST_file(self):
        if Platform != 'android': 
            self.ids.msglbl.text= 'Storage does not exists on '+Platform    
            return
        storage_dir = os.environ["ANDROID_STORAGE"]+'/kivy/kivy3'
        test_file = storage_dir+'/kivy3_ST.txt'
        self.ids.msglbl.text= test_file
        if not os.path.exists(test_file):
            self.ids.msglbl.text +=  ' does not exist'
        else: 
            self.ids.msglbl.text += ' exists: \n'
            with open(test_file, 'r') as kf:
                self.ids.msglbl.text += '\n'+kf.readline()
            ftp_store(test_file)
            self.ids.msglbl.text += '\n'+'File message is stored on FTP server in a HTML publication space.'
            self.ids.msglbl.text += '\n'+'check out:'
            self.ids.msglbl.text += '\n'+PyParams['Ftp']['PublicLink']
            Clipboard.copy(PyParams['Ftp']['PublicLink'])
            self.popFtp = Popup(title='Below URL link is copied to Clipboard already, \nplease check it out in a Browser', 
                    content=Label(text='\n'+ PyParams['Ftp']['PublicLink']),
                    size_hint=(None, None), size=(500, 100))
            self.popFtp.open()
            # self.popup.dismiss()

    def sd_dir_wr(self):
        if Platform != 'android': 
            self.ids.msglbl.text= 'SD Card does not exists on '+Platform    
            return
        sd_dir = os.environ["EXTERNAL_STORAGE"]+'/kivy/kivy3'
        self.ids.msglbl.text= sd_dir
        if not os.path.exists(sd_dir):
            os.mkdir(sd_dir)
            self.ids.msglbl.text += ' created'
        else: 
            self.ids.msglbl.text += ' exists'
            with open(sd_dir+'/kivy3_SD.txt', 'w') as kf:
                kf.write('*** Hi stranger! SD Message from LKL Kivy. Dated: ' + dtStamp())
                self.ids.msglbl.text += '\n test file is created'
    #
    def read_SD_file(self):
        if Platform != 'android': 
            self.ids.msglbl.text= 'SD Card does not exists on '+Platform    
            return
        sd_dir = os.environ["EXTERNAL_STORAGE"]+'/kivy/kivy3'
        test_file = sd_dir+'/kivy3_SD.txt'
        self.ids.msglbl.text= test_file
        if not os.path.exists(test_file):
            self.ids.msglbl.text += ' does not exist'
        else: 
            self.ids.msglbl.text += ' exists: \n'
            with open(test_file, 'r') as kf:
                self.ids.msglbl.text += '\n'+kf.readline()
            ftp_store(test_file)
            self.ids.msglbl.text += '\n'+'File message is stored on FTP server in a HTML publication space.'
            self.ids.msglbl.text += '\n'+'check out:'
            self.ids.msglbl.text += '\n'+PyParams['Ftp']['PublicLink']
            Clipboard.copy(PyParams['Ftp']['PublicLink'])
            self.popFtp = Popup(title='below URL link is copied to Clipboard already, \nplease check it out in Browser', 
                    content=Label(text='\n'+ PyParams['Ftp']['PublicLink']),
                    size_hint=(None, None), size=(500, 100))
            self.popFtp.open()
            # self.popup.dismiss()
    
    def colors_update(self):
        self.ids.msglbl.text= 'Colors update in PayParam file in progress\n'
        result = colors_RGBA_json_update(PyParams, PyParamFile)
        self.ids.msglbl.text+= result
        
    def int_ip_addr(self):
        self.ids.msglbl.text= 'Socket: Internal IP address: '+socket.gethostbyname(socket.gethostname())
    #
    def urlreq_get_headers(self, req, result):
        self.ids.msglbl.text ='UrlReq: Response Headers: '
        for key, value in req.resp_headers.items():
            s = f'{key}: {value}'
            self.ids.msglbl.text+='\n'+s
    #
    def ext_ip_addr(self):
        # self.ids.msglbl.text= 'urllib:'+urllib.request.urlopen('https://ident.me').read().decode('utf8')
        req = UrlRequest('https://ident.me', on_success= self.urlreq_get_headers, method='GET', decode='utf8') #https://ident.me https://httpbin.org/headers
        req.wait(.1)
        self.ids.msglbl.text+='\nUrlReq: External IP address: '+str(req.result)
    #
    def on_enter_ipinput(self, txtinp):
        self.ids.msglbl.text= 'Target: '+ txtinp.text #  self.ids.ipinput.text
        self.popip.dismiss()
        lst = port_scanner_threaded(txtinp.text)
        for l in lst:
            self.ids.msglbl.text += '\n'+l
    #
    def port_scan(self): 
        self.popip = Popup(title='Enter the host IP or Name to be scanned:', 
                    content=TextInput(text='www.', multiline=False, on_text_validate=self.on_enter_ipinput),
                    size_hint=(None, None), size=(500, 500))
                    # 
        self.popip.open()     
#
class kivy3App(App):
    title = 'Window: kivy3.03 by LKL@'+Platform
    kv_file = 'kivy3_kv_.kv'
    Window.clearcolor = Colors.get('LemonChiffon',(0,0,1,1)) 
    #
    def build(self):
        return ScreenManagement()
    #
    def on_exit_in_actionbar(self):
        App.get_running_app().stop()
    #
#
if __name__ == '__main__':
    Args = sys.argv
    logging.info('__main__ started: '+ dtStamp())
    kivy3App().run()
    logging.info('__main__  ended:  '+ dtStamp())
