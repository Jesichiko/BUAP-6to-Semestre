import threading
import time

lock = threading.Lock()
condicion = threading.Condition(lock)
recurso = 0

class Hilo1(threading.Thread):
    def run(self):
        global recurso
        with lock:
            print("El hilo 1 tiene el recurso lock")
            recurso += 1
            condicion.notify_all()  #Notificamos al hilo 2 para que continue
        print("Resultado hilo 1:", recurso)

class Hilo2(threading.Thread):
    def run(self):
        global recurso
        with lock:
            #Estado blocked
            print("Hilo 2 esperando a que hilo 1 libere el recurso...")
            condicion.wait()  #Esperamos hasta que el hilo 1 libere el recurso
            print("El hilo 2 tiene el recurso lock")
            recurso *= 10
        print("Resultado hilo 2:", recurso)

hilo2 = Hilo2()      
hilo1 = Hilo1()
#Estado new, en este caso python maneja el estado new y terminated como valores booleanos true false
print(f"Estado de Hilo1: {hilo1.is_alive()}") #true
print(f"Estado de Hilo2: {hilo2.is_alive()}") #true

#Estado running 
hilo2.start()
time.sleep(0.1) #damos tiempo para que hilo 2 espere lo suficiente a hilo 1
hilo1.start()

#Estado waiting (terminamos la espera)
hilo1.join()
hilo2.join()

# Estado terminated
print(f"Estado de Hilo1: {hilo1.is_alive()}") #false
print(f"Estado de Hilo2: {hilo2.is_alive()}") #false