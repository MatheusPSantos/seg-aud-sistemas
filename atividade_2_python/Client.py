#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback

from cryptography.fernet import Fernet

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

chave_privada = ""
chave_publica = ""
chave_publica_externa = ""

class Server(threading.Thread):

    def initialise(self, receive):
        self.receive = receive
        global chave_publica
        global chave_privada
        global chave_publica_externa

        chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        chave_publica = chave_privada.public_key()
        

    def run(self):
        lis = []
        lis.append(self.receive)

        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                print('entra no for')
                try:
                    s = item.recv(1024)
                    print("s ", s)
                    if s != '':
                        print('entra no if')
                        global chave_privada
                        chunk = s
                        print('entra aqui')
                        print('chunk ', chunk)
                        # texto_pleno = chave_privada.decrypt(
                        #     chunk,
                        #     padding.OAEP(
                        #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        #         algorithm=hashes.SHA256(),
                        #         label=None
                        #     )
                        # )
                        print('passou aqui, >> ', chunk)
                        # print('\t' + texto_pleno + '\n>>')
                    else:
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
        print("Connected\n")
        user_name = input("Enter the User Name to be Used\n>>")
        receive = self.sock
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")
        srv.start()

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
            
            global chave_publica
            global chave_publica_externa

            texto_cifrado = chave_publica.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            self.client(
                host,
                port,
                texto_cifrado
            )
        return (1)


if __name__ == '__main__':
    print("Starting client")
    
    cli = Client()
    cli.start()