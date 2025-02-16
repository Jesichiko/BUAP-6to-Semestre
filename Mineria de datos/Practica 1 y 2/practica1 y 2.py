import random


def generar_numeros(tipo):

    tamanos = {"10": 10, "200k": 200000, "100k": 100000, "millon": 1000000}

    if tipo in tamanos:
        return random.sample(range(1, 1000001), tamanos[tipo])
    else:
        raise ValueError("Tipo no valido")


def imprimir_conjunto(conjunto, limite=10):
    lista_conjunto = list(conjunto)
    if len(lista_conjunto) > limite:
        elementos = ", ".join(map(str, lista_conjunto[:limite]))
        return f"{{{elementos}, ...}}"
    else:
        return f"{{{', '.join(map(str, lista_conjunto))}}}"


def opciones(conjunto_A, conjunto_B, conjunto_C):

    def union(A, B):
        union = set(A)
        for elemento in B:
            if elemento not in union:
                union.add(elemento)
        return union

    def interseccion(A, B):
        interseccion = set()
        for elemento_x in A:
            if elemento_x in B:
                interseccion.add(elemento_x)
        return interseccion

    def diferencia(A, B):
        diferencia = set()
        for elemento in A:
            if elemento not in B:
                diferencia.add(elemento)
        return diferencia

    # union
    union_result = union(conjunto_A, conjunto_B)
    union_operadores = set(conjunto_A) | set(conjunto_B)

    # interseccion
    interseccion_result = interseccion(conjunto_A, conjunto_B)
    interseccion_operadores = set(conjunto_A) & set(conjunto_B)

    # diferencia
    diferencia_result = diferencia(conjunto_A, conjunto_B)
    diferencia_operadores = set(conjunto_A) - set(conjunto_B)

    # resultados
    print(f"Union: {imprimir_conjunto(union_result)}")
    print(f"Union con operadores: {imprimir_conjunto(union_operadores)}")
    print(f"Verificacion: {union_result == union_operadores}")

    print(f"Interseccion: {imprimir_conjunto(interseccion_result)}")
    print(f"Interseccion con operadores: {imprimir_conjunto(interseccion_operadores)}")
    print(f"Verificacion: {interseccion_result == interseccion_operadores}")

    print(f"Diferencia: {imprimir_conjunto(diferencia_result)}")
    print(f"Diferencia con operadores: {imprimir_conjunto(diferencia_operadores)}")
    print(f"Verificacion: {diferencia_result == diferencia_operadores}")

    # propiedades:
    A = set(conjunto_A)
    B = set(conjunto_B)
    C = set(conjunto_C)

    # propiedad 1: asociatividad de la union
    union1 = union(A, union(B, C))
    print(f"A u (B u C) = {imprimir_conjunto(union1)}")
    union2 = union(union(A, B), C)
    print(f"(A u B) u C = {imprimir_conjunto(union2)}")
    print(f"Validacion de prop 1: {union1 == union2}")

    # propiedad 2: asociatividad de la interseccion
    inters1 = interseccion(A, interseccion(B, C))
    print(f"A & (B & C) = {imprimir_conjunto(inters1)}")
    inters2 = interseccion(interseccion(A, B), C)
    print(f"(A & B) & C = {imprimir_conjunto(inters2)}")
    print(f"Validacion de prop 2: {inters1 == inters2}")

    # propiedad 3: distributividad de la interseccion respecto de la union
    inters_distri_1 = interseccion(A, union(B, C))
    print(f"A & (B u C) = {imprimir_conjunto(inters_distri_1)}")
    inters_distri_2 = union(interseccion(A, B), interseccion(A, C))
    print(f"(A & B) u (A & C) = {imprimir_conjunto(inters_distri_2)}")
    print(f"Validacion de prop 3: {inters_distri_1 == inters_distri_2}")

    # propiedad 4: distributividad de la union respecto de la interseccion
    union_distri_1 = union(A, interseccion(B, C))
    print(f"A u (B & C) = {imprimir_conjunto(union_distri_1)}")
    union_distri_2 = interseccion(union(A, B), union(A, C))
    print(f"(A u B) & (A u C) = {imprimir_conjunto(union_distri_2)}")
    print(f"Validacion de prop 4: {union_distri_1 == union_distri_2}")

    # suponemos que el universo es la union de los 3 conjuntos
    universo = A | B | C
    complemento_A = universo - A
    complemento_B = universo - B

    # propiedad 5
    complemento_union_1 = universo - union(
        A, B
    )  # tambien se puede ver de esta forma (A u B)^c
    print(f"(A u B)^c = {imprimir_conjunto(complemento_union_1)}")
    complemento_union_2 = interseccion(complemento_A, complemento_B)
    print(f"A^c & B^c = {imprimir_conjunto(complemento_union_2)}")
    print(f"Validacion de prop 5: {complemento_union_1 == complemento_union_2}")

    # propiedad 6
    complemento_interseccion_1 = universo - interseccion(A, B)
    print(f"(A & B)^c = {imprimir_conjunto(complemento_interseccion_1)}")
    complemento_interseccion_2 = union(complemento_A, complemento_B)
    print(f"A^c u B^c = {imprimir_conjunto(complemento_interseccion_2)}")
    print(
        f"Validacion de prop 6: {complemento_interseccion_1 == complemento_interseccion_2}"
    )


def menu():
    conjunto_a = []
    conjunto_b = []
    conjunto_c = []
    opt = 0

    while opt != 1:

        # tam conjunto A
        print("Dame el tamaño de la lista A (10, 200k, 100k, millon): ")
        conjunto_a = generar_numeros(input())

        # tam conjunto B
        print("Dame el de la lista B: ")
        conjunto_b = generar_numeros(input())

        print("Dame el de la lista C: ")
        conjunto_c = generar_numeros(input())

        # resultado
        print(f"Conjunto A = {imprimir_conjunto(conjunto_a)}")
        print(f"Conjunto B = {imprimir_conjunto(conjunto_b)}")
        print(f"Conjunto C = {imprimir_conjunto(conjunto_c)}")

        print("Resultados: ")
        opciones(conjunto_a, conjunto_b, conjunto_c)

        print("Quieres salir? Escribe 1 si es asi")
        opt = int(input())


menu()
