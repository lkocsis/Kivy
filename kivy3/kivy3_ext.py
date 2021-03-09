import os, sys, re, time, json
import socket, datetime, threading
from queue import Queue
from kivy3_ini import Platform, Colors, rgba_float
if Platform != 'android':
    import pandas as pd
    import numpy  as np
#
def prime_numbers_ext(nr):
    def isprime(n):
        return re.compile(r'^1?$|^(11+)\1+$').match('1' * n) is None
    primeLst= [x for x in range(nr) if isprime(x)]
    return primeLst
#
def fibonacci_numbers_ext(nr):
        result = []
        a, b = 0, 1
        while b < nr:
            result.append(format(b, ',').replace(',',' '))
            a, b = b, a+b                                   # !!!
        return result

def list_to_string_segmented(title, lst, length):
    tmp= title+'\n'
    j = len(title)
    for l in lst:
            tmp = tmp + str(l)+', '
            j += len(str(l))+2
            if j>=length: 
                tmp = tmp+'\n'
                j = 0
    return tmp[:-2]
#
def port_scanner_threaded(target):
    lst=[]
    min= 10
    max= 1024
    ###
    def portscan(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex((targetIP, port))
            with print_lock:
                if result == 0:
                        print(f"Port {port:0>5}: 	 Open")
                        lst.append(f"Port {port:0>5}: 	 Open")
                else:   print(f'port {port:0>5}',end='\r', flush=True)
            sock.close()
        except KeyboardInterrupt:
            lst.append("You pressed Ctrl+C")
            return lst # sys.exit()
        except Exception as e:
            lst.append('Error: '+ str(e))
            return lst
    def threader():
        while True:
            port = q.get()
            portscan(port)
            q.task_done()
    #
    try:
        targetIP = socket.gethostbyname(target)
        lst.append ('Starting scan on host: ' + targetIP)
    except Exception as e:
        lst.append('Error: '+ str(e))
        return lst
    #
    socket.setdefaulttimeout(0.15)
    print_lock = threading.Lock()
    q = Queue()
    startTime = datetime.datetime.now()
    
    for x in range(100):
        t = threading.Thread(target = threader)
        t.daemon = True
        t.start()
    
    for port in range(min, max+1):
        q.put(port)
    
    q.join()
    endTime= datetime.datetime.now()
    lst.append('Time taken:'+ str(endTime - startTime))
    ###
    return lst
#
def colors_RGBA_json_update(param, parfile):
    if Platform == 'android':
        # from android.storage import primary_external_storage_path
        # dir = primary_external_storage_path()
        # download_dir_path = os.path.join(dir, 'Download')
        return 'Colors update is not yet available on Android'
    else: return 'Colors update is in test mode yet'

    try:
        df = pd.read_excel('Colors147.xlsx', sheet_name='Colors147')
        for e in df.ColorName:
            param['Colors'][e] = rgba_float(e,1)
        with open(parfile, 'w', encoding='utf-8') as f:
            json.dump(param, f, indent=4)
        Colors = param['Colors']
        return str(Colors)        
    #
    except Exception as e:
        return str(e)
    #
    
#
if __name__=='__main__':
    print('THIS IS: ' + __file__)
    arg = sys.argv[1] if len(sys.argv)>1 else ''
    print('NOW RUNING THE MAIN PY FILE INSTEAD')
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system('python main.py '+ arg )