# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

import UdpComms as U
import time
from enum import Enum

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001,
                  enableRX=True, suppressWarnings=True)

map_request = 'map'
map_acknowledge = 'map received'
map_close = 'map close'
step = 'step'



print("Server has been started")

# Send this string to other application
sock.SendData("Server has been started")


class STAT(Enum):
    EMPTY = 1
    START_SESSION = 2
    MAP_REQUEST = 3
    NEW_STEP = 4
    END_SESSION = 5


class AbstractState():
    def check_msg(s, msg):
        raise BaseException("Unrealized function")
    def do_job(s):
        raise BaseException("Unrealized function")


class WaitForConnect(AbstractState):
    def check_msg(s, msg):
        
        if msg == None: return s
        print(f'[{msg}]')
        print(f'| |       |')
        print(f'|\./      | ')
        if msg == map_request:
            return OpenConnection()
        return s
    def do_job(s):
        pass



class OpenConnection(AbstractState):
    def __init__(s):
        s.start = 0
        s.resend_time = 5
        s.try_cnt = 5

    def check_msg(s, msg):
        if s.try_cnt <= 0:
            return ClosingConnection()

        if msg == map_acknowledge:
            return StepProcessor()
        return s
    
    def do_job(s):
        if (time.time() - s.start >= s.resend_time):
            s.sendMap('')
            s.try_cnt -= 1
            s.start = time.time()
    
    def sendMap(s, map):
        with open(r'mods/test/map.mp', 'br') as f:
            sock.SendDataBytes(f.read())
            print('|/`\         |')
            print('| |  send map|')



class StepProcessor(AbstractState):
    def check_msg(s, msg):
        if msg == map_request or msg == map_close:
            return ClosingConnection()
        return s
    
    def do_job(s):
        sock.SendData(step)
        pass



class ClosingConnection(AbstractState):
    def __init__ (s):
        s.close_cnt = 4
    def check_msg(s, msg):
        if s.close_cnt <= 0:
            return WaitForConnect()
        return s
    def do_job(s):
        sock.SendData(map_close)
        s.close_cnt -= 1
        pass



class StateMachine:
    def __init__(s):
        s.change_status(WaitForConnect())

    def read_msg(s, msg):
        st = s.machine.check_msg(msg)

        if (s.machine != st):
            s.change_status(st)

    def change_status(s, new_status):
        print(f"new status {type(new_status)}")
        s.machine = new_status

    def do_job(s):
        s.machine.do_job()




machine = StateMachine()
time_f = 0

while True:
    time_f = time.time()
    data = sock.ReadReceivedData()  # read data

    if data != None:  # if NEW data has been received since last ReadReceivedData function call
        data = data.replace('\u200b', '')
    
    machine.read_msg(data)
    machine.do_job()
    time.sleep(.33)
    print(f'{time.time() - time_f:.4f}\r', end='')
