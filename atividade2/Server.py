#! /usr/bin/env python

from re import M
import socket
import sys
from time import sleep
import traceback
import threading
import select
from ast import literal_eval
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend, openssl
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives.serialization import load_ssh_public_key, load_ssh_private_key


SOCKET_LIST = []
TO_BE_SENT = []
SENT_BY = {}
HOST_PUBLIC_KEY = {}
chave_privada = None
chave_publica = None
chave_publica_bytes = None
chave_publica_externa = None
class Server(threading.Thread):

    def init(self):
        global chave_privada, chave_publica, chave_publica_bytes
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.bind(('', 5535))
        self.sock.listen(2)
        SOCKET_LIST.append(self.sock)
        chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        chave_publica = chave_privada.public_key()
        chave_publica_bytes = chave_publica.public_bytes(_serialization.Encoding.OpenSSH, _serialization.PublicFormat.OpenSSH)
        print("Server started on port 5535")

    def run(self):
        
        while 1:
            read, write, err = select.select(SOCKET_LIST, [], [], 0)
            for sock in read:
                if sock == self.sock:
                    sockfd, addr = self.sock.accept()
                    print(str(addr))
                    SOCKET_LIST.append(sockfd)
                    print(SOCKET_LIST[len(SOCKET_LIST) - 1])
                    global chave_publica_bytes
                    sockfd.sendall(chave_publica_bytes) # envia a chave publica assim que alguem se conecta

                else:
                    try:
                        s = sock.recv(2048)
                        if s == '':
                            continue
                        if s.decode().__contains__("[handshake]:"):
                            # quando alguem se conecta, faz o handshake e guarda a chave e o host dono dela                            
                            HOST_PUBLIC_KEY[str(sock.getpeername())] = s.decode().split('[handshake]:')[1]
                        else:
                            TO_BE_SENT.append(s)
                            SENT_BY[s] = (str(sock.getpeername()))
                    except:
                        print(str(sock.getpeername()))


class handle_connections(threading.Thread):
    def run(self):
        while 1:
            read, write, err = select.select([], SOCKET_LIST, [], 0)
            for items in TO_BE_SENT:
                item_dict = literal_eval(items.decode())
                # descriptografa aqui
                global chave_privada
                texto_pleno_cliente = chave_privada.decrypt(
                    item_dict["cifrado"],
                    padding.OAEP(
                        padding.MGF1(algorithm=hashes.SHA256()),
                        hashes.SHA256(),
                        None
                    )
                )

                texto_cifrado_server = b""
                for s in write:
#                    print("s ", s)                    
                    try:
                        if (str(s.getpeername()) == SENT_BY[items]):
                            print("Ignoring %s" % (str(s.getpeername())))
                            continue
                        #precisa iterar sobre a banco de chaves publicas, encriptar para cada chave e enviar para cada uma
                        for key in HOST_PUBLIC_KEY:
                            try:
                                print(str(key))
                                print("----")
                                print(str(s.getpeername()))
                                if(str(s.getpeername()) == str(key)):
                                    print("ignorar a criptografia para ", (str(key)))
                                else:
                                    global chave_publica_externa
                                    chave_publica_externa = load_ssh_public_key(
                                        HOST_PUBLIC_KEY[key].encode(),
                                        default_backend()
                                    )
                                    texto_cifrado_server = chave_publica_externa.encrypt(
                                        texto_pleno_cliente,
                                        padding.OAEP(
                                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                            algorithm=hashes.SHA256(),
                                            label=None
                                        )
                                    )
                                    print('enviando para %s'%str(key))
                                    s.sendto(texto_cifrado_server, literal_eval(key))
                                    
                            except:
                                traceback.print_exc(file=sys.stdout)

                        #print("Sending to %s" % (str(s.getpeername())))
                        #s.send(items)

                    except:
                        traceback.print_exc(file=sys.stdout)

                TO_BE_SENT.remove(items)
                del (SENT_BY[items])

if __name__ == '__main__':
    srv = Server()
    srv.init()
    srv.start()
    print(SOCKET_LIST)
    handle = handle_connections()
    handle.start()