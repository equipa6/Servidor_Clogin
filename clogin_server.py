import socket
import threading

ip = "172.21.233.33"
port = 8432

srv_clogin = socket.socket()
srv_clogin.bind((ip, port))
srv_clogin.listen(1000)
clientes_list = []

