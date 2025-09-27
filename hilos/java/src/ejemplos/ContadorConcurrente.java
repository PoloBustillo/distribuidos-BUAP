package ejemplos;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Demostración de contador thread-safe usando diferentes técnicas
 * Compara synchronized, AtomicInteger y locks explícitos
 */
public class ContadorConcurrente {

    public static void main(String[] args) {
        System.out.println("=== CONTADORES THREAD-SAFE ===");

        // Comparar diferentes implementaciones
        System.out.println("\n1. CONTADOR SYNCHRONIZED:");
        probarContador(new ContadorSynchronized(), "Synchronized");

        System.out.println("\n2. CONTADOR ATOMIC:");
        probarContador(new ContadorAtomic(), "AtomicInteger");

        System.out.println("\n3. CONTADOR CON LOCK:");
        probarContador(new ContadorLock(), "ReentrantLock");

        System.out.println("\n4. CONTADOR VOLÁTIL (NO THREAD-SAFE):");
        probarContador(new ContadorVolatile(), "Volatile (inseguro)");

        // Demostrar rendimiento
        System.out.println("\n5. COMPARACIÓN DE RENDIMIENTO:");
        compararRendimiento();
    }

    private static void probarContador(Contador contador, String tipo) {
        final int NUM_HILOS = 5;
        final int INCREMENTOS_POR_HILO = 1000;

        Thread[] hilos = new Thread[NUM_HILOS];

        long inicio = System.currentTimeMillis();

        for (int i = 0; i < NUM_HILOS; i++) {
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < INCREMENTOS_POR_HILO; j++) {
                    contador.incrementar();
                }
            });
        }

        for (Thread hilo : hilos) {
            hilo.start();
        }

        for (Thread hilo : hilos) {
            try {
                hilo.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        long fin = System.currentTimeMillis();

        System.out.println("Tipo: " + tipo);
        System.out.println("Valor esperado: " + (NUM_HILOS * INCREMENTOS_POR_HILO));
        System.out.println("Valor obtenido: " + contador.getValor());
        System.out.println("¿Correcto? " + (contador.getValor() == NUM_HILOS * INCREMENTOS_POR_HILO));
        System.out.println("Tiempo: " + (fin - inicio) + "ms");
    }

    private static void compararRendimiento() {
        final int NUM_HILOS = 10;
        final int OPERACIONES = 100000;

        System.out.println("Realizando " + (NUM_HILOS * OPERACIONES) + " operaciones con " + NUM_HILOS + " hilos:");

        // Probar diferentes implementaciones
        long tiempoSync = medirTiempo(new ContadorSynchronized(), NUM_HILOS, OPERACIONES);
        long tiempoAtomic = medirTiempo(new ContadorAtomic(), NUM_HILOS, OPERACIONES);
        long tiempoLock = medirTiempo(new ContadorLock(), NUM_HILOS, OPERACIONES);

        System.out.println("\nResultados de rendimiento:");
        System.out.println("Synchronized: " + tiempoSync + "ms");
        System.out.println("AtomicInteger: " + tiempoAtomic + "ms");
        System.out.println("ReentrantLock: " + tiempoLock + "ms");

        System.out.println("\nRanking (más rápido primero):");
        if (tiempoAtomic <= tiempoSync && tiempoAtomic <= tiempoLock) {
            System.out.println("1. AtomicInteger (" + tiempoAtomic + "ms)");
            if (tiempoSync <= tiempoLock) {
                System.out.println("2. Synchronized (" + tiempoSync + "ms)");
                System.out.println("3. ReentrantLock (" + tiempoLock + "ms)");
            } else {
                System.out.println("2. ReentrantLock (" + tiempoLock + "ms)");
                System.out.println("3. Synchronized (" + tiempoSync + "ms)");
            }
        } else if (tiempoSync <= tiempoAtomic && tiempoSync <= tiempoLock) {
            System.out.println("1. Synchronized (" + tiempoSync + "ms)");
            if (tiempoAtomic <= tiempoLock) {
                System.out.println("2. AtomicInteger (" + tiempoAtomic + "ms)");
                System.out.println("3. ReentrantLock (" + tiempoLock + "ms)");
            } else {
                System.out.println("2. ReentrantLock (" + tiempoLock + "ms)");
                System.out.println("3. AtomicInteger (" + tiempoAtomic + "ms)");
            }
        } else {
            System.out.println("1. ReentrantLock (" + tiempoLock + "ms)");
            if (tiempoSync <= tiempoAtomic) {
                System.out.println("2. Synchronized (" + tiempoSync + "ms)");
                System.out.println("3. AtomicInteger (" + tiempoAtomic + "ms)");
            } else {
                System.out.println("2. AtomicInteger (" + tiempoAtomic + "ms)");
                System.out.println("3. Synchronized (" + tiempoSync + "ms)");
            }
        }
    }

    private static long medirTiempo(Contador contador, int numHilos, int operaciones) {
        Thread[] hilos = new Thread[numHilos];

        long inicio = System.currentTimeMillis();

        for (int i = 0; i < numHilos; i++) {
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < operaciones; j++) {
                    contador.incrementar();
                }
            });
        }

        for (Thread hilo : hilos) {
            hilo.start();
        }

        for (Thread hilo : hilos) {
            try {
                hilo.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        return System.currentTimeMillis() - inicio;
    }
}

// Interfaz común para todos los contadores
interface Contador {
    void incrementar();

    int getValor();
}

// Implementación con synchronized
class ContadorSynchronized implements Contador {
    private int valor = 0;

    @Override
    public synchronized void incrementar() {
        valor++;
    }

    @Override
    public synchronized int getValor() {
        return valor;
    }
}

// Implementación con AtomicInteger
class ContadorAtomic implements Contador {
    private final AtomicInteger valor = new AtomicInteger(0);

    @Override
    public void incrementar() {
        valor.incrementAndGet();
    }

    @Override
    public int getValor() {
        return valor.get();
    }
}

// Implementación con ReentrantLock
class ContadorLock implements Contador {
    private int valor = 0;
    private final ReentrantLock lock = new ReentrantLock();

    @Override
    public void incrementar() {
        lock.lock();
        try {
            valor++;
        } finally {
            lock.unlock();
        }
    }

    @Override
    public int getValor() {
        lock.lock();
        try {
            return valor;
        } finally {
            lock.unlock();
        }
    }
}

// Implementación con volatile (NO thread-safe para incremento)
class ContadorVolatile implements Contador {
    private volatile int valor = 0;

    @Override
    public void incrementar() {
        valor++; // Esta operación NO es atómica!
    }

    @Override
    public int getValor() {
        return valor;
    }
}