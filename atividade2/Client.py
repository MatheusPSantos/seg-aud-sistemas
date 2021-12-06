#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import _serialization, hashes
import json


chave_servidor_str = ""

class Server(threading.Thread):
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        lis = []
        lis.append(self.receive)
        global chave_servidor_str
        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                try:
                    s = item.recv(2048)                    
                    if s != '':                        
                        if s.decode().__contains__("chave_servidor="):
                            chave_servidor_str = s.decode().split("chave_servidor=")[1]
                        
                        chunk = s
                        print(chunk.decode() + '\n>>')
                except:
                    traceback.print_exc(file=sys.stdout)
                    break


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
        self.charve_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.chave_publica = self.charve_privada.public_key()
        print("Connected\n")
        user_name = input("Enter the User Name to be Used\n>>")
        receive = self.sock
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")

        p_bytes=self.chave_publica.public_bytes(encoding=_serialization.Encoding.OpenSSH, format=_serialization.PublicFormat.OpenSSH)        
        ##self.client(host, port, self.chave_publica.public_bytes(encoding=_serialization.Encoding.OpenSSH, format=_serialization.PublicFormat.OpenSSH))
        srv.start()
        print("chave server ", chave_servidor_str)
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
            
            
            payload = []
            payload.append(p_bytes)
            payload.append(data)

            print('payload >> ', payload.__str__())
            
            self.client(host, port, payload.__str__().encode())
        return (1)


if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()