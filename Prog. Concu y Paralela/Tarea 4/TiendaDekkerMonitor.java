import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public class TiendaDekkerMonitor {
    static class MonitorDekker {
        private int turno = 0;

        public synchronized void entrar(int hiloId) {
            while (turno != hiloId) {
                try {
                    wait();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }

        public synchronized void salir(int hiloId) {
            turno = 1 - hiloId;
            notifyAll();
        }
    }

    public static class Tienda {
        private HashMap<String, Integer> stock = new HashMap<>();
        ArrayList<String> prendas;

        public Tienda() {
            stock.put("Camisa Azul chica", 2);
            stock.put("Pantalon verde mediano", 3);
            stock.put("Tennis negros chicos", 5);
            prendas = new ArrayList<>(stock.keySet());
        }

        public String[] comprar(int numPrenda) {
            String prenda = prendas.get(numPrenda);
            Integer cantidad = stock.get(prenda);

            if (cantidad == 0)
                return new String[]{prenda, null};

            stock.put(prenda, cantidad - 1);
            return new String[]{prenda, String.valueOf(cantidad - 1)};
        }

        public Integer getSize() { return stock.size(); }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append("Prenda\tCantidad disponible\n");
            stock.forEach(
                    (k, v) -> sb.append(k).append(":\t").append(v).append("\n"));
            return sb.toString();
        }
    }

    abstract static class OperadorTienda implements Runnable {
        protected final MonitorDekker monitor;
        protected final Tienda tienda;
        protected final int hiloId;
        protected final int id;

        public OperadorTienda(int id, Tienda tienda, int hiloId, MonitorDekker monitor) {
            this.id = id;
            this.tienda = tienda;
            this.hiloId = hiloId;
            this.monitor = monitor;
        }
    }

    static class Cliente extends OperadorTienda {
        private final String client;

        public Cliente(String client, int id, Tienda tienda, int hiloId, MonitorDekker monitor) {
            super(id, tienda, hiloId, monitor);
            this.client = client;
        }

        @Override
        public void run() {
            Random rand = new Random();
            Integer random = rand.nextInt(tienda.getSize());

            monitor.entrar(hiloId);
            try {
                //SECCION CRITICA
                String[] resultado = tienda.comprar(random);
                //SECCION CRITICA

                if (resultado[1] == null)
                    System.err.println(client + " quiso comprar " + resultado[0] +
                            " pero ya no hay existencias");
                else
                    System.out.println("- " + client + " ha comprado: " + resultado[0] +
                            " - Existencias restantes: " + resultado[1] +
                            ", saliendo de la tienda...");
            } finally {
                monitor.salir(hiloId);
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        MonitorDekker monitor = new MonitorDekker();
        Tienda inst = new Tienda();
        System.out.println(inst.toString());

        Thread[] hilos = new Thread[2];
        hilos[0] = new Thread(new Cliente("Pedro", 1, inst, 0, monitor));
        hilos[1] = new Thread(new Cliente("Luis", 2, inst, 1, monitor));

        for (Thread hilo : hilos)
            hilo.start();

        for (Thread hilo : hilos)
            hilo.join();

        System.out.println("\n" + inst.toString());
    }
}