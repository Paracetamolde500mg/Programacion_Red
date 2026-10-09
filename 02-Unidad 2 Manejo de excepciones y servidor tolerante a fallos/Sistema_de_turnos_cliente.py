import socket

def main():
    while True:
        print("\n.----Menú----.")
        print("1. Tomar turno TCP")
        print("2. Ver cuantos turnos van UDP")
        print("3. Salir")
        opc = input("¿Qué opción quieres escoger?: ")

        if opc == "1":
            #TCP
            apodo = input("Dame tu nombre: ")
            with socket.create_connection(("127.0.0.1", 5000)) as conexion:
                #Armamos el mensaje
                mensaje = f"TURNO>{apodo}"
                conexion.sendall((mensaje + "\n").encode("utf-8")) 
                respuesta = conexion.recv(1024).decode("utf-8").strip()
                print(f"Turno logrado: {apodo}, el servidor dice: {respuesta}")
                
        elif opc == "2":
            #UDP
            # usamos SOCK_DGRAM
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente_udp:
                #Ponemos un límite de tiempo por si el servidor no responde
                cliente_udp.settimeout(3)            
                mensaje_udp = "CUANTOS\n"
                try:
                    #Lo enviamos directamente a la IP y puerto sin conectarnos antes
                    cliente_udp.sendto(mensaje_udp.encode("utf-8"), ("127.0.0.1", 5001))
                    #Esperamos la respuesta
                    datos, _ = cliente_udp.recvfrom(1024)
                    respuesta_udp = datos.decode("utf-8").strip()
                    print(f"Consulta exitosa: {respuesta_udp}")
                    
                except socket.timeout:
                    print("Error: El servidor tardó mucho en responder (Timeout).")
                    
        elif opc == "3":
            print("Saliendo...")
            break
        else:
            print("Error Opción invalida :/..., solo se permite 1, 2, 3")
if __name__ == "__main__":
    main()