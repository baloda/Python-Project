__author__ = 'dknight'
print('cleint')
                                            # maximum size of meassage can not be more than 4 digits ... 4096
                                            # in each message first we are sending message lenght using send_message() function...
                                            # threaded mrecv() function will receive  the length and send a message 200 to client and than message is printed ..
import socket
import threading

host = socket.gethostname()
port = 9002
class rec_thread(threading.Thread):
    def __init__(self, con):
        threading.Thread.__init__(self)
        self.conn = con
        self.stopIt = False


    def mrecv(self):
        length= self.conn.recv(4)                       # maximum data size
        self.conn.send('200')                           # giving signal 200 to server`s sender
        msg = self.conn.recv (int(length))              # getting message of length from buffer socket connection.
        return msg                                      # return message

    def run(self):
        while not self.stopIt:
            msg=self.mrecv()                            # handling the connection of the server`s sender
            print('message from server', msg)              # printing message


def send_message(conn,msg):
    message_lenght = len(msg)
    if message_lenght >0:
        conn .send(str(message_lenght ))
        if(conn.recv(3)=='200'):
            conn.send(msg)
    else:
        print('no message for server')

soc1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc1.connect(('127.0.0.1',port))
soc1.send('sender')                                     # telling server i m the sender of the message

soc2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc2.connect(('127.0.0.1',port))
soc2.send('receiver')                                   # telling server i m the receiver of the message


thr = rec_thread(soc2)                                      #threading.Thread(target=client, args=(soc2))
thr.start()
try:
    while True:
        send_message(soc1,raw_input())
except:
    print('closing')

thr.stopIt = True
send_message(soc1,'bye server .........')
thr.conn.close()
soc1.close()
soc2.close()