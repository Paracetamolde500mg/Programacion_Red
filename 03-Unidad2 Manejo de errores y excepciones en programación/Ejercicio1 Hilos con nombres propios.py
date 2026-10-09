import threading
import time

def saludar(nombre, cantidad):
    #Imprime el saludo la cantidad de veces especificada
    for i in range(cantidad):
        print(f"{nombre}: hola {i}")
        time.sleep(0.5)

#Lista de tuplas con el nombre del hilo y cuántos saludos dará
tareas = [("Ana", 3), ("Beto", 5), ("Cora", 2)]
hilos = []

#Ciclo for que crea los Thread guardándolos en una lista
for nombre, cantidad in tareas:
    hilo = threading.Thread(target=saludar, args=(nombre, cantidad))
    hilos.append(hilo)
    #Inicia la ejecución concurrente del hilo
    hilo.start()

#Segundo ciclo para esperar que todos los hilos terminen
for hilo in hilos:
    hilo.join()

print("Programa principal terminado.")