#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#define MAX_ITEMS 5
#define MAX_NAME_LENGTH 50

typedef struct {
    char prenda[MAX_NAME_LENGTH];
    int cantidad;
} Articulo;

typedef struct {
    Articulo items[MAX_ITEMS];
    int size;
} Tienda;

typedef struct {
    char prenda[MAX_NAME_LENGTH];
    Tienda* store;
} ArgumentosHilo;

int turno = 0;
int quiere_cliente = 0;
int quiere_proveedor = 0;

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
}

void tienda_comprar(Tienda* store, int itemIndex, char* result, int* cantidad) {
    if (store->items[itemIndex].cantidad == 0) {
        strcpy(result, store->items[itemIndex].prenda);
        *cantidad = -1;
        return;
    }
    
    store->items[itemIndex].cantidad--;
    strcpy(result, store->items[itemIndex].prenda);
    *cantidad = store->items[itemIndex].cantidad;
}


void tienda_reabastecer(Tienda* store, int itemIndex, char* result, int* cantidad) {
    store->items[itemIndex].cantidad = (store->items[itemIndex].cantidad * 2) + 1;
    strcpy(result, store->items[itemIndex].prenda);
    *cantidad = store->items[itemIndex].cantidad;
}

// Función de exclusión mutua del algoritmo de Dekker
void entrar_criterio(int proceso) {
    if (proceso == 0) { // Cliente
        quiere_cliente = 1;
        while (quiere_proveedor == 1) {
            if (turno == 1) {
                quiere_cliente = 0;
                while (turno == 1) {
                    // Esperar a que el proveedor termine
                }
                quiere_cliente = 1;
            }
        }
    } else { // Proveedor
        quiere_proveedor = 1;
        while (quiere_cliente == 1) {
            if (turno == 0) {
                quiere_proveedor = 0;
                while (turno == 0) {
                    // Esperar a que el cliente termine
                }
                quiere_proveedor = 1;
            }
        }
    }
}

void salir_criterio(int proceso) {
    if (proceso == 0) { // Cliente
        turno = 1;
        quiere_cliente = 0;
    } else { // Proveedor
        turno = 0;
        quiere_proveedor = 0;
    }
}

// Función del hilo de cliente
void* hilo_cliente(void* arg) {
    ArgumentosHilo* args = (ArgumentosHilo*)arg;
    char result[MAX_NAME_LENGTH];
    int cantidad;
    
    int random_item = rand() % args->store->size;

    // Entrar a la sección crítica utilizando Dekker
    entrar_criterio(0);

    // Sección crítica
    tienda_comprar(args->store, random_item, result, &cantidad);
    // Fin de la sección crítica

    salir_criterio(0);
    
    if (cantidad == -1) {
        fprintf(stderr, "%s quiso comprar %s pero ya no hay existencias\n", 
                args->prenda, result);
    } else {
        printf("- %s ha comprado: %s - Existencias restantes: %d, saliendo de la tienda...\n",
               args->prenda, result, cantidad);
    }
    
    free(arg);
    return NULL;
}

// Función del hilo de proveedor
void* hilo_proveedor(void* arg) {
    ArgumentosHilo* args = (ArgumentosHilo*)arg;
    char result[MAX_NAME_LENGTH];
    int cantidad;
    
    int random_item = rand() % args->store->size;

    // Entrar a la sección crítica utilizando Dekker
    entrar_criterio(1);

    // Sección crítica
    tienda_reabastecer(args->store, random_item, result, &cantidad);
    // Fin de la sección crítica

    salir_criterio(1);
    
    printf("- Proveedor %s ha reabastecido: %s - Prendas actualizadas: %d\n",
           args->prenda, result, cantidad);
    
    free(arg);
    return NULL;
}

int main() {
    Tienda store;
    tienda_iniciar(&store);
    
    printf("Estado inicial de la tienda:\n");
    tienda_imprimir(&store);
    printf("\n");
    
    pthread_t clientes[4], proveedores[2];
    
    // Crear hilos de clientes
    char* nombres_clientes[] = {"Pedro", "Luis", "Jorge", "Jose"};
    for (int i = 0; i < 4; i++) {
        ArgumentosHilo* args = malloc(sizeof(ArgumentosHilo));
        strcpy(args->prenda, nombres_clientes[i]);
        args->store = &store;
        pthread_create(&clientes[i], NULL, hilo_cliente, args);
    }
    
    // Crear hilos de proveedores
    char* ids_proveedores[] = {"2099", "73"};
    for (int i = 0; i < 2; i++) {
        ArgumentosHilo* args = malloc(sizeof(ArgumentosHilo));
        strcpy(args->prenda, ids_proveedores[i]);
        args->store = &store;
        pthread_create(&proveedores[i], NULL, hilo_proveedor, args);
    }
    
    // Esperamos a que los hilos terminen
    for (int i = 0; i < 4; i++) 
        pthread_join(clientes[i], NULL);
    for (int i = 0; i < 2; i++) 
        pthread_join(proveedores[i], NULL);
    
    tienda_imprimir(&store);  
    
    return 0;
}