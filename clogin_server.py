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
            enviar_mensajes(missatge)   
        except:
            pass

def enviar_mensajes(mss):
    mss = mss.decode()
    if "protocol:sortir:socketsecret" in mss:
        index_nom_a_enviar = mss.index("-")
        nom_a_enviar = mss[0:index_nom_a_enviar]
        index_nom_verificacio_user = mss.index("_")
        nom_verificacio_user = mss[index_nom_verificacio_user+1:]
        missatge_enviar = mss[index_nom_a_enviar+1:index_nom_verificacio_user]
        indice_nombre_cliente = nombre_clientes.index(nom_a_enviar)
        connexion_enviar_mensaje = socket_id_clientes[indice_nombre_cliente]
        try:
            connexion_enviar_mensaje.send("{},{}".format(nom_verificacio_user,missatge_enviar).encode())
        except:
            pass
    else:
        index_eliminar_client = mss.index(",")
        nom_del_usuari_eliminar = mss[index_eliminar_client+1:]
        index_si = nombre_clientes.index(nom_del_usuari_eliminar)
        socket_id_clientes.pop(index_si)
        print("{} a marxat del xat".format(nombre_clientes[nom_del_usuari_eliminar]))
        nombre_clientes.pop(index_si)


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
        
