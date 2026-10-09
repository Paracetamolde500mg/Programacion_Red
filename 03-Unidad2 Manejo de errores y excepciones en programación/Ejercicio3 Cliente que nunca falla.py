import socket
import sys

#Pide al usuario la IP del servidor de forma dinámica
ip = input("Ingresa la IP del servidor: ")

try:
    #Intenta conectarse con un tiempo límite (timeout)
    with socket.create_connection((ip, 5000), timeout=5) as conexion:
        conexion.sendall("hola\n".encode("utf-8"))

#Ocurre cuando la IP o el nombre de host no se pueden resolver
except socket.gaierror:
    print("Error: IP o nombre de host inválido.")
    sys.exit(1)

#Ocurre cuando el servidor está apagado o no acepta conexiones
except ConnectionRefusedError:
    print("Error: Servidor apagado o inalcanzable.")
    sys.exit(1)

#Ocurre cuando una respuesta nunca llega
except TimeoutError:
    print("Error: El servidor no respondió a tiempo.")
    sys.exit(1)

#Ocurre por una desconexión abrupta a media conversación
except ConnectionResetError:
    print("Error: Desconexión a media conversación.")
    sys.exit(1)