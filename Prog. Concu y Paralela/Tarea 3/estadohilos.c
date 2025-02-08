#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t bloqueado;
void* hilo1estados(void* arg) {
    printf("Hilo1 creado y listo para ejecutarse\n");
    sleep(1);
    printf("Hilo1 ejecutandose\n");
    printf("Hilo1 bloqueado\n");
    pthread_mutex_lock(&bloqueado);
    sleep(2);   
    printf("Hilo1 desbloqueado\n");
    pthread_mutex_unlock(&bloqueado);
    pthread_exit(NULL);
}
void* hilo2estados(void* arg) {
    printf("Hilo2 creado y listo para ejecutarse\n");
    sleep(2);
    printf("Hilo2 desbloqueando el hilo 1\n");
    pthread_mutex_unlock(&bloqueado);
    printf("Hilo2 terminado ejecucion\n");
    pthread_exit(NULL);
}

int main() {
    pthread_t hilo1,hilo2;
    pthread_mutex_init(&bloqueado, NULL);
    pthread_mutex_lock(&bloqueado);
    pthread_create(&hilo1, NULL, hilo1estados, NULL);
    pthread_create(&hilo2, NULL, hilo2estados, NULL);
    pthread_join(hilo1, NULL);
    pthread_join(hilo2, NULL);
    pthread_mutex_destroy(&bloqueado);
    printf("Programa terminado\n");
    return 0;
}