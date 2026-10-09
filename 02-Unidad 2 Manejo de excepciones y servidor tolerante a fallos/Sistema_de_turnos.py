import socket
import threading

#Variables globales
turno_actual = 0
candado_turno = threading.Lock()

#TCP 
def tomar_turno(conexion, direccion):
    global turno_actual
    global candado_turno
    with conexion:
        datos = conexion.recv(1024).decode("utf-8").strip()
        
        if datos.startswith("TURNO>"):
            partes = datos.split(">")
            apodo = partes[1] if len(partes) > 1 else "Anónimo"
            
            with candado_turno:
                turno_actual += 1
                turno_asignado = turno_actual
                
            respuesta = f"turno>{turno_asignado}\n"
            conexion.sendall(respuesta.encode("utf-8"))
            print(f"[TCP] Se asignó el turno {turno_asignado} a '{apodo}' ({direccion})")
        else:
            conexion.sendall("ERROR>Protocolo no reconocido\n".encode("utf-8"))


#TCP: Escucha la puerta 5000
def atender_tcp():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()
    print("Servidor TCP (Turnos) escuchando en el puerto 5000...")
    
    while True:
        conexion, direccion = servidor.accept()
        #Cada vez que llega alguien, creamos un hilo exclusivamente para esa persona
        hilo_cliente = threading.Thread(target=tomar_turno, args=(conexion, direccion), daemon=True)
        hilo_cliente.start()


#UDP Escucha la puerta 5001
def atender_udp():
    global turno_actual
    
    servidor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_udp.bind(("0.0.0.0", 5001))
    print("Servidor UDP (Consultas) escuchando en el puerto 5001...")
    
    while True:
        datos, direccion = servidor_udp.recvfrom(1024)
        mensaje = datos.decode("utf-8").strip()
        
        if mensaje == "CUANTOS":
            with candado_turno:
                total = turno_actual
            
            respuesta = f"van>{total}\n"
            servidor_udp.sendto(respuesta.encode("utf-8"), direccion)
            print(f"[UDP] Consulta de {direccion} respondida. Van {total}.")

def main():
    hilo_tcp = threading.Thread(target=atender_tcp, daemon=True)
    hilo_udp = threading.Thread(target=atender_udp, daemon=True)
    
    #Los arrancamos
    hilo_tcp.start()
    hilo_udp.start()
    
    #Esperamos a que terminen
    hilo_tcp.join()
    hilo_udp.join()

if __name__ == "__main__":
    main()