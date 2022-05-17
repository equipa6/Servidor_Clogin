import socket
import threading

ip = "172.21.233.33"
port = 8432

srv_clogin = socket.socket()
srv_clogin.bind((ip, port))
srv_clogin.listen(1000)
clientes_list = []

def recibir_mensajes():
    while True:
        try:
            missatge = srv_clogin.recv(1024)
            enviar_mensajes(missatge)
        except:
            pass

def enviar_mensajes(mss):
    mss = mss.decode()
    indice_coma = mss.index(",")
    nom_usuari = mss[0:indice_coma]
    for i in clientes_list:
        if i[0] == nom_usuari:
            i[1].send(mss.encode())
            break

ejecutar_funcio = threading.Thread(recibir_mensajes)
ejecutar_funcio.start()

while True:
    try:
        connexio, address = srv_clogin.accept()
        nom_client = connexio.recv(1024)
        informacio_usuari = [nom_client.decode(), connexio]
        clientes_list.append(informacio_usuari)
        print("S'ha connectat l'usuari {} amb la següent IP --> {}".format(nom_client.decode(), address))
        connexio.send("Correct".encode())
    except:
        pass