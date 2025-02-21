#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <time.h>

#define MAX_ITEMS 5
#define MAX_NAME_LENGTH 50

// Variables compartidas
bool flag[2] = {false, false}; // Banderas para los dos hilos
int turn = 0; // Turno inicial

// Estructura para representar cada item de la tienda
typedef struct {
    char prenda[MAX_NAME_LENGTH];
    int cantidad;
} Articulo;

// Estructura para representar la tienda
typedef struct {
    Articulo items[MAX_ITEMS];
    int size;
} Tienda;

// Estructura para pasar los argumentos a los hilos
typedef struct {
    char nombre[MAX_NAME_LENGTH];
    Tienda *store;
    int id; // ID del hilo
} ArgumentosHilo;

// Inicializar la tienda
void tienda_iniciar(Tienda *store) {

    strcpy(store->items[0].prenda, "Camisa Azul chica");
    store->items[0].cantidad = 2;

    strcpy(store->items[1].prenda, "Pantalon verde mediano");
    store->items[1].cantidad = 3;

    strcpy(store->items[2].prenda, "Tennis negros chicos");
    store->items[2].cantidad = 5;

    strcpy(store->items[3].prenda, "Gorro cafe grande");
    store->items[3].cantidad = 7;

    strcpy(store->items[4].prenda, "Gafas de sol grandes");
    store->items[4].cantidad = 11;
    store->size = MAX_ITEMS;
}

void tienda_imprimir(Tienda *store) {
    printf("Prenda\tCantidad disponible\n");
    for (int i = 0; i < store->size; i++)
        printf("%s:\t%d\n", store->items[i].prenda, store->items[i].cantidad);
}

// Comprar un artículo en la tienda
void tienda_comprar(Tienda *store, int itemIndex, char *result, int *cantidad) {
    if (store->items[itemIndex].cantidad == 0) {
        strcpy(result, store->items[itemIndex].prenda);
        *cantidad = -1;
        return;
    }
    store->items[itemIndex].cantidad--;
    strcpy(result, store->items[itemIndex].prenda);
    *cantidad = store->items[itemIndex].cantidad;
}

// Reabastecer un artículo en la tienda
void tienda_reabastecer(Tienda *store, int itemIndex, char *result, int *cantidad) {
    store->items[itemIndex].cantidad = (store->items[itemIndex].cantidad * 2) + 1;
    strcpy(result, store->items[itemIndex].prenda);
    *cantidad = store->items[itemIndex].cantidad;
}

// Función para entrar en la sección crítica
void entrar_seccion_critica(int id) {
    int otro = 1 - id;
    flag[id] = true;
    while (flag[otro]) {
        if (turn == otro) {
            flag[id] = false;
            while (turn == otro) {}
            flag[id] = true;
        }
    }
}

// Función para salir de la sección crítica
void salir_seccion_critica(int id) {
    int otro = 1 - id;
    turn = otro;
    flag[id] = false;
}

// Función que ejecuta el hilo 1 (cliente)
void *hilo1(void *arg) {
    ArgumentosHilo *args = (ArgumentosHilo *)arg;
    char result[MAX_NAME_LENGTH];
    int cantidad;

    int random_item = rand() % args->store->size;

    entrar_seccion_critica(args->id); // Entrar en la sección crítica

    // Sección crítica
    tienda_comprar(args->store, random_item, result, &cantidad);

    salir_seccion_critica(args->id); // Salir de la sección crítica

    printf("%s ha comprado: %s - Existencias restantes: %d\n", args->nombre, result, cantidad);

    free(args); 
    return NULL;
}

// Función que ejecuta el hilo 2 (proveedor)
void *hilo2(void *arg) {
    ArgumentosHilo *args = (ArgumentosHilo *)arg;
    char result[MAX_NAME_LENGTH];
    int cantidad;

    int random_item = rand() % args->store->size;

    entrar_seccion_critica(args->id); // Entrar en la sección crítica

    // Sección crítica
    tienda_reabastecer(args->store, random_item, result, &cantidad);

    salir_seccion_critica(args->id); // Salir de la sección crítica

    printf("%s ha reabastecido: %s - Prendas actualizadas: %d\n", args->nombre, result, cantidad);

    free(args); 
    return NULL;
}

int main() {
    pthread_t hilos[2];
    Tienda store;
    tienda_iniciar(&store);
    srand(time(NULL)); 

    printf("Estado inicial de la tienda:\n");
    tienda_imprimir(&store);
    printf("\n");

    // Crear los dos hilos
    ArgumentosHilo *args1 = malloc(sizeof(ArgumentosHilo));
    strcpy(args1->nombre, "Cliente");
    args1->store = &store;
    args1->id = 0;

    ArgumentosHilo *args2 = malloc(sizeof(ArgumentosHilo));
    strcpy(args2->nombre, "Proveedor");
    args2->store = &store;
    args2->id = 1;

    pthread_create(&hilos[0], NULL, hilo1, args1);
    pthread_create(&hilos[1], NULL, hilo2, args2);

    // Esperar a que los hilos terminen
    pthread_join(hilos[0], NULL);
    pthread_join(hilos[1], NULL);

    printf("\nEstado final de la tienda:\n");
    tienda_imprimir(&store);

    return 0;
}