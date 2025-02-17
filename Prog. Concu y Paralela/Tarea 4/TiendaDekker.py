import random
from abc import ABC, abstractmethod
from threading import Thread
from typing import List

flag: List[bool] = [False, False]
turno: int = 0


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
        output = ["Prenda\tCantidad disponible"]
        for prenda, cantidad in self.stock.items():
            output.append(f"{prenda}:\t{cantidad}")
        return "\n".join(output)


class OperadorTienda(ABC, Thread):
    def __init__(self, id: int, tienda: Tienda, proceso_id: int):
        super().__init__()
        self.id = id
        self.tienda = tienda
        self.hilo_id = proceso_id

    def entrar_seccion_critica(self):
        global flag, turno
        flag[self.hilo_id] = True
        otro = 1 - self.hilo_id

        while flag[otro]:
            if turno != self.hilo_id:
                flag[self.hilo_id] = False
                while turno != self.hilo_id:
                    pass
                flag[self.hilo_id] = True

    def salir_seccion_critica(self):
        global flag, turno
        turno = 1 - self.hilo_id
        flag[self.hilo_id] = False

    @abstractmethod
    def run(self):
        pass


class Cliente(OperadorTienda):
    def __init__(self, nombre, id, tienda, proceso_id):
        super().__init__(id, tienda, proceso_id)
        self.nombre = nombre

    def run(self):
        random_num = random.randint(0, self.tienda.get_size() - 1)  # [0 , getSize()]

        self.entrar_seccion_critica()
        try:
            # SECCION CRITICA
            resultado = self.tienda.comprar(random_num)
            # SECCION CRITICA

            if resultado[1] is None:
                print(
                    f"{self.nombre} quiso comprar {resultado[0]} pero ya no hay existencias"
                )
            else:
                print(
                    f"- {self.nombre} ha comprado: {resultado[0]} - Existencias restantes: {resultado[1]}, saliendo de la tienda..."
                )
        finally:
            self.salir_seccion_critica()


def main():
    tienda = Tienda()
    print(tienda, "\n")

    hilos = [
        Cliente("Tadeo", 1, tienda, 0),
        Cliente("Marcos", 3, tienda, 1),
    ]

    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()

    print("\n", tienda)


main()
