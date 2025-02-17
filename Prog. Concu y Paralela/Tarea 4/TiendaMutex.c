#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_ITEMS 5
#define MAX_NAME_LENGTH 50

// estructura para representar cada item de la tienda
typedef struct {
  char prenda[MAX_NAME_LENGTH];
  int cantidad;
} Articulo;

// estructura para representar la tienda
typedef struct {
  Articulo items[MAX_ITEMS];
  int size;
  pthread_mutex_t mutex;
} Tienda;

// estructura para pasar los argumentos a los hilos
typedef struct {
  char prenda[MAX_NAME_LENGTH];
  Tienda *store;
} ArgumentosHilo;

// Inicializar la tienda
void tienda_iniciar(Tienda *store) {
  pthread_mutex_init(&store->mutex, NULL);

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
void tienda_reabastecer(Tienda *store, int itemIndex, char *result,
                        int *cantidad) {
  store->items[itemIndex].cantidad = (store->items[itemIndex].cantidad * 2) + 1;
  strcpy(result, store->items[itemIndex].prenda);
  *cantidad = store->items[itemIndex].cantidad;
}

// Función del hilo de cliente
void *hilo_cliente(void *arg) {
  ArgumentosHilo *args = (ArgumentosHilo *)arg;
  char result[MAX_NAME_LENGTH];
  int cantidad;

  int random_item = rand() % args->store->size;

  pthread_mutex_lock(&args->store->mutex);
  // Sección crítica
  tienda_comprar(args->store, random_item, result, &cantidad);
  // Fin de la sección crítica
  pthread_mutex_unlock(&args->store->mutex);

  if (cantidad == -1) {
    fprintf(stderr, "%s quiso comprar %s pero ya no hay existencias\n",
            args->prenda, result);
  } else {
    printf("- %s ha comprado: %s - Existencias restantes: %d, saliendo de la "
           "tienda...\n",
           args->prenda, result, cantidad);
  }

  free(arg);
  return NULL;
}

// Función del hilo de proveedor
void *hilo_proveedor(void *arg) {
  ArgumentosHilo *args = (ArgumentosHilo *)arg;
  char result[MAX_NAME_LENGTH];
  int cantidad;

  int random_item = rand() % args->store->size;

  pthread_mutex_lock(&args->store->mutex);
  // Sección crítica
  tienda_reabastecer(args->store, random_item, result, &cantidad);
  // Fin de la sección crítica
  pthread_mutex_unlock(&args->store->mutex);

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
  char *nombres_clientes[] = {"Pedro", "Luis", "Jorge", "Jose"};
  for (int i = 0; i < 4; i++) {
    ArgumentosHilo *args = malloc(sizeof(ArgumentosHilo));
    strcpy(args->prenda, nombres_clientes[i]);
    args->store = &store;
    pthread_create(&clientes[i], NULL, hilo_cliente, args);
  }

  // Crear hilos de proveedores
  char *ids_proveedores[] = {"2099", "73"};
  for (int i = 0; i < 2; i++) {
    ArgumentosHilo *args = malloc(sizeof(ArgumentosHilo));
    strcpy(args->prenda, ids_proveedores[i]);
    args->store = &store;
    pthread_create(&proveedores[i], NULL, hilo_proveedor, args);
  }

  // esperamos a que los hilos terminen
  for (int i = 0; i < 4; i++)
    pthread_join(clientes[i], NULL);
  for (int i = 0; i < 2; i++)
    pthread_join(proveedores[i], NULL);

  tienda_imprimir(&store);
  pthread_mutex_destroy(&store.mutex);
  return 0;
}
