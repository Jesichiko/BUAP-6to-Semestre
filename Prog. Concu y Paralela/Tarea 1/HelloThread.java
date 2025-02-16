//Codigo 1
public class HelloThread extends Thread{
    @Override
    public void run(){
        System.out.println("Hello from a thread!");
    }
    public static void main(String[] args){
        (new HelloThread()).start();
    }
}

//Codigo 2
class HelloRunnable implements Runnable{
    @Override
    public void run(){
        System.out.println("Hello from a thread!");
    }
    
    public static void main(String[] args) {
        (new Thread( new HelloRunnable())).start();
    }
}

// Codigo 3
class RunnableDemo implements Runnable{
    private Thread t;
    private final String threadName;
    
    RunnableDemo(String name){
        threadName = name;
        System.out.println("Creating " + threadName);
    }
    
    @Override
    public void run(){
        System.out.println("Running " + threadName);
        try{
            for(int i = 4; i > 0; i--){
                System.out.println("Thread " + threadName + ", " + i);
                Thread.sleep(50);
            }
        }catch(InterruptedException e){
            System.out.println("Thread" + threadName + " interrupted");
        }
        System.out.println("Thread " + threadName + " exiting");
    }
    
    public void start(){
        System.out.println("Starting " + threadName);
        if(t == null){
            t = new Thread(this, threadName);
            t.start();
        }
    }
    
    public static void main(String[] args) {
        RunnableDemo R1 = new RunnableDemo("Thread-1");
        R1.start();
        
        RunnableDemo R2 = new RunnableDemo("Thread-2");
        R2.start();
    }
}
