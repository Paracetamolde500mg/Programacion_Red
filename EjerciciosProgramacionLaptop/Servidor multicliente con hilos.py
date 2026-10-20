import socket
import threading

def atender_cliente(conexion, direccion):
    """Atiende el eco para cada cliente conectado."""
    print(f"Cliente conectado desde {direccion}")
    try:
        while True:
            data = conexion.recv(1024)
            if not data:
                break
            #Envía de vuelta los mismos datos recibidos(eco)
            conexion.sendall(data)
    finally:
        conexion.close()
        print(f"Conexión cerrada con {direccion}")

def servidor():
    HOST = '0.0.0.0'
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor multicliente escuchando en el puerto {PORT}...")

        while True:
            conexion, direccion = s.accept()
            #Se asigna el tratamiento del cliente a un hilo independiente
            hilo = threading.Thread(
                target=atender_cliente, 
                args=(conexion, direccion), 
                daemon=True
            )
            hilo.start()

if __name__ == "__main__":
    servidor()import socket
import threading

def atender_cliente(conexion, direccion):
    """Atiende el eco para cada cliente conectado."""
    print(f"Cliente conectado desde {direccion}")
    try:
        while True:
            data = conexion.recv(1024)
            if not data:
                break
            #Envía de vuelta los mismos datos recibidos (eco)
            conexion.sendall(data)
    finally:
        conexion.close()
        print(f"Conexión cerrada con {direccion}")

def servidor():
    HOST = '0.0.0.0'
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor multicliente escuchando en el puerto {PORT}...")

        while True:
            conexion, direccion = s.accept()
            #Se asigna el tratamiento del cliente a un hilo independiente
            hilo = threading.Thread(
                target=atender_cliente, 
                args=(conexion, direccion), 
                daemon=True
            )
            hilo.start()

if __name__ == "__main__":
    servidor()