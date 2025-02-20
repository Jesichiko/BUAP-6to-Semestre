package Monitores;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public class TiendaDekkerMonitor {
    
    public static class MonitorDekker {
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

    public static class Cliente extends Thread {
        private final MonitorDekker monitor;
        private final String nombre;
        private final Tienda tienda;
        private final int hiloId;

        public Cliente(String nombre, Tienda tienda, int hiloId, MonitorDekker monitor) {
            this.nombre = nombre;
            this.tienda = tienda;
            this.hiloId = hiloId;
            this.monitor = monitor;
        }

        @Override
        public void run() {
            int random = new Random().nextInt(tienda.getSize());

            monitor.entrar(hiloId);
            try {
                //SECCION CRITICA
                String[] resultado = tienda.comprar(random);
                //SECCION CRITICA

                if (resultado[1] == null)
                    System.err.println(nombre + " quiso comprar " + resultado[0] + 
                            " pero ya no hay existencias");
                else
                    System.out.println("- " + nombre + " ha comprado: " + resultado[0] +
                            " - Existencias restantes: " + resultado[1]);
            } finally {
                monitor.salir(hiloId);
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        MonitorDekker monitor = new MonitorDekker();
        Thread[] hilos = new Thread[2];
        Tienda inst = new Tienda();
       
        System.out.println(inst.toString());
        hilos[0] = new Cliente("Pedro", inst, 0, monitor);
        hilos[1] = new Cliente("Luis", inst, 1, monitor);

        for (Thread hilo : hilos)
            hilo.start();

        for (Thread hilo : hilos)
            hilo.join();
        System.out.println("\n" + inst.toString());
    }
}