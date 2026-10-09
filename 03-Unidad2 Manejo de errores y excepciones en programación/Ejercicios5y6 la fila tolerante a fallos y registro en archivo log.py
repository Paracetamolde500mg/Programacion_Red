import socket
import threading
import time

#Variables Globales
turno_actual = 0
candado_turno = threading.Lock()
candado_log = threading.Lock()

#Log de errores
def registrar_error(direccion, descripcion):
    """Escribe un registro de error de forma segura en un archivo de texto."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"{timestamp} {direccion} {descripcion}\n"
    
    with candado_log:
        #Se abre en modo "a" para agregar sin borrar lo anterior
        with open("errores.log", "a", encoding="utf-8") as archivo:
            archivo.write(linea_log)
            
    #También lo imprimimos en consola para que sepas que ocurrió
    print(f"[ALERTA] Error guardado en log -> {direccion}: {descripcion}")

#Empleado tolerante a fallos
def tomar_turno(conexion, direccion):
    global turno_actual
    try:
        with conexion:
            datos = conexion.recv(1024)
            if not datos: return
            texto = datos.decode("utf-8").strip()
            
            #Si manda basura que no empieza con "TURNO>"
            if not texto.startswith("TURNO>"):
                raise ValueError("Mensaje no sigue el protocolo (Envió otra cosa)")
            
            #Proceso normal si todo está bien
            with candado_turno:
                turno_actual += 1
                turno_asignado = turno_actual
                
            conexion.sendall(f"turno>{turno_asignado}\n".encode("utf-8"))
            print(f"[TCP] Turno {turno_asignado} asignado a {direccion}")
            
    except UnicodeDecodeError:
        registrar_error(direccion, "Los bytes enviados no son UTF-8 válido")
    except ValueError as e:
        registrar_error(direccion, str(e))
    except ConnectionResetError:
        registrar_error(direccion, "Conexión reiniciada abruptamente por el cliente")
    except Exception as e:
        registrar_error(direccion, f"Error inesperado: {e}")

#Servidor Principal
def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()
    print("Servidor de Turnos Tolerante a Fallos escuchando en el puerto 5000...")
    
    try:
        while True:
            conexion, direccion = servidor.accept()
            #Creamos el hilo para el cliente
            hilo = threading.Thread(target=tomar_turno, args=(conexion, direccion), daemon=True)
            hilo.start()
    except KeyboardInterrupt:
        print("\nApagando el servidor...")

if __name__ == "__main__":
    main()