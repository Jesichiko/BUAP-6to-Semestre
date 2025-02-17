import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.Semaphore;

public class TiendaSemaforos{

  // recurso compartido, en este caso acceso a la tienda
  public static class Tienda {
    private HashMap<String, Integer> stock =
        new HashMap<>(); // diccionario para almacenar el stock

    public Tienda() {
      stock.put("Camisa Azul chica", 2);
      stock.put("Pantalon verde mediano", 3);
      stock.put("Tennis negros chicos", 5);
      stock.put("Gorro cafe grande", 7);
      stock.put("Gafas de sol grandes", 11);
    }

    public String comprar(int numPrenda) {
      ArrayList<String> prendas = new ArrayList<>(stock.keySet());
      String prenda = prendas.get(numPrenda);

      if (stock.get(prenda).equals(0))
        return null;

      stock.put(prenda, stock.get(prenda) -
                            1); // quitamos 1 del stock disponible de la prenda
      return prenda;
    }

    public String agregar(int numPrenda) {
      ArrayList<String> prendas = new ArrayList<>(stock.keySet());
      String prenda = prendas.get(numPrenda);
      Integer cantidad = (stock.get(prenda) * 2) + 1;
      stock.put(prenda, cantidad);
      return prenda;
    }

    public Integer getSize() { return stock.size(); }

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder();
      sb.append("Prenda \tCantidad disponible\n");
      stock.forEach(
          (k, v) -> sb.append(k).append(":\t").append(v).append("\n"));
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
      Integer random = rand.nextInt(1, tienda.getSize());
      try {
        semaforo.acquire(); // intentamos acceder a la tienda
        // SECCION CRITICA
        String prenda = tienda.comprar(random);
        // SECCION CRITICA

        if (prenda.equals(null))
          System.err.println(client + " quiso comprar " + prenda +
                             " pero ya no hay existencias");
        else
          System.out.println(client + " ha comprado: " + prenda +
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
      Integer random = rand.nextInt(1, tienda.getSize());
      try {
        semaforo.acquire();

        // SECCION CRITICA
        String prenda = tienda.agregar(random);
        // SECCION CRITICA

        System.out.println("Proveedor " + id + " ha reabastecido: " + prenda);
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
        new Semaphore(1); // semaforo de tamaño 1, es decir, solo puede acceder
													// un solo hilo a la seccion critica
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

    System.out.println("\n"+inst.toString()); // tienda al final
  }
}