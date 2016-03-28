__author__ = 'dknight'

print('server')

import socket
import threading


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 9002

s.bind(('127.0.0.1',port))
s.listen(5)

class rec_thread(threading.Thread):
    def __init__(self,c):
        threading.Thread.__init__(self)
        self.conn = c
        self.stopIt = False

    def mrecv(self):
        length = self.conn.recv(4)
        self.conn.send('200')                       # giving signal 200 to client sender
        msg = self.conn.recv (int(length))
        return msg

    def run(self):
        while not self.stopIt:
            msg=self.mrecv()                        # handling the connection of the client`s sender
            print('message from client ',msg)

def setconnection(con1,con2):
    dict={}

    state = con1.recv(6)
    con2.recv(8)
    if state == 'sender':
        dict['recv']=con1
        dict['send']=con2
    else:
        dict['recv']=con2
        dict['send']=con1
    return dict

def send_message(conn,msg):
    message_lenght = len(msg)
    if message_lenght >0:
        conn .send(str(message_lenght ))
        if(conn.recv(3)=='200'):
            conn.send(msg)
    else:
        print('no message for client')

                                                        # accepting the client connection.

(con1, (ip1,port1))  = s.accept()
(con2, (ip2,port2))  = s.accept()


dict = setconnection(con1,con2)

thr = rec_thread (dict['recv'])#threading.Thread(target=rec_thread, args=(dict['recv']))
thr.start()

try:
    while True:
        send_message(dict['send'],raw_input())
except:
    print('stoping the sending message')
thr.stopIt = True
send_message(dict['send'],'bye client ... ')
thr.conn.close()
s.close()