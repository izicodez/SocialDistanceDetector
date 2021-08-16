from new_server import SDD
import socket, threading
from flask import Flask, render_template, Response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip='127.0.0.1'
print('HOST IP:', host_ip)
port = 9995
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at", socket_address)

count=-1



def engine(client_socket, addr, count):
    if count == 0:
        a = SDD(addr,client_socket, '127.0.1.1')
        a.show_client()
        a.run_flask()
    elif count==1:
        b = SDD(addr,client_socket, '127.0.1.2')
        b.show_client()
        b.run_flask()


while True:
    count+=1
    client_socket, addr = server_socket.accept()

    threading.Thread(target = engine ,args = (client_socket, addr,count)).start()
    print('aaaaaaaaaaaaa')
