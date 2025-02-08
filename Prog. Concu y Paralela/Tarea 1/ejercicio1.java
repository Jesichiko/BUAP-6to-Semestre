public class ejercicio1{
    
    public static class Pares extends Thread{
        @Override
        public void run() {
            for(int i = 0; i <= 10; i+=2){
                System.out.println(i);
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static class Impares implements Runnable{
        @Override
        public void run(){
            for(int i = 1; i <= 10; i+=2){
                System.out.println(i);
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) {
         Pares hilo1 = new Pares();
        Thread hilo2 = new Thread(new Impares());

        hilo1.start();
        hilo2.start();
    }
}