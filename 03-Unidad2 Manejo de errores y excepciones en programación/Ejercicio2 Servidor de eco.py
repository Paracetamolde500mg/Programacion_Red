import socket
import threading

#FUNCIÓN DEL EMPLEADO
def atender_cliente(conexion, direccion):
    print(f"[NUEVA CONEXIÓN] Cliente conectado desde {direccion}")
    #El contador es LOCAL. Cada cliente que entre empezará desde 0.
    contador = 0 
    
    try:
        with conexion:
            buffer = ""
            while True:
                datos = conexion.recv(1024)
                if not datos: 
                    break #Si no hay datos, el cliente se desconectó
                
                buffer += datos.decode("utf-8")
                
                #Procesa línea por línea buscando el salto de línea (\n)
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    contador += 1
                    
                    #Le devolvemos el mismo texto pero con su número de mensaje
                    respuesta = f"{contador}>{linea}\n"
                    conexion.sendall(respuesta.encode("utf-8"))
                    
    except ConnectionResetError:
        print(f"[ERROR] El cliente {direccion} se desconectó de golpe.")
    except Exception as e:
        print(f"[ERROR] Fallo con el cliente {direccion}: {e}")
    finally:
        print(f"[DESCONEXIÓN] Cliente {direccion} terminó.")

#El servidor principal
def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #Abrimos el puerto 5000
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()
    print("Servidor de Eco con Contador escuchando en el puerto 5000...")
    
    try:
        while True:
            conexion, direccion = servidor.accept()
            #Creamos un hilo para cada cliente que llegue
            hilo = threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True)
            hilo.start()
    except KeyboardInterrupt:
        print("\nApagando el servidor...")

if __name__ == "__main__":
    main()