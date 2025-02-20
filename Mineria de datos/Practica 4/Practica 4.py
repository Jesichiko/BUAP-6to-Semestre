from collections import defaultdict

variables = []  # variables y sus eventos sin repetir (como tuplas)
muestras = []  # muestras que se dieron para cada variable (como tuplas)


def generar_tuplas(variable, eventos_repetidos):
    variables.append((variable, identificar_eventos(eventos_repetidos)))
    muestras.append((variable, eventos_repetidos))


def identificar_eventos(eventos_ingresados):
    eventos_sin_repetir = []
    for evento in eventos_ingresados:
        if evento not in eventos_sin_repetir:
            eventos_sin_repetir.append(evento)
    return eventos_sin_repetir


def ingresar_valores(variable, lista_eventos):
    generar_tuplas(variable, lista_eventos)


def generar_tabla():
    frecuencias_variables = {}

    # Recorremos las variables almacenadas
    for variable_i, _ in variables:
        conteo = defaultdict(int)  # Contador de frecuencias absolutas
        total = 0  # Contador total de muestras

        # Buscamos la lista de eventos repetidos para la variable actual
        for variable, eventos_repetidos in muestras:
            if variable == variable_i:
                for evento in eventos_repetidos:
                    conteo[evento] += 1
                    total += 1

        # Calculamos las frecuencias relativas
        freq_relativas = {evento: count / total for evento, count in conteo.items()}

        # Guardamos los resultados
        frecuencias_variables[variable_i] = {
            "absoluta": dict(conteo),
            "relativa": freq_relativas,
        }

    # Imprimimos la tabla
    for variable, datos in frecuencias_variables.items():
        print(f"\nVariable: {variable}")
        print("Evento\t\tFA\t\tFR")
        print("-" * 50)
        suma_fa = 0
        suma_fr = 0

        for evento, abs_freq in datos["absoluta"].items():
            rel_freq = datos["relativa"][evento]
            suma_fa += abs_freq
            suma_fr += rel_freq
            print(f"{evento:<15}{abs_freq:<16}{rel_freq:.3f}")

        print("-" * 50)
        print(f"Total{'':<10}{suma_fa:<16}{suma_fr:.3f}")


def menu():
    ingresar_valores(
        "Outlook",
        [
            "Sunny",
            "Sunny",
            "Overcast",
            "Rain",
            "Rain",
            "Rain",
            "Overcast",
            "Sunny",
            "Sunny",
            "Rain",
            "Sunny",
            "Overcast",
            "Overcast",
            "Rain",
        ],
    )
    ingresar_valores(
        "Temperature",
        [
            "High",
            "High",
            "High",
            "Medium",
            "Low",
            "Low",
            "Low",
            "Medium",
            "Low",
            "Medium",
            "Medium",
            "Medium",
            "High",
            "Medium",
        ],
    )
    generar_tabla()


menu()
