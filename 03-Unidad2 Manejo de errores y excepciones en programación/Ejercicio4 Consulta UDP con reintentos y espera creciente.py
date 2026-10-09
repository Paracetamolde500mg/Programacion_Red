import socket
import time

def main():
    servidor = ("127.0.0.1", 5001)
    print(f"Iniciando cliente UDP. Consultando al puerto 5001...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        #El timeout evita que se quede congelado si el servidor no existe
        cliente.settimeout(2)
        
        #Reintentar hasta tres veces
        for intento in range(1, 4):
            try:
                print(f"Enviando mensaje 'CUANTOS' (Intento {intento})...")
                cliente.sendto("CUANTOS\n".encode("utf-8"), servidor)
                
                #Esperamos la respuesta
                datos, _ = cliente.recvfrom(1024)
                print(f"¡Éxito! El servidor respondió: {datos.decode('utf-8').strip()}")
                return # Siresponde, salimos de la función y termina el programa
                
            except (TimeoutError, ConnectionResetError):
                #Si pasan 2 segundos sin respuesta, entra aquí
                espera = 2 ** (intento - 1) # Calcula 1s, 2s, 4s
                print(f"[Aviso] No hubo respuesta. Esperando {espera} segundos para el próximo intento...\n")
                time.sleep(espera)
        
        print("Error definitivo: El servidor no respondió tras 3 intentos. Abortando.")

if __name__ == "__main__":
    main()