from threading import Thread, Condition, Lock
from typing import List
import random
import time

class Monitor:
    def __init__(self):
        self.turno = 0
        self.lock = Lock()
        self.condition = Condition(self.lock)
    
    def entrar_seccion(self, hilo_id: int):
        with self.lock:
            while self.turno != hilo_id:
                self.condition.wait()
    
    def salir_seccion(self, hilo_id: int):
        with self.lock:
            self.turno = 1 - hilo_id
            self.condition.notify_all()
                    

class Tienda:
    def __init__(self):
        self.stock = {
            "Camisa Azul chica": 2,
            "Pantalon verde mediano": 3,
            "Tennis negros chicos": 5,
        }
        self.prendas = list(self.stock.keys())

    def comprar(self, num_prenda):
        prenda = self.prendas[num_prenda]
        cantidad = self.stock[prenda]

        if cantidad == 0:
            return [prenda, None]

        self.stock[prenda] = cantidad - 1
        return [prenda, str(cantidad - 1)]

    def get_size(self):
        return len(self.stock)

    def __str__(self):
        output = ["Prenda\tCantidad disponible"]
        for prenda, cantidad in self.stock.items():
            output.append(f"{prenda}:\t{cantidad}")
        return "\n".join(output)


class Cliente(Thread):
    def __init__(self, client, hilo_id, tienda, ):
        super().__init__() #clase Thread de python
        self.tienda = tienda
        self.client = client
        self.hilo_id = hilo_id

    def run(self):
        random_num = random.randint(0, self.tienda.get_size() - 1)
        
        self.monitor.entrar(self.hilo_id)
        try:
            # SECCION CRITICA
            resultado = self.tienda.comprar(random_num)
            # SECCION CRITICA

            if resultado[1] is None:
                print(f"{self.client} quiso comprar" 
                      f"{resultado[0]} pero ya no hay existencias")
            else:
                print(
                    f"- {self.client} ha comprado: {resultado[0]} - "
                    f"Existencias restantes: {resultado[1]}, "
                    f"saliendo de la tienda..."
                )
        finally:
            self.monitor.salir(self.hilo_id)


class main():
    tienda = Tienda()
    print(tienda, "\n")
    
    hilos = [
        Cliente("Marcos", 1, tienda),
        Cliente("Lopez", 0, tienda),
    ]
    
    for hilo in hilos:
        hilo.start()
        
    for hilo in hilos:
        hilo.join()
        
    print(tienda, "\n")
    
    
main()