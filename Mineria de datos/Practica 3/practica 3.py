import matplotlib
import matplotlib.pyplot as plt
import numpy as np

sizes = {"10": 10, "100": 100, "1000": 1000, "millon": 1000000}


def generar_muestra(size):
    # Hacemos una muestra del tamaño deseado desde 0 hasta 1500 (1501 para incluir el 1500)
    muestra = np.random.randint(
        0, 1501, sizes[size]
    )  # ordenamos para poder dividir los rangos y que sean excluyentes mas adelante
    muestra.sort()
    print(f"Muestra generada (ordenada): {muestra}")
    return muestra


def creacion_rangos():
    rangos = []
    inicio = 0
    # se generan los 10 intervalos que son excluyentes y que "saltan" de 1500 // 10 en 1500 // 10
    for _ in range(9):
        fin = inicio + (1500 // 10) - 1
        rangos.append(
            (inicio, fin)
        )  # se guarda el inicio del rango y el final del rango en una tupla esto para su posterior impresion
        inicio += 1500 // 10
    rangos.append((inicio, 1500))  # ultimo rango, el que completa los 1500
    return rangos


def tabla(muestra, rangos):
    total_FA, total_FR = 0, 0
    frecuencias = []

    print("\tRangos\t\tFA\tFR")
    for i, rango_particiones in enumerate(rangos):
        # formulas para el calculo de FA y FR
        # se recorre toda la muestra y se suma 1 por cada numero i que este en el rango (rango_particiones[0] <= i <= rango_particiones[1])
        # es decir, se cuentan los numeros de la muestra cayeron en un intervalo dado y se suma 1 si es asi
        frecuencia_absoluta = sum(
            1
            for valor in muestra
            if rango_particiones[0] <= valor <= rango_particiones[1]
        )
        # formual general para FR
        frecuencia_relativa = frecuencia_absoluta / len(muestra)

        frecuencias.append(
            frecuencia_absoluta
        )  # añadimos la frecuencia absoluta para luego imprimirla
        total_FA += frecuencia_absoluta
        total_FR += frecuencia_relativa
        print(
            f"{i:<2} || {rango_particiones[0]:<3} - {rango_particiones[1]:<6} || {frecuencia_absoluta:<6} || {frecuencia_relativa:.2f}"
        )
    print(f"Suma total de Frecuencia Absoluta: {total_FA}")
    print(f"Suma total de Frecuencia Relativa: {total_FR:.1f}")
    return frecuencias


def graficar(rangos, frecuencias, size):
    size = sizes[size]

    # Etiquetas de los intervalos en el eje X
    etiquetas = [f"{r[0]}-{r[1]}" for r in rangos]

    # Configuracion inicial de la grafica
    plt.figure(figsize=(14, 8))
    plt.gca().set_facecolor("#f7f7f7")  # blanco

    # Creamos las barras
    barras = plt.bar(
        etiquetas, frecuencias, color="#4CAF50", edgecolor="black", alpha=0.85
    )  # verde

    # Agregar etiquetas con los valores sobre las barras
    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura + max(frecuencias) * 0.02,
            str(altura),
            ha="center",
            fontsize=12,
            color="black",
            fontweight="bold",
        )

    plt.xticks(rotation=45, fontsize=12)  # Rotamos etiquetas del eje X
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Etiquetas y titulo
    plt.xlabel("Rangos", color="#2E7D32", fontsize=14, fontweight="bold")  # verde
    plt.ylabel(
        "Frecuencia Absoluta", color="#C62828", fontsize=14, fontweight="bold"
    )  # rojo
    plt.title(
        f"Distribucion de Frecuencias en muestra tamaño {size}",
        color="#C62828",
        fontsize=20,
        fontweight="bold",
    )  # rojo
    plt.show(block=True)


def menu():
    print("Dame el tamaño de la muestra: (10, 100, 1000, millon)")
    size = input()
    muestra = generar_muestra(size)
    rangos = creacion_rangos()
    frecuencias = tabla(muestra, rangos)
    graficar(rangos, frecuencias, size)


menu()
