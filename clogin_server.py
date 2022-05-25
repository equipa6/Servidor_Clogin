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
            if missatge:
                missatge_val = missatge.decode()
                if "+" in missatge_val:
                    print("ha entrat")
                    index_eliminar_client = missatge_val.index("+")
                    eliminar_client(missatge_val[index_eliminar_client+1:])
                else:
                    enviar_mensajes(missatge)  
        except:
            pass

def eliminar_client(nom):
    global nombre_clientes
    global socket_id_clientes
    index_si = nombre_clientes.index(nom)
    socket_id_clientes.pop(index_si)
    print("{} a marxat del xat".format(nom))
    nombre_clientes.pop(index_si)
        
def enviar_mensajes(mss):
    mss = mss.decode()
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
        
