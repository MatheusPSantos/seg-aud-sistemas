#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives.serialization import load_ssh_public_key, load_ssh_private_key
from ast import literal_eval


chave_privada = None
chave_publica = None
chave_publica_servidor = None
chave_publica_servidor_bytes = None
class Server(threading.Thread):
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        global chave_privada, chave_publica, chave_publica_servidor, chave_publica_servidor_bytes
        lis = []
        lis.append(self.receive)

        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                try:
                    s = item.recv(2048)
                    if s != '':
                        mensagem_descriptografada = chave_privada.decrypt(
                            s,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        print("<<< " + mensagem_descriptografada.decode())
                except:
                    traceback.print_exc(file=sys.stdout)
                    break


class Client(threading.Thread):

    def connect(self, host, port):
        #self.sock.connect((host, port))
        self.sock.connect(("localhost", 5535))
    def client(self, host, port, msg):
        sent = self.sock.send(msg)
        # print "Sent\n"

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # try:
        #     host = input("Enter the server IP \n>>")
        #     port = int(input("Enter the server Destination Port\n>>"))

        # except EOFError:
        #     print("Error")
        #     return 1
        print("Connecting\n")
        s = ''
        host = "localhost"
        port = 5535
        self.connect(host, port)
        print("Connected\n")
        receive = self.sock
        
        global chave_publica_servidor_bytes
        chave_publica_servidor_bytes = receive.recv(2048)        
        print("recebeu a chave publica do server ...")
        global chave_publica_servidor
        chave_publica_servidor = load_ssh_public_key(chave_publica_servidor_bytes, default_backend())

        user_name = input("Enter the User Name to be Used\n>>")
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")
        srv.start()

        global chave_privada
        chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        global chave_publica
        chave_publica = chave_privada.public_key()


        self.chave_publica_bytes = chave_publica.public_bytes(
            encoding=_serialization.Encoding.OpenSSH,
            format=_serialization.PublicFormat.OpenSSH
        )
        self.client(host, port, b"[handshake]:"+self.chave_publica_bytes)

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
            
            mensagem_cifrada = chave_publica_servidor.encrypt(
                data, padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
            ))            
            payload = {"key": self.chave_publica_bytes, "cifrado": mensagem_cifrada}
            self.client(host, port, payload.__str__().encode())
        return (1)


if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()