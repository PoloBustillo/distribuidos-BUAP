package ejemplos;

/**
 * Demostración de problemas comunes de concurrencia
 * Race conditions, datos inconsistentes, etc.
 */
public class ProblemasConcurrencia {
    private static int saldo = 1000;

    public static void main(String[] args) {
        System.out.println("=== PROBLEMAS DE CONCURRENCIA ===");

        System.out.println("\n1. INCONSISTENCIA - Operaciones bancarias:");
        demostrarInconsistenciaBancaria();

        System.out.println("\n2. LECTURAS INCONSISTENTES:");
        demostrarLecturasInconsistentes();
    }

    private static void demostrarInconsistenciaBancaria() {
        saldo = 1000;

        // Crear múltiples hilos que realizan transacciones
        Thread depositador = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                realizarDeposito(50);
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        Thread retirador = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                realizarRetiro(30);
                try {
                    Thread.sleep(15);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        System.out.println("Saldo inicial: $" + saldo);

        depositador.start();
        retirador.start();

        try {
            depositador.join();
            retirador.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("Saldo final: $" + saldo);
        System.out.println("Saldo esperado: $" + (1000 + 10 * 50 - 10 * 30));
    }

    private static void realizarDeposito(int cantidad) {
        int saldoActual = saldo;
        // Simular procesamiento
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        saldo = saldoActual + cantidad;
        System.out.println("Depósito $" + cantidad + ", nuevo saldo: $" + saldo);
    }

    private static void realizarRetiro(int cantidad) {
        int saldoActual = saldo;
        if (saldoActual >= cantidad) {
            // Simular procesamiento
            try {
                Thread.sleep(1);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            saldo = saldoActual - cantidad;
            System.out.println("Retiro $" + cantidad + ", nuevo saldo: $" + saldo);
        }
    }

    private static void demostrarLecturasInconsistentes() {
        DatosCompartidos datos = new DatosCompartidos();

        // Hilo que modifica los datos
        Thread escritor = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                datos.actualizar(i, i * 10);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        // Hilo que lee los datos
        Thread lector = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                datos.leer();
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        escritor.start();
        lector.start();

        try {
            escritor.join();
            lector.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

class DatosCompartidos {
    private int x = 0;
    private int y = 0;

    public void actualizar(int nuevoX, int nuevoY) {
        System.out.println("[Escritor] Actualizando x=" + nuevoX + ", y=" + nuevoY);
        this.x = nuevoX;
        // Simular retraso entre actualizaciones
        try {
            Thread.sleep(10);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        this.y = nuevoY;
    }

    public void leer() {
        int valorX = this.x;
        int valorY = this.y;
        System.out.println("[Lector] x=" + valorX + ", y=" + valorY +
                " (consistente: " + (valorY == valorX * 10) + ")");
    }
}