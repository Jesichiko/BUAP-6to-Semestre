import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public class TiendaDekker {
	// variables compartidas para dekker
	private static volatile boolean[] flag = {
			false, false }; // banderas para indicar que un hilo quiere entrar a la
											// seccion critica
	private static volatile int turno = 0; // var de turno, decide quien de varios hilos entra si ambos lo desean

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
				return new String[] { prenda, null };

			stock.put(prenda,
					cantidad - 1); // quitamos 1 del stock disponible de la prenda
			return new String[] { prenda, String.valueOf(cantidad - 1) };
		}

		public Integer getSize() {
			return stock.size();
		}

		@Override
		public String toString() {
			StringBuilder sb = new StringBuilder();
			sb.append("Prenda\tCantidad disponible\n");
			stock.forEach(
					(k, v) -> sb.append(k).append(":\t").append(v).append("\n"));
			return sb.toString();
		}
	}

	// Clase abstracta que sera la base
	// para aplicar dekker tanto en Cliente como en Proveedor
	abstract static class OperadorTienda implements Runnable {
		protected final int id;
		protected final Tienda tienda;
		protected final int hiloId; // 0 o 1 para Dekker

		public OperadorTienda(int id, Tienda tienda, int procesoId) {
			this.id = id;
			this.tienda = tienda;
			this.hiloId = procesoId;
		}

		protected void entrarSeccionCritica() {
			flag[hiloId] = true; // el hilo i (actual) tiene la intencion de entrar a
														// la seccion critica

			int otro = 1 - hiloId; // hilo oponente que compite (si el hilo actual es
															// 1, el otro es 0 y viceversa)

			while (flag[otro]) { // si el otro hilo quiere entrar

				// se compite por la seccion critica

				if (turno != hiloId) { // si el turno no le toca al hilo actual entonces espera

					flag[hiloId] = false; // cede el paso hilo oponente

					while (turno != hiloId) // espera su turno
						Thread.yield(); // permite que el otro hilo se ejecute mientras no
														// sea su turno

					flag[hiloId] = true; // vuelve a intentar entrar, se repite el ciclo
				}
			}
		}

		protected void salirSeccionCritica() {
			turno = 1 - hiloId; // cuando el hilo en turno terminal cede el turno a su
													// oponente (1 a 0, 0 a 1)

			flag[hiloId] = false; // da la intencion de que ya no quiere entrar
		}
	}

	// cliente usando Dekker
	static class Cliente extends OperadorTienda {
		private final String client;

		public Cliente(String client, int id, Tienda tienda, int procesoId) {
			super(id, tienda, procesoId);
			this.client = client;
		}

		@Override
		public void run() {
			Random rand = new Random();
			Integer random = rand.nextInt(tienda.getSize()); // [0,getSize() )

			entrarSeccionCritica();
			try {
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
			} finally {
				salirSeccionCritica();
			}
		}
	}

	public static void main(String[] args) throws InterruptedException {
		Tienda inst = new Tienda();
		System.out.println(inst.toString()); // tienda al principio

		// creamos los hilos alternando entre proceso 0 y 1
		Thread[] hilos = new Thread[2];
		hilos[0] = new Thread(new Cliente("Pedro", 1, inst, 0));
		hilos[1] = new Thread(new Cliente("Luis", 2, inst, 1));

		// iniciamos los hilos
		for (Thread hilo : hilos)
			hilo.start();

		// esperamos a que terminen
		for (Thread hilo : hilos)
			hilo.join();

		System.out.println("\n" + inst.toString()); // tienda al final
	}
}
