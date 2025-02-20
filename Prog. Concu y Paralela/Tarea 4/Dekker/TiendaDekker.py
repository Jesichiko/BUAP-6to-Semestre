from threading import Thread
from typing import List
import random
import time

# variables compartidas para Dekker
flag: List[bool] = [False, False]
turno: int = 0

class Dekker:
    @staticmethod
    def entrar_seccion(hilo_id):
        global flag, turno
        flag[hilo_id] = True
        otro = 1 - hilo_id

        while flag[otro]:
            if turno != hilo_id:
                flag[hilo_id] = False
                while turno != hilo_id:
                    time.sleep(0) #yield en python
                flag[hilo_id] = True

    @staticmethod
    def salir_seccion(hilo_id):
        global flag, turno
        turno = 1 - hilo_id
        flag[hilo_id] = False

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
    def __init__(self, client, hilo_id, tienda, dekker):
        super().__init__() #clase Thread de python
        self.dekker = dekker
        self.tienda = tienda
        self.client = client
        self.hilo_id = hilo_id

    def run(self):
        random_num = random.randint(0, self.tienda.get_size() - 1)

        self.dekker.entrar_seccion_critica(self.hilo_id)
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
            self.dekker.salir_seccion_critica(self.hilo_id)

def main():
    dekker = Dekker()
    inst = Tienda()
    print(inst, "\n")

    hilos = [
        Cliente("Pedro", 1, inst, dekker),
        Cliente("Luis", 0, inst, dekker)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\n", inst)

main()