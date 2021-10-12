#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback

from cryptography.fernet import Fernet

connection_key = ''
class Server(threading.Thread):

    def initialise(self, receive):
        self.receive = receive

    def run(self):
        global connection_key
        lis = []
        lis.append(self.receive)

        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                if connection_key != '':
                    fernet = Fernet(connection_key)               
                try:
                    s = item.recv(1024)
                    if s != '':
                        chunk = s
                        if connection_key != '':
                            decoded = fernet.decrypt(chunk)                        
                            print('\t' + decoded.decode() + '\n>>')
                        else:
                            print(chunk.decode() + '\n>>')
                except:
                    traceback.print_exc(file=sys.stdout)
                    break
    
    # def saveKey(self, key):
    #     connection_key = key
    #     return connection_key

class Client(threading.Thread):

    def connect(self, host, port):
        self.sock.connect((host, port))

    def client(self, host, port, msg):
        sent = self.sock.send(msg)
        # print "Sent\n"

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host = input("Enter the server IP \n>>")
            port = int(input("Enter the server Destination Port\n>>"))
        except EOFError:
            print("Error")
            return 1

        print("Connecting\n")
        s = ''
        self.connect(host, port)
        print("Connected\n")
        user_name = input("Enter the User Name to be Used\n>>")
        receive = self.sock
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")
        srv.start()
        global connection_key
        connection_key = receive.recv(1024)
        fernet = Fernet(connection_key)

        while 1:
            # print "Waiting for message\n"
            msg = input('>>')
            if msg == 'exit':
                break
            if msg == '':
                continue
            # print "Sending\n"
            msg = user_name + ': ' + msg
            data = msg.encode()
            self.client(
                host, 
                port, 
                fernet.encrypt(data)
            )
        return (1)


if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()