from threading import Thread, Semaphore
import random
from typing import Dict, List

class Tienda:
    def __init__(self):
        self.stock = {
            "Camisa Azul chica": 2,
            "Pantalon verde mediano": 3,
            "Tennis negros chicos": 5,
            "Gorro cafe grande": 7,
            "Gafas de sol grandes": 11
        }
        self.prendas = list(self.stock.keys())

    def comprar(self, num_prenda):
        prenda = self.prendas[num_prenda]

        if self.stock[prenda] == 0:
            return [prenda, None]

        self.stock[prenda] -= 1
        return [prenda, self.stock[prenda]]

    def agregar(self, num_prenda):
        prenda = self.prendas[num_prenda]
        cantidad = (self.stock[prenda] * 2) + 1
        self.stock[prenda] = cantidad
        return [prenda, cantidad]

    def get_size(self):
        return len(self.stock)

    def __str__(self):
        sb = ["Prenda\tCantidad disponible\n"]
        for prenda, cantidad in self.stock.items():
            sb.append(f"{prenda}:\t{cantidad}\n")
        return "".join(sb)

class Cliente(Thread):
    def __init__(self, nombre, tienda, semaforo):
        super().__init__()
        self.nombre = nombre
        self.tienda = tienda
        self.semaforo = semaforo

    def run(self):
        random_num = random.randint(0,self.tienda.get_size()-1)
        try:
            self.semaforo.acquire()
            
            #SECCION CRITICA
            resultado = self.tienda.comprar(random_num)
            #SECCION CRITICA
            
            if resultado[1] is None:
                print(f"{self.nombre} quiso comprar {resultado[0]} pero ya no hay existencias")
            else:
                print(f"- {self.nombre} ha comprado: {resultado[0]} - Existencias restantes: {resultado[1]}, saliendo de la tienda...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.semaforo.release()

class Proveedores(Thread):
    def __init__(self, id_proveedor: int, tienda: Tienda, semaforo: Semaphore):
        super().__init__()
        self.id = id_proveedor
        self.tienda = tienda
        self.semaforo = semaforo

    def run(self):
        random_num = random.randint(0,self.tienda.get_size()-1)
        try:
            self.semaforo.acquire()
            #SECCION CRITICA
            resultado = self.tienda.agregar(random_num)
            #SECCION CRITICA
            print(f"- Proveedor {self.id} ha reabastecido: {resultado[0]} - Prendas actualizadas: {resultado[1]}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.semaforo.release()

def main():
    tienda = Tienda()
    #semaforo de tamaño 1 solo puede acceder un solo hilo al codigo de la seccion critica
    semaforo = Semaphore(1)
    print(tienda)  #tienda al principio

    cliente1 = Cliente("Paco", tienda, semaforo)
    cliente2 = Cliente("Memo", tienda, semaforo)
    cliente3 = Cliente("Kalusha", tienda, semaforo)
    cliente4 = Cliente("Tito", tienda, semaforo)
    proveedor1 = Proveedores(2099, tienda, semaforo)
    proveedor2 = Proveedores(73, tienda, semaforo)

    cliente1.start()
    proveedor1.start()
    cliente2.start()
    cliente3.start()
    proveedor2.start()
    cliente4.start()

    #esperamos a que terminen todos los hilos
    for thread in [cliente1, proveedor1, cliente2, cliente3, proveedor2, cliente4]:
        thread.join()
    print("\n",tienda)  #tienda al final
main()