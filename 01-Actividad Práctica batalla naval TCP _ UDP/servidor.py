import socket  # Importa el módulo estándar 'socket' para permitir la comunicación de red entre procesos

def iniciar_servidor():  # Define una función principal que encapsula la lógica de inicialización y ejecución del servidor
    HOST = '127.0.0.1'  # Define la dirección IP local (localhost) en la que el servidor escuchará las peticiones
    PUERTO = 65432  # Define el número de puerto de red específico que utilizará el servicio
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un objeto socket utilizando IPv4 (AF_INET) y el protocolo orientado a conexión TCP (SOCK_STREAM)
    servidor.bind((HOST, PUERTO))  # Asocia (vincula) el socket creado a la dirección IP y al puerto definidos previamente
    servidor.listen(1)  # Configura el servidor en modo de escucha, permitiendo aceptar una fila de hasta 1 cliente en espera
    
    print(f"Servidor de Batalla Naval activo y escuchando en {HOST}:{PUERTO}...")  # Imprime un mensaje en la consola indicando que el servidor está listo
    
    conexion, direccion = servidor.accept()  # Detiene la ejecución y espera de forma bloqueante a que un cliente se conecte; al hacerlo, devuelve un nuevo socket de conexión y la IP del cliente
    print(f"¡Conexión establecida exitosamente con el cliente ubicado en: {direccion}")  # Muestra en pantalla la dirección IP y puerto del cliente conectado
    
    try:  # Inicia un bloque de código protegido para gestionar de manera segura la sesión y posibles desconexiones
        while True:  # Crea un bucle infinito para mantener el juego o la comunicación activa turno por turno
            datos_recibidos = conexion.recv(1024)  # Lee y almacena hasta 1024 bytes de datos enviados por el cliente a través del socket
            if not datos_recibidos:  # Evalúa si la variable está vacía, lo que indica que el cliente cerró la conexión abruptamente
                print("El cliente ha finalizado la sesión de red.")  # Informa en la consola local sobre la desconexión del cliente
                break  # Rompe el bucle repetitivo para salir de la comunicación
            
            mensaje = datos_recibidos.decode('utf-8')  # Convierte los bytes crudos recibidos a una cadena de texto (string) utilizando codificación UTF-8
            print(f"Coordinada de ataque recibida del cliente: {mensaje}")  # Imprime en consola la jugada enviada por el cliente para fines de monitoreo
            
            respuesta = f"Procesando jugada para la coordenada: {mensaje} -> Resultado: [Agua / Impacto]"  # Genera una respuesta simulada basada en la posición recibida
            conexion.sendall(respuesta.encode('utf-8'))  # Codifica la respuesta a bytes y la transmite de vuelta al cliente garantizando la entrega total
    finally:  # Bloque que se ejecuta obligatoriamente al finalizar la sesión o si ocurre un error imprevisto
        conexion.close()  # Cierra la conexión específica del cliente actual liberando el canal
        servidor.close()  # Cierra el socket principal del servidor liberando completamente el puerto en el sistema operativo

if __name__ == "__main__":  # Verifica si el script se está ejecutando directamente desde la terminal como programa principal
    iniciar_servidor()  # Invoca la función principal para poner en marcha el servidor de red