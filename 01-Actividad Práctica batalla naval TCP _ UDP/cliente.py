import socket  # Importa la librería socket para gestionar la conexión de red

def iniciar_cliente():
    HOST = '127.0.0.1'  # Dirección IP del servidor al que nos vamos a conectar (en este caso, tu propia PC o localhost)
    PUERTO = 65432      # Puerto de red específico al que debe apuntar la conexión (debe coincidir con el servidor)
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un objeto socket TCP/IP (IPv4 y orientado a conexión)
    cliente.connect((HOST, PUERTO))  # Establece activamente la conexión de red con el servidor en la IP y puerto especificados
    
    print("Conexión establecida con éxito al servidor de Batalla Naval.")  # Mensaje de confirmación local
    
    coordenada = "B4"  # Define una coordenada de ataque simulada para el juego
    print(f"Enviando coordenada de ataque: {coordenada}")  # Muestra en consola la jugada que se va a transmitir
    cliente.sendall(coordenada.encode('utf-8'))  # Convierte el string a bytes y lo envía por la red garantizando entrega completa
    
    respuesta = cliente.recv(1024)  # Se bloquea brevemente esperando la respuesta del servidor (hasta 1024 bytes)
    print(f"Respuesta recibida del servidor: {respuesta.decode('utf-8')}")  # Decodifica los bytes a texto y los imprime en pantalla
    
    cliente.close()  # Cierra el socket del cliente para liberar los recursos de red

if __name__ == "__main__":  # Verifica si el script se ejecuta de forma directa
    iniciar_cliente()  # Ejecuta la función principal del cliente