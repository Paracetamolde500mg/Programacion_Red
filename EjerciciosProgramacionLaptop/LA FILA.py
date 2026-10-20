import socket
import threading

#Contador global de turnos y cerrojo de exclusión mutua
contador_turnos = 0
lock = threading.Lock()

def atender_cliente_tcp(conexion, direccion):
    """Procesa las solicitudes TCP de turnos por cada cliente."""
    global contador_turnos
    try:
        buffer = ""
        while True:
            data = conexion.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8', errors='ignore')

            # Procesamiento de mensajes terminados en \n
            while '\n' in buffer:
                linea, buffer = buffer.split('\n', 1)
                linea = linea.strip()

                if linea.startswith("TURNO>"):
                    apodo = linea.split("TURNO>", 1)[1]
                    
                    #Incremento protegido con Lock
                    with lock:
                        contador_turnos += 1
                        turno_asignado = contador_turnos

                    respuesta = f"turno>{turno_asignado}\n"
                    conexion.sendall(respuesta.encode('utf-8'))
                    print(f"Turno {turno_asignado} asignado a '{apodo}' ({direccion})")
    except (ConnectionResetError, BrokenPipeError):
        print(f"Cliente {direccion} se desconectó intempestivamente.")
    except Exception as e:
        print(f"Error procesando cliente {direccion}: {e}")
    finally:
        conexion.close()

def servidor_tcp():
    """Hilo principal para aceptar conexiones TCP en el puerto 5000."""
    HOST = '0.0.0.0'
    PORT_TCP = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp:
        s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_tcp.bind((HOST, PORT_TCP))
        s_tcp.listen()
        print(f"Servidor de turnos escuchando en el puerto {PORT_TCP}...")

        while True:
            try:
                conexion, direccion = s_tcp.accept()
                hilo_tcp = threading.Thread(
                    target=atender_cliente_tcp,
                    args=(conexion, direccion),
                    daemon=True
                )
                hilo_tcp.start()
            except Exception as e:
                print(f"Error al aceptar conexión: {e}")

def servidor_udp():
    """Hilo secundario para responder consultas UDP en el puerto 5001."""
    global contador_turnos
    HOST = '0.0.0.0'
    PORT_UDP = 5001

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
        s_udp.bind((HOST, PORT_UDP))
        print(f"Servidor de consultas escuchando en el puerto {PORT_UDP}...")

        while True:
            try:
                data, direccion = s_udp.recvfrom(1024)
                mensaje = data.decode('utf-8', errors='ignore').strip()

                if mensaje == "CUANTOS":
                    with lock:
                        total_actual = contador_turnos

                    respuesta = f"van>{total_actual}\n"
                    s_udp.sendto(respuesta.encode('utf-8'), direccion)
                    print(f"Consulta de {direccion}: respondido '{respuesta.strip()}'")
            except Exception as e:
                print(f"Error procesando datagrama: {e}")

def main():
    #Iniciar ciclo de escucha UDP en un hilo en segundo plano
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)
    hilo_udp.start()

    #Ejecutar ciclo de escucha TCP en el hilo principal
    servidor_tcp()

if __name__ == "__main__":
    main()