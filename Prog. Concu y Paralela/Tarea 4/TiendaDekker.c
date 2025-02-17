#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>

#define MAX_ITEMS 5
#define MAX_NAME_LENGTH 50

volatile int turno = 0;
volatile int quiere_cliente[2] = {0, 0};

typedef struct {
    char prenda[MAX_NAME_LENGTH];
    int cantidad;
} Articulo;

typedef struct {
    Articulo items[MAX_ITEMS];
    int size;
} Tienda;

typedef struct {
    char nombre[MAX_NAME_LENGTH];
    Tienda* store;
    int id;
} ArgumentosHilo;

void tienda_iniciar(Tienda* store) {
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

void tienda_imprimir(Tienda* store) {
    printf("Prenda\tCantidad disponible\n");
    for (int i = 0; i < store->size; i++) 
        printf("%s:\t%d\n", store->items[i].prenda, store->items[i].cantidad);
    printf("\n");
}

void tienda_comprar(Tienda* store, int itemIndex, char* result, int* cantidad, int id) {
    int otro = 1 - id;
    
    quiere_cliente[id] = 1;
    while (quiere_cliente[otro]) {
        if (turno != id) {
            quiere_cliente[id] = 0;
            while (turno != id);
            quiere_cliente[id] = 1;
        }
    }
    
    // Sección crítica
    if (store->items[itemIndex].cantidad == 0) {
        strcpy(result, store->items[itemIndex].prenda);
        *cantidad = -1;
    } else {
        store->items[itemIndex].cantidad--;
        strcpy(result, store->items[itemIndex].prenda);
        *cantidad = store->items[itemIndex].cantidad;
    }
    // Fin de la sección crítica
    
    turno = otro;
    quiere_cliente[id] = 0;
}

void* hilo_cliente(void* arg) {
    ArgumentosHilo* args = (ArgumentosHilo*)arg;
    char result[MAX_NAME_LENGTH];
    int cantidad;
    
    // Inicializar la semilla de rand() con el tiempo actual más el ID del hilo
    srand(time(NULL) + args->id);
    
    int random_item = rand() % args->store->size;
    
    tienda_comprar(args->store, random_item, result, &cantidad, args->id);
    
    if (cantidad == -1) {
        fprintf(stderr, "%s quiso comprar %s pero ya no hay existencias\n", 
                args->nombre, result);
    } else {
        printf("- %s ha comprado: %s - Existencias restantes: %d, saliendo de la tienda...\n",
               args->nombre, result, cantidad);
    }
    
    free(arg);
    return NULL;
}

int main() {
    Tienda store;
    tienda_iniciar(&store);
    
    printf("Estado inicial de la tienda:\n");
    tienda_imprimir(&store);

    pthread_t clientes[2];
    char* nombres_clientes[] = {"Pedro", "Jose"};
    
    for (int i = 0; i < 2; i++) {
        ArgumentosHilo* args = malloc(sizeof(ArgumentosHilo));
        strcpy(args->nombre, nombres_clientes[i]);
        args->store = &store;
        args->id = i;
        pthread_create(&clientes[i], NULL, hilo_cliente, args);
    }
    
    // Esperar a que los hilos terminen
    for (int i = 0; i < 2; i++) 
        pthread_join(clientes[i], NULL);
    
    printf("\nEstado final de la tienda:\n");
    tienda_imprimir(&store);
    
    return 0;
}