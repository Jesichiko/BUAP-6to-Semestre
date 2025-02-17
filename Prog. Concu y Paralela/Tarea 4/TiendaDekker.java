import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public class TiendaDekker {
    //variables compartidas para dekker
    private static volatile boolean[] flag = {false, false};  //intencion de entrar
    private static volatile int turn = 0;                     //turno

    public static class Tienda {
        private HashMap<String, Integer> stock = new HashMap<>();
        ArrayList<String> prendas;

        public Tienda() {
            stock.put("Camisa Azul chica", 2);
            stock.put("Pantalon verde mediano", 3);
            stock.put("Tennis negros chicos", 5);
            stock.put("Gorro cafe grande", 7);
            stock.put("Gafas de sol grandes", 11);
            prendas = new ArrayList<>(stock.keySet());
        }

        public String[] comprar(int numPrenda) {
            String prenda = prendas.get(numPrenda);
            Integer cantidad = stock.get(prenda);

            if (cantidad == 0)
                return new String[]{prenda, null};

            stock.put(prenda, cantidad -1); // quitamos 1 del stock disponible de la prenda
            return new String[]{prenda, String.valueOf(cantidad)};
        }

        public String[] agregar(int numPrenda) {
            String prenda = prendas.get(numPrenda);
            Integer cantidad = (stock.get(prenda) * 2) + 1;

            stock.put(prenda, cantidad);
            return new String[]{prenda, String.valueOf(cantidad)};
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

    //Clase abstracta que sera la base 
    //para aplicar dekker tanto en Cliente como en Proveedor
    static abstract class OperadorTienda implements Runnable {
        protected final int id;
        protected final Tienda tienda;
        protected final int procesoId; //0 o 1 para Dekker

        public OperadorTienda(int id, Tienda tienda, int procesoId) {
            this.id = id;
            this.tienda = tienda;
            this.procesoId = procesoId;
        }

        protected void entrarSeccionCritica() {
            flag[procesoId] = true;
            int otro = 1 - procesoId;
            while (flag[otro]) 
                if (turn != procesoId) {
                    flag[procesoId] = false;
                    while (turn != procesoId) 
                        Thread.yield(); // Permite que otro proceso se ejecute
                    flag[procesoId] = true;
                }
        }

        protected void salirSeccionCritica() {
            turn = 1 - procesoId;
            flag[procesoId] = false;
        }
    }

    //cliente usando Dekker
    static class Cliente extends OperadorTienda {
        private final String client;

        public Cliente(String client, int id, Tienda tienda, int procesoId) {
            super(id, tienda, procesoId);
            this.client = client;
        }

        @Override
        public void run() {
            Random rand = new Random();
            Integer random = rand.nextInt(tienda.getSize()); //[0,getSize() )

            entrarSeccionCritica();
            try {
                //SECCION CRITICA
                String[] resultado = tienda.comprar(random);
                //SECCION CRITICA

                if (resultado[1] == null)
                System.err.println(client + " quiso comprar " + resultado[0] +
                                    " pero ya no hay existencias");
                else
                System.out.println("- " +client + " ha comprado: " + resultado[0] +" - Existencias restantes: "
                                    + resultado[1] +", saliendo de la tienda...");
            } finally {
                salirSeccionCritica();
            }
        }
    }

    //proveedor usando Dekker
    static class Proveedor extends OperadorTienda {
        public Proveedor(int id, Tienda tienda, int procesoId) {
            super(id, tienda, procesoId);
        }

        @Override
        public void run() {
            Random rand = new Random();
            Integer random = rand.nextInt(tienda.getSize()); //[0,getSize() )

            entrarSeccionCritica();
            try {

                //SECCION CRITICA
                String[] resultado = tienda.agregar(random);
                //SECCION CRITICA

                System.out.println("- Proveedor " + id + " ha reabastecido: " + resultado[0] 
                          + " - Prendas actualizadas: " +resultado[1]);
            } finally {
                salirSeccionCritica();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Tienda inst = new Tienda();
        System.out.println(inst.toString()); //tienda al principio

        //creamos los hilos alternando entre proceso 0 y 1
        Thread[] hilos = new Thread[6];
        hilos[0] = new Thread(new Cliente("Pedro", 1, inst, 0));
        hilos[1] = new Thread(new Proveedor(2099, inst, 1));
        hilos[2] = new Thread(new Cliente("Luis", 2, inst, 0));
        hilos[3] = new Thread(new Cliente("Jorge", 3, inst, 1));
        hilos[4] = new Thread(new Proveedor(73, inst, 0));
        hilos[5] = new Thread(new Cliente("Jose", 4, inst, 1));

        //iniciamos los hilos
        for (Thread hilo : hilos)
            hilo.start();

        //esperamos a que terminen
        for (Thread hilo : hilos)
            hilo.join();

        System.out.println("\n"+inst.toString()); //tienda al final
    }
}