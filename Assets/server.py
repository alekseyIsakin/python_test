# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

import UdpComms as U
import time
import json
import random as rnd
js = {}
with open(r'mods/test/entity_list.json','r') as f:
    js = json.loads(''.join(f.readlines()))

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001,
                  enableRX=True, suppressWarnings=True)

map_request = 'map'
map_acknowledge = 'map received'
map_close = 'map close'
step = 'step'
send_bots = 'new state'



print("Server has been started")

# Send this string to other application
sock.SendData("Server has been started")

class SimpleByteConverter:
    def toByteArray(value:int, bite=4) -> bytearray:
        return value.to_bytes(length=bite,byteorder='little',signed = False)
    def fromByteArray(value:bytearray) -> int:
        return int.from_bytes(value, byteorder='little',signed = False)


class Bot():
    def __init__(s, ID, pos):
        s.id = ID
        s.pos = pos

class AbstractState():
    def check_msg(s, msg):
        raise BaseException("Unrealized function")
    def do_job(s):
        raise BaseException("Unrealized function")



class WaitForConnect(AbstractState):
    def check_msg(s, msg):
        
        if msg == None: return s
        print(f'[{msg}]    ')
        print(f'| |       |')
        print(f'|\./      |')
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
        s.sended_map = bytes()

    def check_msg(s, msg):
        if s.try_cnt <= 0:
            return ClosingConnection()

        if msg == map_acknowledge:
            return StepProcessor(s.sended_map)
        return s
    
    def do_job(s):
        if (time.time() - s.start >= s.resend_time):
            s.sendMap('')
            s.try_cnt -= 1
            s.start = time.time()
    
    def sendMap(s, map):
        with open(r'mods/test/map.mp', 'br') as f:
            bt = f.read()
            sock.SendDataBytes(bt)
            s.sended_map = bt
            print('|/`\         |')
            print('| |  send map|')



class StepProcessor(AbstractState):
    def __init__(s, bt_map):
        cursor = 1

        h = int.from_bytes(bt_map[cursor+0:cursor+4], byteorder='little',signed = False)
        w = int.from_bytes(bt_map[cursor+4:cursor+8], byteorder='little',signed = False)
        f = int.from_bytes(bt_map[cursor+8:cursor+12], byteorder='little',signed = False)
        cursor += 12 + h*w*f

        s.bots = []
        cursor += 1

        if(bt_map[cursor] == js['BOT']):
            cursor += 1
            while (cursor < len(bt_map)):
                cursor += 1
                ID = int.from_bytes(bt_map[cursor+0:cursor+4], byteorder='little',signed = False)
                cursor += 1
                x = int.from_bytes(bt_map[cursor+4:cursor+8], byteorder='little',signed = False)
                y = int.from_bytes(bt_map[cursor+8:cursor+12], byteorder='little',signed = False)
                z = int.from_bytes(bt_map[cursor+12:cursor+16], byteorder='little',signed = False)
                s.bots.append(Bot(ID,[x,y,z]))
                cursor += 16
                if bt_map[cursor] == js['ENDBOT']:
                    break

        s._map = bt_map

    def check_msg(s, msg):
        if msg == map_request or msg == map_close:
            return ClosingConnection()
        return s
    
    def get_bots_data(s) -> bytearray:
        bots_dt = bytearray()
        for b in s.bots:
            path = []
            for i in range(4):
                path.append(rnd.randint(2,13))
                path.append(rnd.randint(2,13))
            
            bot = bytearray()
            
            bot.append(bytes([js["BOTID"]]))
            bot.append(SimpleByteConverter.toByteArray(b.ID))
            bot.append(bytes([js["BOTPATH"]]))
            
            len(path)
            bots_dt.append()

    def do_job(s):
        sock.SendData(send_bots)
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
