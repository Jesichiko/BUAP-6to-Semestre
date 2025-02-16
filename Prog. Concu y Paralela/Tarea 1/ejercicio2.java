import java.util.Random;
import java.util.Vector;

public class ejercicio2 {
	 public static class Hilo extends Thread{
        int sum = 0, cuadrados = 0;
        Vector<Integer> vect;
        double media;

        Hilo(Vector<Integer> vect){
            this.vect = vect;
        }

        @Override
        public void run(){
            System.out.println("Vector: \n");
            for (int x : vect) {
                System.out.print(x + ", ");
                sum += x;
                cuadrados += x * x;
            }
            media = sum / vect.size();
            System.out.println("Suma: " +sum +"\nSuma de cuadrados: " +cuadrados + "\nMedia: "+media);
        }
    }

    public static Vector<Integer> llenado(int size){
        Vector<Integer> vect = new Vector<>(size);
        Random random = new Random();

        for(int i = 0; i < size; i++)
            vect.add(random.nextInt());
        return vect;
    }

    public static void main(String[] args){
        int size = 0;

        if(args.length != 1){
            System.err.println("Necesitas dar el tamaño del vector");
            System.exit(-1);
        }

        try {
            size = Integer.valueOf(args[0]);
        } catch (NumberFormatException e) {
            System.err.println("Da valores solo numericos");
            System.exit(-1);
        }
     
        Hilo hilo = new Hilo(llenado(size));
        hilo.start();
    }
}
