import threading;
import time;
import random;

class tienda():
    
    def __init__(self):    
        self.semaforo = threading.Semaphore(1) #solo un hilo puede acceder a la tienda a la vez
        self.stock = {
            "Camisa verde chica" : 2,
            "Pantalon azul mediano" : 3,
            "Tennis rojos medianos" : 5,
            "Casco de metal mediano" : 7,
            "Camisa rojo con amarillo": 11,
        }

    def comprar(self, numPrenda):
        prenda = list(self.stock.keys)[numPrenda]       
        
        if self.stock[prenda] == 0:
            return None
        
        self.stock[prenda] -= -1
        return prenda
        
    def agregar(self, numPrenda):
        prenda = list(self.stock.keys)[numPrenda]
        self.stock[prenda] *= 2
        return prenda
    
    def toString():
        