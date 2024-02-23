# server_status_checker.py
# server_status_checker_cython.pyx

import sys, os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QMenuBar
from PySide6.QtGui import QIcon, QFont, QAction
from PySide6.QtCore import Qt, QThread, Signal, QRunnable, QThreadPool
import requests, socket, ping3
from urllib.parse import unquote
import time, ast, datetime
from flask import Flask, request
import gc
from pygame import mixer
###########Sound_MsgBox_Handler############
snd_msg_box_trigger = False
################SoundHandler###############
sound_L3_47 = True
sound_L3_48 = True
sound_L4_47 = True
sound_L4_48 = True
sound_L7_47 = True
sound_L7_48 = True
sound_L3_47_48 = True ## All servers are down
sound_L4_47_48 = True ## All servers are down
sound_L7_47_48 = True ## All servers are down
########################################
setting_file = 'Server_option.txt'
setting_file_content_array=[]
py2js_log_list = []
###########DEFUALT###########
option_socket = 'False'
option_request = 'False'
server_47 = '127.0.0.1'
server_48 = '127.0.0.1'
port_47 = 8080
port_47_sokcet = 5000
port_48 = 8181
port_48_sokcet = 5000
log_switch = 'False'
socket_view = 'False'
py2js = False
py2js_port = 9000
font_size = 12
timeout_L3 = 2
timeout_L4 = 2
timeout_L7 = 10
##############################
#######################################################################Setting_Handler#####################################################################
def open_setting(filename):
    print('Loading_Settings')
    with open(os.getcwd() + os.sep + filename, "r") as file:
        setting_file_content = file.read()
        setting_file_content_arr = setting_file_content.split('\n')
        for i in setting_file_content_arr:
            setting_file_content_array = i.replace(' ','').split('=')
            if(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='option_socket' and setting_file_content_array[0]=='option_socket'):
                global option_socket
                if setting_file_content_array[1]!='False' or setting_file_content_array[1]!='True':
                    setting_file_content_array[1]=='False'
                option_socket = ast.literal_eval(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='option_request'):
                global option_request
                if setting_file_content_array[1]!='False' or setting_file_content_array[1]!='True':
                    setting_file_content_array[1]=='False'
                option_request = ast.literal_eval(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='server_47'):
                global server_47
                if setting_file_content_array[1]=='':
                    setting_file_content_array[1]=='127.0.0.1'
                server_47 = setting_file_content_array[1]
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='server_48'):
                global server_48
                if setting_file_content_array[1]=='':
                    setting_file_content_array[1]=='127.0.0.1'
                server_48 = setting_file_content_array[1]
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='port_47'):
                global port_47
                if setting_file_content_array[1]=='':
                    setting_file_content_array[1]==80   
                port_47 = int(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='port_48'):
                global port_48
                if setting_file_content_array[1]=='':
                    setting_file_content_array[1]==80
                port_48 = int(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='log_switch'):
                global log_switch # Server_Log on_off
                if setting_file_content_array[1]!='False' or setting_file_content_array[1]!='True':
                    setting_file_content_array[1]=='False'
                log_switch = ast.literal_eval(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='socket_view'):
                global socket_view # socket_view on_off
                if setting_file_content_array[1]!='False' or setting_file_content_array[1]!='True':
                    setting_file_content_array[1]=='False'
                socket_view = ast.literal_eval(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='py2js'):
                global py2js # Python_info to Chromium_base_JS
                if setting_file_content_array[1]!='False' or setting_file_content_array[1]!='True':
                    setting_file_content_array[1]=='False'
                py2js = ast.literal_eval(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='py2js_port'):
                global py2js_port # Python_info to Chromium_base_JS
                if not isinstance(int(setting_file_content_array[1]), int) :
                    setting_file_content_array[1]=='8181'
                py2js_port = ast.literal_eval(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='font_size'):
                global font_size
                if not isinstance(int(setting_file_content_array[1]), int) :
                    setting_file_content_array[1]=='12'
                font_size = int(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='timeout_L3'):
                global timeout_L3
                if not isinstance(int(setting_file_content_array[1]), int) :
                    setting_file_content_array[1]=='1'
                timeout_L3 = int(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='timeout_L4'):
                global timeout_L4
                if not isinstance(int(setting_file_content_array[1]), int) :
                    setting_file_content_array[1]=='1'
                timeout_L4 = int(setting_file_content_array[1])
                print(setting_file_content_array)
            elif(len(setting_file_content_array) == 2 and setting_file_content_array[0]=='timeout_L7'):
                global timeout_L7
                if not isinstance(int(setting_file_content_array[1]), int) :
                    setting_file_content_array[1]=='10'
                timeout_L7 = int(setting_file_content_array[1])
                print(setting_file_content_array)
        print("Setting Loaded")
    file.close()
##########################################################<Log_Handler>##############################################################

