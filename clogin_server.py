import socket
import threading

ip = "172.21.233.33"
port = 8432

srv_clogin = socket.socket()
srv_clogin.bind((ip, port))
srv_clogin.listen(100)
socket_id_clientes = []
nombre_clientes = []

def recibir_mensajes(conn, addr):
    while True:
        try:
            missatge = conn.recv(1024)
            print("{} --> {}".format(missatge.decode(),addr[0]))
            enviar_mensajes(missatge)   
        except:
            pass

def enviar_mensajes(mss):
    mss = mss.decode()
    indice_coma = mss.index(",")
    nom_usuari = mss[0:indice_coma]
    missatge_enviar = mss[indice_coma+1:]
    indice_nombre_cliente = nombre_clientes.index(nom_usuari)
    connexion_enviar_mensaje = socket_id_clientes[indice_nombre_cliente]
    try:
        connexion_enviar_mensaje.send(missatge_enviar.encode())
    except:
        pass

while True:
    connexio, address = srv_clogin.accept()
    nom_client = connexio.recv(1024)
    socket_id_clientes.append(connexio)
    nombre_clientes.append(nom_client.decode())
    print("S'ha connectat l'usuari {} amb la IP --> {}".format(nom_client.decode(), address))
    connexio.send("Correct".encode())  
    ejecutar_funcio = threading.Thread(target=recibir_mensajes, args=(connexio, address))
    ejecutar_funcio.daemon = True
    ejecutar_funcio.start()
        
