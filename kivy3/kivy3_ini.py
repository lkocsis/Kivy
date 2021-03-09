# https://www.w3schools.com/colors/colors_names.asp
# https://www.w3schools.com/colors/colors_groups.asp
#$ CWD
import os, sys, datetime, ftplib
PyFilePath  = os.path.dirname(os.path.abspath(__file__))
PyPrgName0   = os.path.basename(__file__).split('.')[0].split('_')[0]
os.chdir(PyFilePath)
#$ Kivy
from kivy.core.window import Window
WindowSizes = Window.size
#$ Log
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.logger import logging
from kivy.utils import platform
# 
#$ PyParam
import json
def pyParam(pyFilePath, pyPrgName0):
    pyParamFile    = pyFilePath +'/'+ pyPrgName0 +'.json'
    pyParams = {}
    if os.path.exists(pyParamFile):
        with open(pyParamFile+'', 'r', encoding='utf-8') as f:
                pyParams = json.loads(f.read())
                logging.info('Parameters JSON is loaded: '+pyParamFile)
                c = pyParams["Comments"]
                for j in c: 
                    logging.info(j+": "+ c[j], mode='p')
    else: 
        logging.info('Parameters JSON is NOT loaded since does not exist: ' +pyParamFile)
    return pyParams, pyParamFile
PyParams, PyParamFile = pyParam(PyFilePath, PyPrgName0)
#$ Global Variables
Platform = platform
Spinner1Items= PyParams['Spinner1Items']
Colors = PyParams['Colors']
# ColorsInLines = str([f' {k:10}: {v} \n' for k,v in Colors.items()])
Ftp = PyParams['Ftp']
def ftp_store(data):
    with ftplib.FTP(Ftp['Host'], Ftp['User'], Ftp['Pwd']) as ftp:
        ftp.cwd(Ftp['Folder'])
        lst = []
        if type(data) != list:  lst.append(data)
        else:                   lst = data 
        for l in lst:
            with open(l, 'rb') as file:
                ftp.storbinary('STOR '+Ftp['Folder']+os.path.basename(l), file)      
#
def dtStamp(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def timeStamp(): return datetime.datetime.now().strftime("%H:%M:%S")
def dateStamp(): return datetime.datetime.now().strftime("%Y-%m-%d")
def shortDate(): return datetime.datetime.now().strftime("%Y%m%d")
#
def rgba_float(color_name, alpha):
    from webcolors import name_to_rgb_percent
    rgba = []
    for e in name_to_rgb_percent(color_name):
        rgba.append(float(e.strip('%'))/100)
    rgba.append(alpha)    
    return rgba
#
def object_dir_list(obj):
    lst = []
    w = dict([attr, getattr(obj, attr)] for attr in dir(obj) if not attr.startswith('_'))
    for k, v in w.items():
        lst.append(str('{:>17} {:<3} {:}'.format(k, ':', v))[:1023])
    return lst
# 
def dir_list(d):
    lst = []
    for k,v in d.items():
        lst.append(str('{:>17} {:<3} {:}'.format(k, ':', v))[:1023])
    return lst
#
logging.info (
    f'*** LOG STARTS for {PyFilePath}/{PyPrgName0} on PLATFORM "{platform}" at [{dtStamp()}]')
#
if __name__=='__main__':

    print('THIS IS: ' + __file__)
    arg = sys.argv[1] if len(sys.argv)>1 else ''
    print('NOW RUNING THE MAIN PY FILE INSTEAD')
    os.system('python main.py '+ arg )

#################################################################################################
# from kivy.config import Config    
# Window.size = (1000,500)
# Window.clearcolor = rgba_float('BlanchedAlmond',1) # RGBA
# Config.set ("kivy", "log_dir", PyFilePath+'/log')
# Config.set ("kivy", "log_level", "info")
# Config.set ("kivy", "log_name", PyPrgName0+".log")
# Config.write ()
"""
    for i,e in enumerate(object_dir_list(Config)): logging.info(f'{i:4}: {e}')
    for i,e in enumerate(object_dir_list(App)): logging.info(f'{i:4}: {e}')
    for i,e in enumerate(object_dir_list(App.user_data_dir)): logging.info(f'{i:4}: {e}')
    for i,e in enumerate(object_dir_list(App.directory)): logging.info(f'{i:4}: {e}')

    try:
        print('NOW RUNING '+ __file__+' FILE INSTEAD')
        os.system('python '+__file__.replace('_ini','')+' ' + arg )
    except:
        try:
            print('NOW RUNING THE MAIN PY FILE INSTEAD')
            print("Error:", sys.exc_info()[0])
            os.system('python main.py '+ arg )
        except:
            print("Error:", sys.exc_info()[0])
"""
"""
ScrollView:
    do_scroll_x: False
    do_scroll_y: True

    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        padding: 10, 10
        text:
            'really some amazing text\n' * 100
"""
"""
    colorNames= [k for k in Colors.keys() ]
    with open('Colors_rgba.json','w') as fh:
        fh.write('    "Colors" : {')
        first = True
        space = '                                          '
        for cn in colorNames:
            if first: 
                fh.write('\n')
                first=False
            else:
                fh.write(',\n')
            fh.write(f'        "{cn}"{space[:(17-len(cn))]}: {list(rgba_float(cn, 1))}')
        fh.write('\n    }\n')
    for i,e in enumerate(dir_list(Colors)): logging.info(f'{i:4}: {e}')
"""