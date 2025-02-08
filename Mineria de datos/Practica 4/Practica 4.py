import random
from collections import defaultdict

variables = [] #num de eventos y variables desconocido, se define vacio

def generar_variables(nombre, eventos):
    variables.append((nombre, eventos))

def generar_muestra(n):
    muestras = []
    for _ in range(n):
        muestra_i = {}
        for variable_i, eventos_i in variables:
            evento_aleatorio = random.choice(eventos_i)
            muestra_i[variable_i] = evento_aleatorio
        muestras.append(muestra_i)
    return muestras
    
def generar_tabla(muestra_variables):
    frecuencias_variables = {} #almacenaremos las frecuencias de cada variable
    
    #recorremos las variables
    for variable_i, _ in variables:
        conteo = defaultdict(int) #creamos un contador
        total = len(muestra_variables) #total del tamaño de la muestra
        
        for muestra in muestra_variables: #contamos los eventos
            evento = muestra[variable_i] #se obtiene el evento i de la muestra para una variable dada
            conteo[evento] += 1 #con conteo sumamos 1 a ese evento cada que aparece
        
        #gracias a conteo calculamos la frecuencia relativa del evento dado
        freq_relativas = {evento: count/total for evento, count in conteo.items()}
        #insertamos en el diccionario las frecuencias para cada uno
        frecuencias_variables[variable_i] = {
            'absoluta': dict(conteo),
            'relativa': freq_relativas
        }
        
    #imprimimos la tabla
    for variable, datos in frecuencias_variables.items():
        print(f"\nVariable: {variable}")
        print("Evento\t\tFA\t\tFR")
        print("-" * 50)
        suma_fa = 0
        suma_fr = 0
        
        for evento in dict(datos['absoluta']): #convertimos a diccionario para recorrerlo
            abs_freq = datos['absoluta'][evento]
            rel_freq = datos['relativa'][evento]
            
            suma_fa += abs_freq
            suma_fr += rel_freq
            print(f"{evento:<15}{abs_freq:<16}{rel_freq:.3f}")
        print("-" * 50)
        print(f"Total{'':<10}{suma_fa:<16}{suma_fr:.3f}")

def menu():
    generar_variables("Outlook", ["Sunny", "Overcast", "Rain"])
    generar_variables("Temperature", ["High", "Medium", "Low"])
    generar_variables("Var Ejemplo", ["caso 1", "caso 2", "caso 3", "caso 4", "caso 5"])
    muestra_variables = generar_muestra(13)
    generar_tabla(muestra_variables)
menu()