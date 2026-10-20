import socket
import threading

def atender_cliente(conexion, direccion):
    print(f"Cliente conectado desde {direccion}")
    try:
        while True:
            data = conexion.recv(1024)
            if not data:
                break
            conexion.sendall(data)
    except ConnectionResetError:
        print(f"El cliente {direccion} se desconectó abruptamente.")
    except Exception as e:
        print(f"Error inesperado con {direccion}: {e}")
    finally:
        conexion.close()
        print(f"Registro: Conexión finalizada correctamente con {direccion}")

def servidor():
    HOST = '0.0.0.0'
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor persistente iniciado en puerto {PORT}...")

        while True:
            conexion, direccion = s.accept()
            hilo = threading.Thread(
                target=atender_cliente, 
                args=(conexion, direccion), 
                daemon=True
            )
            hilo.start()

if __name__ == "__main__":
    servidor()