import java.util.ArrayList;
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicInteger;

public class TiendaSemaforos {

  // recurso compartido, en este caso acceso a la tienda
  public static class Tienda {
    private ConcurrentHashMap<String, AtomicInteger> stock =
        new ConcurrentHashMap<>();
    private ArrayList<String> prendas;

    public Tienda() {
      stock.put("Camisa Azul chica", new AtomicInteger(2));
      stock.put("Pantalon verde mediano", new AtomicInteger(3));
      stock.put("Tennis negros chicos", new AtomicInteger(5));
      stock.put("Gorro cafe grande", new AtomicInteger(7));
      stock.put("Gafas de sol grandes", new AtomicInteger(11));
      prendas = new ArrayList<>(stock.keySet());
    }

    public String[] comprar(int numPrenda) {
      String prenda = prendas.get(numPrenda);
      AtomicInteger cantidad = stock.get(prenda);

      if (cantidad.get() == 0)
        return new String[] {prenda, null};

      cantidad
          .decrementAndGet(); // quitamos 1 del stock disponible de la prenda
      return new String[] {prenda, String.valueOf(cantidad)};
    }

    public String[] agregar(int numPrenda) {
      String prenda = prendas.get(numPrenda);
      AtomicInteger cantidad = stock.get(prenda);

      int actual = cantidad.get();
      cantidad.set(actual * 2 + 1);

      return new String[] {prenda, String.valueOf(cantidad.get())};
		} 

    public Integer getSize() { return stock.size(); }

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder();
      sb.append("Prenda \tCantidad disponible\n");
      stock.forEach(
          (k, v) -> sb.append(k).append(":\t").append(v.get()).append("\n"));
      return sb.toString();
    }
  }

  // usuarios como hilos
  public static class Cliente extends Thread {
    private String client;
    private Tienda tienda;
    private Semaphore semaforo;

    Cliente(String client, Tienda tienda, Semaphore semaforo) {
      this.client = client;
      this.tienda = tienda;
      this.semaforo = semaforo;
    }

    @Override
    public void run() {
      Random rand = new Random();
      Integer random = rand.nextInt(tienda.getSize());
      try {
        semaforo.acquire(); // intentamos acceder a la tienda
        // SECCION CRITICA
        String[] resultado = tienda.comprar(random);
        // SECCION CRITICA

        if (resultado[1] == null)
          System.err.println(client + " quiso comprar " + resultado[0] +
                             " pero ya no hay existencias");
        else
          System.out.println("- " + client + " ha comprado: " + resultado[0] +
                             " - Existencias restantes: " + resultado[1] +
                             ", saliendo de la tienda...");
      } catch (InterruptedException e) {
        e.printStackTrace();
      } finally {
        semaforo.release(); // liberamos el semaforo para que siga otro hilo
      }
    }
  }

  public static class Provedores extends Thread {
    private Tienda tienda;
    private Integer id;
    private Semaphore semaforo;

    Provedores(Integer id, Tienda tienda, Semaphore semaforo) {
      this.id = id;
      this.tienda = tienda;
      this.semaforo = semaforo;
    }

    @Override
    public void run() {
      Random rand = new Random();
      Integer random = rand.nextInt(tienda.getSize());
      try {
        semaforo.acquire();

        // SECCION CRITICA
        String[] resultado = tienda.agregar(random);
        // SECCION CRITICA

        System.out.println("- Proveedor " + id +
                           " ha reabastecido: " + resultado[0] +
                           " - Prendas actualizadas: " + resultado[1]);
      } catch (InterruptedException e) {
        e.printStackTrace();
      } finally {
        semaforo.release();
      }
    }
  }

  public static void main(String[] args) {
    Tienda inst = new Tienda();
    Semaphore semaforo =
        new Semaphore(3); // semaforo de tamaño 2, es decir, solo pueden acceder
    // dos hilos a la seccion critica a la vez
    System.out.println(inst.toString()); // tienda al principio

    Cliente cliente1 = new Cliente("Pedro", inst, semaforo);
    Cliente cliente2 = new Cliente("Luis", inst, semaforo);
    Cliente cliente3 = new Cliente("Jorge", inst, semaforo);
    Cliente cliente4 = new Cliente("Jose", inst, semaforo);
    Provedores provedor1 = new Provedores(2099, inst, semaforo);
    Provedores provedor2 = new Provedores(73, inst, semaforo);

    cliente1.start();
    provedor1.start();
    cliente2.start();
    cliente3.start();
    provedor2.start();
    cliente4.start();

    try {
      cliente1.join();
      provedor1.join();
      cliente2.join();
      cliente3.join();
      provedor2.join();
      cliente4.join();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }

    System.out.println("\n" + inst.toString()); // tienda al final
  }
}