# server_log_L3 
def server_log_L3(server, server_response):
    try:
        if ('failed' in server_response):
            f = open(os.getcwd() + os.sep + "log" + os.sep + "server_log_L3", "a")
            f.write(str(server) +'   '+ str(server_response) +'   '+ str(datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')) + '\n')
            f.close()
    except Exception as e:
            if ('failed' in server_response):
                f = open(os.getcwd() + os.sep + "log" + os.sep + "server_log_L3", "a")
                f.write(str(e) + '\n')
                f.close()
# server_log_L4 
def server_log_L4(server, server_response):
    try:
        if ('failed' in server_response):
            f = open(os.getcwd() + os.sep + "log" + os.sep + "server_log_L4", "a")
            f.write(str(server) +'   '+ str(server_response) +'   '+ str(datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')) + '\n')
            f.close()
    except Exception as e:
        if ('failed' in server_response):
            f = open(os.getcwd() + os.sep + "log" + os.sep + "server_log_L4", "a")
            f.write(str(e) + '\n')
            f.close()

# server_log_L7  
def server_log_L7(server, server_response):
    try:
        if ('failed' in str(server_response)):
            f = open(os.getcwd() + os.sep + "log" + os.sep + "server_log_L7", "a")
            f.write(str(server) +'   '+ str(server_response) +'   '+ str(datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')) + '\n')
            f.close()
    except Exception as e:
         if ('failed' in str(server_response)):
            f = open(os.getcwd() + os.sep + "log" + os.sep + "server_log_L7", "a")
            f.write(str(e) + '\n')
            f.close()       

# python_2_js
def python_2_js(server,port,server_response): # auto-refresh (delete - create) # logic => if failed store if on clear
    try:
        global py2js_log_list
        if ((not f'[{server}:{server_response}]' in str(py2js_log_list)) and ('failed' in f'[{server}:{server_response}]') and (not 'WinError' in f'[{server}:{server_response}]')):
            py2js_log_list.append(f'[{server}:{server_response}]')

        if server in str(py2js_log_list) and 'Ping:' in f'[{server}:{server_response}]':
            py2js_log_list = [item for item in py2js_log_list if server not in item or 'L3_Ping failed:' not in item]
            
        if server in str(py2js_log_list) and f'[Port:{port}]' in f'[{server}:{server_response}]' and 'ms' in f'[{server}:{server_response}]':
            py2js_log_list= [item for item in py2js_log_list if server not in item or f'[Port:{port}]: L4_Ping failed' not in item]

        if server in str(py2js_log_list) and 'status' in f'[{server}:{server_response}]' and 'ms' in f'[{server}:{server_response}]':
            py2js_log_list = [item for item in py2js_log_list if server not in item or 'L7_failed to get data' not in item]
        
        #     #py2js_log_list.append(f'[{server}:{server_response}]')
        # if(len(py2js_log_list)>=11):
        #     py2js_log_list = []
    except Exception as e:
        print(e)
########################################################################################################################
###########################################<Main_LIBRARY>######################################################################
def ping(host, timeout):
    host = host.replace('http://', '').replace('https://', '').split('/')[0]
    xijinpingping = ping3.ping(host, unit='ms', timeout=timeout)
    try:
        if xijinpingping == None:
            return 'L3_Ping failed'
        else:
            return f'Ping: {int(xijinpingping)}ms'
    except ping3.errors as e:
        return f'L3_Ping failed {str(e)}'
def socket_ping(host, port, timeout):
    host = host.replace('http://', '').replace('https://', '').split('/')[0]
    if ':' in host:
        host = host.split(':')
        port = host[1]
        host = host[0]
    sock_start_time = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            socket.timeout(2)
            sock_end_time = time.time()
            sock_time_spent = int((sock_end_time - sock_start_time)*1000)
            return f' [Port:{port}]: {sock_time_spent}ms'
    except (socket.timeout, socket.error) as e:
        return f' [Port:{port}]: L4_Ping failed {str(e)}'
    
def http_https_ping(url, timeout):
    try:
        if not('http://' or 'https://') in url:
            url = 'http://'+ url
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        end_time = time.time()
        response_time_spent = int((end_time - start_time)*1000)
        status = response.status_code
        if status <= 399:
            return f'[status: {status}] {response_time_spent}ms'
        elif status>= 400:
            return f'[status: {status}] L7_failed to get data {response_time_spent}ms'
    except Exception as e:
        return f'[status: 500++] L7_failed to get data'
###############################################<<<<<L3>>>>>#################################################
class ServerChecker_L3_47_Thread(QThread):
    status_signal_47 = Signal(bool)
    def run(self):
        global ping_L3_47
        while ServerStatusChecker.trigger:
            try:
                ping_L3_47 = ping(server_47, timeout_L3)
                self.status_signal_47.emit(not 'failed' in ping_L3_47)
                if log_switch and ('failed' in ping_L3_47):
                    server_log_L3(server_47, ping_L3_47)
                if py2js:
                    python_2_js(server_47, port_47, ping_L3_47)
                time.sleep(1)
            except Exception as e:
                self.status_signal_47.emit(False)
                if log_switch:
                    server_log_L3(server_47, f'L3_Ping failed: {str(e)}')
                if py2js:
                    python_2_js(server_47, port_47, f'L3_Ping failed: {str(e)}')

class ServerChecker_L3_48_Thread(QThread):
    status_signal_48 = Signal(bool)
    def run(self):
        global ping_L3_48
        while ServerStatusChecker.trigger:
            try:
                ping_L3_48 = ping(server_48, timeout_L3)
                self.status_signal_48.emit(not 'failed' in ping_L3_48)
                if log_switch and ('failed' in ping_L3_48):
                    server_log_L3(server_48, ping_L3_48)
                if py2js:
                    python_2_js(server_48, port_48, ping_L3_48)
                time.sleep(1)
            except Exception as e:
                    self.status_signal_48.emit(False)
                    if log_switch:
                        server_log_L3(server_48, f'L3_Ping failed: {str(e)}')
                    if py2js:
                        python_2_js(server_48, port_48, f'L3_Ping failed: {str(e)}')
#############################################################################################################
####################################<<<<<<<<<<<<L4+Socket>>>>>>>>>>>>####################################
class ServerChecker_L4_47_Thread(QThread):
    status_signal_47 = Signal(bool)
    def run(self):
        global ping_L4_47
        while ServerStatusChecker.trigger:
            try:
                ping_L4_47 = socket_ping(server_47,port_47, timeout_L4)
                self.status_signal_47.emit(not 'failed' in ping_L4_47)
                if log_switch and ('failed' in ping_L4_47):
                    server_log_L4(server_47, ping_L4_47)
                if py2js:
                    python_2_js(server_47, port_47, ping_L4_47)
                time.sleep(1)
            except Exception as e:
                    self.status_signal_47.emit(False)
                    if log_switch:
                        server_log_L4(server_47, f'L4_Ping failed: {str(e)}')
                    if py2js:
                        python_2_js(server_47, port_47, f'L4_Ping failed: {str(e)}')

class ServerChecker_L4_47_socket_Thread(QThread):
    status_signal_47_socket = Signal(bool)
    def run(self):
        global ping_L4_47
        while ServerStatusChecker.trigger:
            try:
                ping_L4_47 = socket_ping(server_47, port_47_sokcet, timeout_L4)
                self.status_signal_47_socket.emit(not 'failed' in ping_L4_47)
                if log_switch and ('failed' in ping_L4_47):
                    server_log_L4(server_47, ping_L4_47)
                if py2js:
                    python_2_js(server_47, port_47_sokcet, ping_L4_47)
                time.sleep(1)
            except Exception as e:
                    self.status_signal_47_socket.emit(False)
                    if log_switch:
                        server_log_L4(server_47, f'L4_Ping failed: {str(e)}')
                    if py2js:
                        python_2_js(server_47, port_47_sokcet, f'L4_Ping failed: {str(e)}')

class ServerChecker_L4_48_Thread(QThread):
    status_signal_48 = Signal(bool)
    def run(self):
        global ping_L4_48
        while ServerStatusChecker.trigger:
            try:
                ping_L4_48 = socket_ping(server_48, port_48, timeout_L4)
                self.status_signal_48.emit(not 'failed' in ping_L4_48)
                if log_switch and ('failed' in ping_L4_48):
                    server_log_L4(server_48, ping_L4_48)
                if py2js:
                    python_2_js(server_48, port_48 ,ping_L4_48)
                time.sleep(1)
            except Exception as e:
                self.status_signal_48.emit(False)
                if log_switch:
                    server_log_L4(server_48, f'L4_Ping failed: {str(e)}')
                if py2js:
                    python_2_js(server_48, port_48, f'L4_Ping failed: {str(e)}')

class ServerChecker_L4_48_socket_Thread(QThread):
    status_signal_48_socket = Signal(bool)
    def run(self):
        global ping_L4_48
        while ServerStatusChecker.trigger:
            try:
                ping_L4_48 = socket_ping(server_48, port_48_sokcet, timeout_L4)
                self.status_signal_48_socket.emit(not 'failed' in ping_L4_48)
                if log_switch and ('failed' in ping_L4_48):
                    server_log_L4(server_48, ping_L4_48)
                if py2js:
                    python_2_js(server_48, port_48 ,ping_L4_48)
                time.sleep(1)
            except Exception as e:
                self.status_signal_48_socket.emit(False)
                if log_switch:
                    server_log_L4(server_48, f'L4_Ping failed: {str(e)}')
                if py2js:
                    python_2_js(server_48, port_48, f'L4_Ping failed: {str(e)}')
#####################################################################################################
########################################<<<<<<<<<<L7>>>>>>>>>>>########################################
class ServerChecker_L7_47_Thread(QThread):
    status_signal_47 = Signal(bool)
    def run(self):
        global ping_L7_47
        while ServerStatusChecker.trigger:
            try:
                ping_L7_47 = http_https_ping(server_47, timeout_L7)
                self.status_signal_47.emit(not 'failed' in ping_L7_47)
                if log_switch and ('failed' in ping_L7_47):
                    server_log_L7(server_47, f'L7_failed to get data {ping_L7_47}')
                if py2js:
                    python_2_js(server_47, port_47, ping_L7_47)
            except Exception as e:
                self.status_signal_47.emit(False)
                if log_switch:
                    server_log_L7(server_47, f'L7_failed to get data {e}')
                if py2js:
                    python_2_js(server_47, port_47, f'L7_failed to get data {e}')
            time.sleep(1)
class ServerChecker_L7_48_Thread(QThread):
    status_signal_48 = Signal(bool)
    def run(self):
        global ping_L7_48
        while ServerStatusChecker.trigger:
            try:
                ping_L7_48 = http_https_ping(server_48, timeout_L7)
                self.status_signal_48.emit(not 'failed' in ping_L7_48)
                if log_switch and ('failed' in ping_L7_48):
                    server_log_L7(server_48, f'L7_failed to get data {ping_L7_48}')
                if py2js:
                    python_2_js(server_48, port_48, ping_L7_48)
            except Exception as e:
                self.status_signal_48.emit(False)
                if log_switch:
                    server_log_L7(server_48, f'L7_failed to get data {e}')
                if py2js:
                    python_2_js(server_48, port_48, f'L7_failed to get data {e}')
            time.sleep(1)
#####################################<py2js_server>########################################
            
class py2js_server_core(QThread):
    js2py_Extension = []
    js2py_Internal = []
    previous_data = ''
    py2js_run_sound = Signal()
    def __init__(self):
        super(py2js_server_core, self).__init__()
        self.app_py2js = Flask(__name__)
        self.app_py2js.add_url_rule("/connect", 'connect_js2py', self.connect_js2py, methods=['POST'])
        self.app_py2js.add_url_rule("/endpoint", 'send_py2js', self.send_py2js, methods=['POST'])
        self.app_py2js.add_url_rule("/log", 'send_py2js_log', self.send_py2js_log, methods=['POST'])
        self.keep_running = True
        
    def run(self):
        try:
            self.app_py2js.run(host='127.0.0.1', port=py2js_port)         
        except Exception as e:
            print(f'Error in Flask server: {str(e)}')
        print('Flask server terminated')
    
    def connect_js2py(self): # handler 
        try:
            gc.collect()
            data = request.get_json()
            self.js2py_Extension = self.js2py_Extension[:2]
            self.js2py_Internal = self.js2py_Internal[:2]
            if ('asking' in str(self.js2py_Internal) and 'connect' in str(self.js2py_Extension)):
                return ({'message': f'Python and Extension are successfully communicated {data}'})
            elif 'asking' in str(data):
                self.js2py_Internal.append(data)
                #js2py_Extension = [item for item in js2py_Extension if 'connect' not in item]
                return ({f'message': f'Waiting for the data {data}'})
            elif 'connect' in str(data):
                self.js2py_Extension.append(data)
                #js2py_Internal = [item for item in js2py_Internal if 'asking' not in item]
                return ({'message': f'Data has been received successfully from Extension {data}'})
            else:
                self.js2py_Extension = []
                self.js2py_Internal = []
                return ({f'message': f'Data not recieved {data}'})
        except Exception as e:
            return ({f'message': f'error {str(e)}'})
    #app_py2js.add_url_rule('/connect', 'connect_js2py', connect_js2py, methods=['POST'])
    
    # json_data_list_py2js = []
    # cleaner_py2js = 0
    def send_py2js(self):
        try:
            gc.collect()
            # global json_data_list_py2js
            data = request.get_json()
            # json_data_list_py2js.append(data)
            # global cleaner_js2py
            # cleaner_py2js = cleaner_py2js + 1
            # if cleaner_py2js == 7:
            #     cleaner_py2js = 0
            #     json_data_list_py2js = json_data_list_py2js[:3]
            if 'sync_py2js' in str(data):
                return ({'message': f'js2py'})
            elif 'Server_47_2_Server_48'  in str(data):
                self.sound_play('server_47')
                return ({'message': f'Server_47_2_Server_48'})
            elif 'Server_48_2_Server_47'  in str(data):
                self.sound_play('server_48')
                return ({'message': f'Server_48_2_Server_47'})
            elif 'Servers_down' in str(data):
                self.sound_play('server_47_48_down')
                return ({'message': f'Servers_down'})
            elif '47_server_up' in str(data):
                self.sound_play('47_restore_up')
                return ({'message': f'47_server_up'})
            elif '48_server_up' in str(data):
                self.sound_play('48_restore_up')
                return ({'message': f'48_server_up'})
            else:
                return ({f'message': f'Data not recieved'})
        except Exception as e:
            return ({f'message': f'error {str(e)}'})
    #app_py2js.add_url_rule('/endpoint', 'send_py2js', send_py2js, methods=['POST'])
   
    def send_py2js_log(self):
        try:
            gc.collect()
            data = request.get_data()
            if 'py2js_data' in str(data):
                #print('py2js_data'+str(previous_data))
                self.previous_data = unquote(str(data))
                return ({'message': f'{self.previous_data}'})
            if 'js2py_log':
                #print('js2py_log'+str(previous_data))
                return self.previous_data
        except Exception as e:
            return ({f'message': f'error {str(e)}'})
    #app_py2js.add_url_rule('/log', 'send_py2js_log', send_py2js_log, methods=['POST'])

###########################<Alert_sound_handler>#############################    
    def sound_play(self, server):
        mixer.init()
        if server == 'server_47':
            mixer.music.stop()
            mixer.music.load('Server47_To_Server48.mp3')
            mixer.music.play()
        elif server == 'server_48':
            mixer.music.stop()
            mixer.music.load('Server48_To_Server47.mp3')
            mixer.music.play()
        elif server == 'server_47_48_down':
            mixer.music.stop()
            mixer.music.load('Server47_48_Down.mp3')
            mixer.music.play(-1)
            self.py2js_run_sound.emit()
        elif server == '47_restore_up':
            mixer.music.stop()
            mixer.music.load('47_restore_up.mp3')
            mixer.music.play()
        elif server == '48_restore_up':
            mixer.music.stop()
            mixer.music.load('48_restore_up.mp3')
            mixer.music.play()
        
    def stop(self):
        self.keep_running = False
        self.terminate()
    
###########################py2js_server#####################################
class py2js_server(QThread):  ### Trhead link to the main to start
    py2js_run = Signal(bool, str)
    def __init__(self):
        super(py2js_server, self).__init__()
        self.flask_thread= None
    def run(self):
        try:
            self.flask_thread = py2js_server_core()
            self.flask_thread.start()
            self.py2js_run.emit(True, 'Waiting_Response')
            print('Flask server started')
        except Exception as e:
            self.py2js_run.emit(False, str({e}))
            print(f"Error starting Flask server: {e}")
    
    def stop(self):
            try:
                if self.flask_thread:
                    self.flask_thread.stop()
                    self.flask_thread.wait()
                self.terminate()
                self.wait()
                self.py2js_run.emit(False, 'Terminated')
                print('Flask server terminated')
            except Exception as e:
                print(e)
   
##############################Inernal_py2py##############################    

class pyserver_Thread(QThread):
    py2js_run = Signal(bool, str)
    def run(self):
        url_connect = f'http://localhost:{py2js_port}/connect'
        url_endpoint = f'http://localhost:{py2js_port}/endpoint'
        url_log = f'http://localhost:{py2js_port}/log'
        while ServerStatusChecker.trigger:
            data = {'asking': True} 
            data_endpoint = {'sync_py2js': True}         
            try:
                gc.collect()
                response_connect = requests.post(url_connect, json=data)
                result_connect = response_connect.json()
                response_endpoint = requests.post(url_endpoint, json=data_endpoint)
                result_endpoint = response_endpoint.json()
                if 'js2py' in str(result_endpoint):
                    global py2js_log_list
                    #print(str(py2js_log_list))
                    result_endpoint = requests.post(url_log, data={"message": f'py2js_data: {str(py2js_log_list)}'})
                if 'successfully' in str(result_connect) or 'js2py' in str(result_connect):
                    self.py2js_run.emit(True, f'{result_connect["message"]}')
                if 'Waiting' in str(result_connect):
                    self.py2js_run.emit(True, f'{result_connect["message"]}')
                else: 
                    self.py2js_run.emit(True, f'{result_connect["message"]}')
            except Exception as e:
                self.py2js_run.emit(False, f'Error connecting to the server {str(e)}')
            time.sleep(1)
    def stop(self):
        try:
            self.terminate()
            self.quit()
            self.wait()
        except Exception as e:
            print(e)


################################################<GUI_HANDLER>################################################
class ServerStatusCheckerRunnable(QRunnable):
    def __init__(self, main_window):
        super(ServerStatusCheckerRunnable,self).__init__()
        self.main_window = main_window
    def run(self):
        ServerStatusChecker.trigger = not ServerStatusChecker.trigger
        try:
            if ServerStatusChecker.trigger:
                self.main_window.check_button.setEnabled(False)
                self.main_window.thread_L3_47.start()
                self.main_window.thread_L3_48.start()
                self.main_window.thread_L4_47.start()
                self.main_window.thread_L4_48.start()
                if socket_view:
                    self.main_window.thread_L4_47_socket.start()
                    self.main_window.thread_L4_48_socket.start()
                self.main_window.thread_L7_47.start()
                self.main_window.thread_L7_48.start()
                if py2js:
                    self.main_window.py2js_server.start()
                    self.main_window.py2js_server_py.start()
                self.main_window.check_button.setEnabled(True)
                self.main_window.check_button.setText('Click to Stop')
            elif not ServerStatusChecker.trigger:
                self.main_window.check_button.setEnabled(False)
                self.main_window.check_button.setText('Stopping_L3_thread')
                self.main_window.thread_L3_47.quit()
                self.main_window.thread_L3_47.wait()
                self.main_window.thread_L3_48.quit()
                self.main_window.thread_L3_48.wait()
                self.main_window.check_button.setText('Stopping_L4_thread')
                self.main_window.thread_L4_47.quit()
                self.main_window.thread_L4_47.wait()
                self.main_window.thread_L4_48.quit()
                self.main_window.thread_L4_48.wait()
                if socket_view:
                    self.main_window.thread_L4_47_socket.quit()
                    self.main_window.thread_L4_47_socket.wait()
                    self.main_window.thread_L4_48_socket.quit()
                    self.main_window.thread_L4_48_socket.wait()
                self.main_window.check_button.setText('Stopping_L7_thread')
                self.main_window.thread_L7_47.quit()
                self.main_window.thread_L7_47.wait()
                self.main_window.thread_L7_48.quit()
                self.main_window.thread_L7_48.wait()
                if py2js:
                    self.main_window.check_button.setText('Closing Server')
                    self.main_window.py2js_server.stop()
                    self.main_window.py2js_server_py.stop()
                self.main_window.check_button.setEnabled(True)
                self.main_window.check_button.setText('Check Server Status')
                mixer.music.stop()
        except Exception as e:
            print(e)
################################ Main Window #############################################################

class ServerStatusChecker(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('monitor.ico')) 
        self.initUI()
        self.threadpool_Thread = QThreadPool() #start_stop main processes
        self.threadpool_pyserver = QThreadPool() #pyserver

    def checkServerStatus(self):
        try:
            runnable = ServerStatusCheckerRunnable(self)
            self.threadpool_Thread.start(runnable)
        except Exception as e:
            print(e)

    def initUI(self):
        menubar = QMenuBar(self)
        help_menu = menubar.addMenu("Help")
        reference_action = QAction("Library Used", self)
        reference_action.triggered.connect(self.show_reference_dialog)
        help_menu.addAction(reference_action)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        layout = QVBoxLayout(self)
        if py2js:
            self.status_label_py2js = QLabel(f'py2js is ({py2js} = True) http://127.0.0.1:{py2js_port}', self)
            self.status_label_py2js.setAlignment(Qt.AlignCenter)
            self.py2js_server = py2js_server()
            self.py2js_server.py2js_run.connect(self.updateStatus_py2js)
            self.py2js_server_core = py2js_server_core()
            self.py2js_server_core.py2js_run_sound.connect(self.show_servers_are_down)
            self.py2js_server_py = pyserver_Thread()
            self.py2js_server_py.py2js_run.connect(self.updateStatus_py2js)
            layout.addWidget(self.status_label_py2js)
        # elif py2js == False:
        #     self.status_label_py2js = QLabel(f'py2js is ({py2js} = OFF)', self)
        #     self.status_label_py2js.setAlignment(Qt.AlignCenter)

        self.status_label_L3_47 = QLabel(f'Server_47_L3_PING: {server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}', self)
        self.status_label_L3_47.setAlignment(Qt.AlignCenter)
        self.status_label_L3_48 = QLabel(f'Server_48_L3_PING: {server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}', self)
        self.status_label_L3_48.setAlignment(Qt.AlignCenter)

        self.status_label_L4_47 = QLabel(f'Server_47_L4_PORT_PING: {server_47.replace("http://","").replace("https://","").split("/")[0]}', self)
        self.status_label_L4_47.setAlignment(Qt.AlignCenter)
        self.status_label_L4_48 = QLabel(f'Server_48_L4_PORT_PING: {server_48.replace("http://","").replace("https://","").split("/")[0]}', self)
        self.status_label_L4_48.setAlignment(Qt.AlignCenter)
        if socket_view:
            self.status_label_socket_L4_47 = QLabel(f'Server_47_L4_Socket_PORT_PING: {server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_47_sokcet}', self)
            self.status_label_socket_L4_47.setAlignment(Qt.AlignCenter)
            self.status_label_socket_L4_48 = QLabel(f'Server_48_L4_Socket_PORT_PING: {server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_48_sokcet}', self)
            self.status_label_socket_L4_48.setAlignment(Qt.AlignCenter)

        self.status_label_L7_47 = QLabel(f'Server_47_L7_HTTP: {server_47}', self)
        self.status_label_L7_47.setAlignment(Qt.AlignCenter)
        self.status_label_L7_48 = QLabel(f'Server_48_L7_HTTP: {server_48}', self)
        self.status_label_L7_48.setAlignment(Qt.AlignCenter)

        self.check_button = QPushButton('Check Server Status', self)
        self.check_button.clicked.connect(self.checkServerStatus)
        self.L3_H = QLabel('===========L3(ICMP)===========', self)
        self.L4_H = QLabel('\n===========L4(TCP)===========', self)
        self.L7_H = QLabel('\n===========L7(HTTP)===========', self)
        self.L3_H.setAlignment(Qt.AlignCenter)
        self.L4_H.setAlignment(Qt.AlignCenter)
        self.L7_H.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.L3_H)
        layout.addWidget(self.status_label_L3_47)
        layout.addWidget(self.status_label_L3_48)
        layout.addWidget(self.L4_H)
        layout.addWidget(self.status_label_L4_47)
        layout.addWidget(self.status_label_L4_48)
        if socket_view:
            layout.addWidget(self.status_label_socket_L4_47)
            layout.addWidget(self.status_label_socket_L4_48)
        layout.addWidget(self.L7_H)
        layout.addWidget(self.status_label_L7_47)
        layout.addWidget(self.status_label_L7_48)
        layout.addWidget(self.check_button)
        layout.setMenuBar(menubar)
        self.setLayout(layout)
        self.setMaximumSize(1000, 450)
        self.thread_L3_47 = ServerChecker_L3_47_Thread()
        self.thread_L3_47.status_signal_47.connect(self.updateStatus_L3_47)
        self.thread_L3_48 = ServerChecker_L3_48_Thread()
        self.thread_L3_48.status_signal_48.connect(self.updateStatus_L3_48)
        self.thread_L4_47 = ServerChecker_L4_47_Thread()
        self.thread_L4_47.status_signal_47.connect(self.updateStatus_L4_47)
        self.thread_L4_48 = ServerChecker_L4_48_Thread()
        self.thread_L4_48.status_signal_48.connect(self.updateStatus_L4_48)
        self.thread_L7_47 = ServerChecker_L7_47_Thread()
        self.thread_L7_47.status_signal_47.connect(self.updateStatus_L7_47)
        self.thread_L7_48 = ServerChecker_L7_48_Thread()
        self.thread_L7_48.status_signal_48.connect(self.updateStatus_L7_48)
        if socket_view:
            self.thread_L4_47_socket = ServerChecker_L4_47_socket_Thread()
            self.thread_L4_47_socket.status_signal_47_socket.connect(self.updateStatus_L4_47_socket)
            self.thread_L4_48_socket = ServerChecker_L4_48_socket_Thread()
            self.thread_L4_48_socket.status_signal_48_socket.connect(self.updateStatus_L4_48_socket)

    trigger = False
#######################Server_Down_sound_handler##############################
    def show_servers_are_down(self):
            global snd_msg_box_trigger
            if not snd_msg_box_trigger:
                snd_msg_box_trigger = True
                # app = QApplication.instance()
                # if app is None:
                #     app = QApplication(sys.argv)
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Critical)
                msg_box.setWindowTitle("Servers are DOWN")
                msg_box.setWindowIcon(QIcon('monitor.ico')) 
                msg_box.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
                msg_box.setText("47 and 48 are down!\nClick 'OK' or 'X' to stop alert")
                msg_box.setStyleSheet("font-weight: bold; Color : darkorange")
                msg_box.exec_()
                if msg_box.clickedButton():
                    snd_msg_box_trigger = False
                    mixer.music.stop()
##############################Mebubar#######################################
    def show_about_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About_Server_Viewer")
        msg_box.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setText(f"""Automatic_Switching_Program_under_Multi_Servers_(ASPS)'
                Contact(Bug_Report): ljs_fr@nate.com""")
        msg_box.setStyleSheet("font-weight: bold; color : darkcyan")
        msg_box.exec()
    def show_reference_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Library_Used")
        msg_box.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setText("Python3.11.7\n(ping3, socket, response, requests, PyQt5, nuitka, pygame)")
        msg_box.exec() 

#######################UpdateStatus#############################

    def updateStatus_L3_47(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_L3_47.setText(f'[{server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}: {ping_L3_47}]')
                self.status_label_L3_47.setStyleSheet('color: green')
            else:
                self.status_label_L3_47.setText(f'({server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}) is down')
                self.status_label_L3_47.setStyleSheet('color: red')
        except Exception as e:
                self.status_label_L3_47.setText(f'[{server_47}]: {str(e)}')
                self.status_label_L3_47.setStyleSheet('color: yellow')

    def updateStatus_L3_48(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_L3_48.setText(f'[{server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}: {ping_L3_48}]')
                self.status_label_L3_48.setStyleSheet('color: green')
            else:
                self.status_label_L3_48.setText(f'({server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}) is down')
                self.status_label_L3_48.setStyleSheet('color: red')
        except Exception as e:
            self.status_label_L3_48.setText(f'[{server_48}]: {str(e)}')
            self.status_label_L3_48.setStyleSheet('color: yellow')

    def updateStatus_L3_47(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_L3_47.setText(f'[{server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}: {ping_L3_47}]')
                self.status_label_L3_47.setStyleSheet('color: green')
            else:
                self.status_label_L3_47.setText(f'({server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}) is down')
                self.status_label_L3_47.setStyleSheet('color: red')
        except Exception as e:
                self.status_label_L3_47.setText(f'[{server_47}]: {str(e)}')
                self.status_label_L3_47.setStyleSheet('color: yellow')

    def updateStatus_L4_47_socket(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_socket_L4_47.setText(f'[{server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_47_sokcet} {ping_L4_47}]')
                self.status_label_socket_L4_47.setStyleSheet('color: green')
            else:
                self.status_label_socket_L4_47.setText(f'({server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_47_sokcet}) is down')
                self.status_label_socket_L4_47.setStyleSheet('color: red')
        except Exception as e:
            self.status_label_socket_L4_47.setText(f'[{server_47}]: {str(e)}')
            self.status_label_socket_L4_47.setStyleSheet('color: yellow')

    def updateStatus_L3_48(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_L3_48.setText(f'[{server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}: {ping_L3_48}]')
                self.status_label_L3_48.setStyleSheet('color: green')
            else:
                self.status_label_L3_48.setText(f'({server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}) is down')
                self.status_label_L3_48.setStyleSheet('color: red')
        except Exception as e:
            self.status_label_L3_48.setText(f'[{server_48}]: {str(e)}')
            self.status_label_L3_48.setStyleSheet('color: yellow')

    def updateStatus_L4_48_socket(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_socket_L4_48.setText(f'[{server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_48_sokcet} {ping_L4_48}]')
                self.status_label_socket_L4_48.setStyleSheet('color: green')
            else:
                self.status_label_socket_L4_48.setText(f'({server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_48_sokcet}) is down')
                self.status_label_socket_L4_48.setStyleSheet('color: red')
        except Exception as e:
            self.status_label_socket_L4_48.setText(f'[{server_48}]: {str(e)}')
            self.status_label_socket_L4_48.setStyleSheet('color: yellow')

    def updateStatus_L4_47(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_L4_47.setText(f'[{server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_47} {ping_L4_47}]')
                self.status_label_L4_47.setStyleSheet('color: green')
            else:
                self.status_label_L4_47.setText(f'({server_47.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_47}) is down')
                self.status_label_L4_47.setStyleSheet('color: red')
        except Exception as e:
            self.status_label_L4_47.setText(f'[{server_47}]: {str(e)}')
            self.status_label_L4_47.setStyleSheet('color: yellow')

    def updateStatus_L4_48(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_L4_48.setText(f'[{server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_48} {ping_L4_48}]')
                self.status_label_L4_48.setStyleSheet('color: green')
            else:
                self.status_label_L4_48.setText(f'({server_48.replace("http://","").replace("https://","").split("/")[0].split(":")[0]}:{port_48}) is down')
                self.status_label_L4_48.setStyleSheet('color: red')
        except Exception as e:
            self.status_label_L4_48.setText(f'[{server_48}]: {str(e)}')
            self.status_label_L4_48.setStyleSheet('color: yellow')

    def updateStatus_L7_47(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_L7_47.setText(f'({server_47}): {ping_L7_47}')
                self.status_label_L7_47.setStyleSheet('color: green')
            else:
                self.status_label_L7_47.setText(f'({server_47}): {ping_L7_47}')
                self.status_label_L7_47.setStyleSheet('color: red')
        except Exception as e:
                self.status_label_L7_47.setText(f'({server_47}): {str(e)}')
                self.status_label_L7_47.setStyleSheet('color: yellow')


    def updateStatus_L7_48(self, is_reachable):
        try:
            if is_reachable:
                self.status_label_L7_48.setText(f'({server_48}): {ping_L7_48}')
                self.status_label_L7_48.setStyleSheet('color: green')
            else:
                self.status_label_L7_48.setText(f'({server_48}): {ping_L7_48}')
                self.status_label_L7_48.setStyleSheet('color: red')

        except Exception as e:
                self.status_label_L7_48.setText(f'({server_48}): {str(e)}')
                self.status_label_L7_48.setStyleSheet('color: yellow')

    def updateStatus_py2js(self, is_reachable, response):
            try:
                if is_reachable:
                    self.status_label_py2js.setText(f'py2js: {response}')
                    self.status_label_py2js.setStyleSheet('color: green')
                elif is_reachable == False:
                    self.status_label_py2js.setText(f'py2js: {response}')
                    self.status_label_py2js.setStyleSheet('color: red')

            except Exception as e:
                self.status_label_py2js.setText(f'py2js: {str(e)}')
                self.status_label_py2js.setStyleSheet('color: yellow')

###################################################################################################  
# def increase_font_size(app):
#     font = app.font()
#     font.setPointSize(font.pointSize() + 4)
#     app.setFont(font)

class HighDpiFix:
    def __init__(self):
        if sys.platform == 'win32':
            if hasattr(Qt, 'AA_EnableHighDpiScaling'):
                QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            # Enable DPI awareness on Windows Vista (6.0) and later
            if sys.getwindowsversion().major >= 6:
                try:
                    from ctypes import windll
                    windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
                except ImportError:
                    pass

if __name__ == '__main__':
    try:
        if not os.path.isdir(os.getcwd() + os.sep + 'log'):
            os.mkdir(os.getcwd() + os.sep + 'log')
        if not os.path.isfile(os.getcwd() + os.sep + setting_file):
            f = open(os.getcwd() + os.sep + setting_file, 'a')
            f.write('''option_socket=False
option_request=False
server_47=127.0.0.1
server_48=127.0.0.1
port_47 = 8080
port_47_sokcet = 5000
port_48 = 8181
port_48_sokcet = 5000
log_switch=False
socket_view =False
py2js=False
py2js_port=9000
font_size=12
timeout_L3=2
timeout_L4=2
timeout_L7=10
                     ''')
            f.close()
        open_setting(setting_file)
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText('Setting_file_missing')
        msg.setInformativeText('Setting_file_missing')
        msg.setWindowTitle('No_setting_file')
        msg.exec_()
    mixer.init()
    gc.collect()
    high_dpi_fix = HighDpiFix()
    app = QApplication(sys.argv)
    # increase_font_size(app)
    app.setFont(QFont('Arial', font_size, QFont.Weight.Light))
    mainWindow = ServerStatusChecker()
    mainWindow.setGeometry(100, 100, 400, 200)
    mainWindow.setWindowTitle('Server_viewer__ASPS')
    mainWindow.show()
    sys.exit(app.exec_())
