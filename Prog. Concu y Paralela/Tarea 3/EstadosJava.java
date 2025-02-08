public class EstadosJava {
    static final Object lock = new Object(); //Objeto de ejemplo para estado blocked
    static int recurso = 0;

    public static class Hilo1 extends Thread {

        @Override
        public void run() {
            
            synchronized (lock) {
                System.out.println("El hilo 1 tiene el recurso lock");
                recurso++;
                //Se notifica al hilo 2 para que salga del estado Blocked
                lock.notifyAll();
            }
            System.out.println("Resultado hilo 1: " + recurso);

        }
    }

    public static class Hilo2 extends Thread {

        @Override
        public void run() {

            synchronized (lock) {

                try {
                    //Estado Blocked, esperamos al hilo 1 a que libere al recurso y despues de esto podemos seguir
                    System.out.println("Hilo 2 esperando a que hilo 1 libere el recurso...");
                    lock.wait();
                } catch (InterruptedException e) {e.printStackTrace();}
                System.out.println("El hilo 2 tiene el recurso lock");
                recurso *= 10;

            }
            System.out.println("Resultado hilo 2: " + recurso);

        }

    }


    public static void main(String[] args) {
        //Estado ready (new en java)
        Hilo1 instancia1 = new Hilo1();
        Hilo2 instancia2 = new Hilo2();

        System.out.println("Estado de Hilo1: " + instancia1.getState()); //new
        System.out.println("Estado de Hilo2: " + instancia2.getState()); //new

        //Estado running (runnable)
        instancia2.start();
        try {
            Thread.sleep(100); //Damos tiempo a que Hilo2 entre en wait()
        } catch (InterruptedException e) {}

        instancia1.start();

        System.out.println("Estado de Hilo1: " + instancia1.getState()); //runnable
        System.out.println("Estado de Hilo2: " + instancia2.getState()); //waiting

        //Estado waiting
        try {
            instancia1.join();
            instancia2.join();
        } catch (InterruptedException e) {e.printStackTrace();}

        //Estado terminated
        System.out.println("Estado de Hilo1: " + instancia1.getState()); //terminated
        System.out.println("Estado de Hilo2: " + instancia2.getState()); //terminated
        //esto es lo mismo que instancia1.stop(); y instancia2.stop(), ambos terminan el hilo
    }
}