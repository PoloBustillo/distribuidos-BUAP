package ejemplos;

/**
 * Demostración de la importancia de los hilos
 * Compara ejecución secuencial vs concurrente
 */
public class ImportanciaHilos {

    public static void main(String[] args) {
        System.out.println("=== IMPORTANCIA DE LOS HILOS ===");

        // Simulación de tareas que toman tiempo
        System.out.println("\n1. EJECUCIÓN SECUENCIAL:");
        long inicioSecuencial = System.currentTimeMillis();
        ejecutarTareaSecuencial("Tarea-A", 2000);
        ejecutarTareaSecuencial("Tarea-B", 2000);
        ejecutarTareaSecuencial("Tarea-C", 2000);
        long finSecuencial = System.currentTimeMillis();

        System.out.println("Tiempo total secuencial: " +
                (finSecuencial - inicioSecuencial) + " ms\n");

        // Ejecución concurrente
        System.out.println("2. EJECUCIÓN CONCURRENTE:");
        long inicioConcurrente = System.currentTimeMillis();

        Thread hiloA = new Thread(() -> ejecutarTareaSecuencial("Tarea-A", 2000));
        Thread hiloB = new Thread(() -> ejecutarTareaSecuencial("Tarea-B", 2000));
        Thread hiloC = new Thread(() -> ejecutarTareaSecuencial("Tarea-C", 2000));

        hiloA.start();
        hiloB.start();
        hiloC.start();

        try {
            hiloA.join();
            hiloB.join();
            hiloC.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        long finConcurrente = System.currentTimeMillis();
        System.out.println("Tiempo total concurrente: " +
                (finConcurrente - inicioConcurrente) + " ms");

        // Mostrar mejora en rendimiento
        double mejora = (double) (finSecuencial - inicioSecuencial) /
                (finConcurrente - inicioConcurrente);
        System.out.printf("\nMejora en rendimiento: %.2fx más rápido\n", mejora);

        // Demostrar responsividad
        System.out.println("\n3. RESPONSIVIDAD - Interfaz no bloqueante:");
        demostrarResponsividad();
    }

    private static void ejecutarTareaSecuencial(String nombre, int duracion) {
        System.out.println(nombre + " iniciada por " + Thread.currentThread().getName());
        try {
            Thread.sleep(duracion);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println(nombre + " completada");
    }

    private static void demostrarResponsividad() {
        // Simular una tarea larga en background
        Thread tareaLarga = new Thread(() -> {
            for (int i = 1; i <= 10; i++) {
                System.out.println("Procesando... " + (i * 10) + "% completado");
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
            System.out.println("Tarea larga completada!");
        });

        // Simular interfaz responsiva
        Thread interfaz = new Thread(() -> {
            for (int i = 0; i < 15; i++) {
                System.out.println("[UI] Interfaz respondiendo... tick " + i);
                try {
                    Thread.sleep(300);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        });

        tareaLarga.start();
        interfaz.start();

        try {
            tareaLarga.join();
            interfaz.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("La interfaz se mantuvo responsiva durante la tarea larga!");
    }
}