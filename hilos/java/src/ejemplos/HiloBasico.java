package ejemplos;

/**
 * Ejemplo básico de creación y uso de hilos en Java
 */
public class HiloBasico {

    public static void main(String[] args) {
        System.out.println("=== EJEMPLO BÁSICO DE HILOS ===");
        System.out.println("Hilo principal: " + Thread.currentThread().getName());

        // Método 1: Extendiendo Thread
        MiHilo hilo1 = new MiHilo("Hilo-1");
        hilo1.start();

        // Método 2: Implementando Runnable
        Thread hilo2 = new Thread(new MiTarea("Hilo-2"));
        hilo2.start();

        // Método 3: Usando lambda expression (Java 8+)
        Thread hilo3 = new Thread(() -> {
            for (int i = 1; i <= 5; i++) {
                System.out.println("Hilo-Lambda ejecutando: " + i);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            System.out.println("Hilo-Lambda ha terminado.");
        });
        hilo3.start();

        // Esperar a que todos los hilos terminen
        try {
            hilo1.join();
            hilo2.join();
            hilo3.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("Todos los hilos han terminado.");
    }
}

/**
 * Clase que extiende Thread
 */
class MiHilo extends Thread {
    private String nombre;

    public MiHilo(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println(nombre + " ejecutando: " + i);
            try {
                Thread.sleep(1000); // Simular trabajo
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        System.out.println(nombre + " ha terminado.");
    }
}

/**
 * Clase que implementa Runnable
 */
class MiTarea implements Runnable {
    private String nombre;

    public MiTarea(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println(nombre + " ejecutando: " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        System.out.println(nombre + " ha terminado.");
    }
}