from threading import Thread
import random
from typing import List
from abc import ABC, abstractmethod

flag: List[bool] = [False, False]
turn: int = 0

class Tienda:
    def __init__(self):
        self.stock = {
            "Camisa Azul chica": 2,
            "Pantalon verde mediano": 3,
            "Tennis negros chicos": 5,
            "Gorro cafe grande": 7,
            "Gafas de sol grandes": 11
        }
    
    def comprar(self, num_prenda):
        prendas = list(self.stock.keys())
        prenda = prendas[num_prenda]
        
        if self.stock[prenda] == 0:
            return None
            
        self.stock[prenda] -= 1
        return prenda
    
    def agregar(self, num_prenda):
        prendas = list(self.stock.keys())
        prenda = prendas[num_prenda]
        cantidad = (self.stock[prenda] * 2) + 1
        self.stock[prenda] = cantidad
        return prenda
    
    def get_size(self):
        return len(self.stock)
    
    def __str__(self):
        output = ["Prenda\tCantidad disponible"]
        for prenda, cantidad in self.stock.items():
            output.append(f"{prenda}:\t{cantidad}")
        return "\n".join(output)

class OperadorTienda(ABC, Thread):
    def __init__(self, id: int, tienda: Tienda, proceso_id: int):
        super().__init__()
        self.id = id
        self.tienda = tienda
        self.proceso_id = proceso_id
    
    def entrar_seccion_critica(self):
        global flag, turn
        flag[self.proceso_id] = True
        otro = 1 - self.proceso_id
        
        while flag[otro]:
            if turn != self.proceso_id:
                flag[self.proceso_id] = False
                while turn != self.proceso_id:
                    pass 
                flag[self.proceso_id] = True
    
    def salir_seccion_critica(self):
        global flag, turn
        turn = 1 - self.proceso_id
        flag[self.proceso_id] = False
    
    @abstractmethod
    def run(self):
        pass

class Cliente(OperadorTienda):
    def __init__(self, nombre, id, tienda, proceso_id):
        super().__init__(id, tienda, proceso_id)
        self.nombre = nombre
    
    def run(self):
        random_num = random.randint(1, self.tienda.get_size() - 1)
        
        self.entrar_seccion_critica()
        try:
            #SECCION CRITICA
            prenda = self.tienda.comprar(random_num)
            #SECCION CRITICA
            
            if prenda is None:
                print(f"{self.nombre} quiso comprar pero ya no hay existencias")
            else:
                print(f"{self.nombre} ha comprado: {prenda}, saliendo de la tienda...")
        finally:
            self.salir_seccion_critica()

class Proveedor(OperadorTienda):
    def run(self):
        random_num = random.randint(1, self.tienda.get_size() - 1)        
        self.entrar_seccion_critica()
        try:
            #SECCION CRITICA
            prenda = self.tienda.agregar(random_num)
            #SECCION CRITICA
            
            print(f"Proveedor {self.id} ha reabastecido: {prenda}")
        finally:
            self.salir_seccion_critica()

def main():
    tienda = Tienda()
    print(tienda)

    hilos = [
        Cliente("Tadeo", 1, tienda, 0),
        Proveedor(2099, tienda, 1),
        Cliente("Pedro", 2, tienda, 0),
        Cliente("Marcos", 3, tienda, 1),
        Proveedor(73, tienda, 0),
        Cliente("Jesus", 4, tienda, 1)
    ]
    for hilo in hilos:
        hilo.start()    
    for hilo in hilos:
        hilo.join()
    
    print(tienda)
main()