import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.RemoteException;
import java.util.Scanner;
import java.util.Arrays;

/**
 * Cliente RMI que consume servicios de la calculadora remota
 * Demuestra Remote Procedure Calls desde el lado del cliente
 */
public class ClienteCalculadora {

    private CalculadoraRemota calculadora;
    private Scanner scanner;

    public ClienteCalculadora() {
        scanner = new Scanner(System.in);
    }

    public void conectar() {
        try {
            System.out.println("=== CLIENTE RMI CALCULADORA ===");
            System.out.println("Conectando al servidor RMI...");

            // Obtener el registro RMI
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);

            // Buscar el servicio remoto
            calculadora = (CalculadoraRemota) registry.lookup("CalculadoraServicio");

            System.out.println("¡Conectado exitosamente al servidor RMI!");

            // Obtener información del servidor
            String infoServidor = calculadora.obtenerInfoServidor();
            System.out.println("\n--- Información del Servidor ---");
            System.out.println(infoServidor);
            System.out.println("\n¡Listo para realizar operaciones remotas!\n");

        } catch (Exception e) {
            System.err.println("Error conectando al servidor RMI: " + e.getMessage());
            System.err.println("Asegúrate de que ServidorCalculadora esté ejecutándose");
            System.exit(1);
        }
    }

    public void mostrarMenu() {
        while (true) {
            System.out.println("\n=== MENU RPC CALCULADORA ===");
            System.out.println("1.  Operaciones básicas (+-*/)");
            System.out.println("2.  Operaciones avanzadas (potencia, raíz)");
            System.out.println("3.  Operaciones con vectores");
            System.out.println("4.  Gestionar resultados");
            System.out.println("5.  Información del servidor");
            System.out.println("6.  Prueba de rendimiento");
            System.out.println("7.  Salir");
            System.out.print("Opción: ");

            int opcion = leerEntero();

            try {
                switch (opcion) {
                    case 1:
                        menuOperacionesBasicas();
                        break;
                    case 2:
                        menuOperacionesAvanzadas();
                        break;
                    case 3:
                        menuOperacionesVectoriales();
                        break;
                    case 4:
                        menuGestionResultados();
                        break;
                    case 5:
                        mostrarInfoServidor();
                        break;
                    case 6:
                        pruebaRendimiento();
                        break;
                    case 7:
                        System.out.println("¡Hasta luego!");
                        return;
                    default:
                        System.out.println("Opción inválida");
                }
            } catch (RemoteException e) {
                System.err.println("Error RMI: " + e.getMessage());
            }
        }
    }

    private void menuOperacionesBasicas() throws RemoteException {
        System.out.println("\n--- OPERACIONES BÁSICAS ---");
        System.out.print("Primer número: ");
        double a = leerDouble();
        System.out.print("Segundo número: ");
        double b = leerDouble();

        System.out.println("\nResultados (RPC):");
        System.out.printf("%.2f + %.2f = %.2f%n", a, b, calculadora.sumar(a, b));
        System.out.printf("%.2f - %.2f = %.2f%n", a, b, calculadora.restar(a, b));
        System.out.printf("%.2f * %.2f = %.2f%n", a, b, calculadora.multiplicar(a, b));

        try {
            System.out.printf("%.2f / %.2f = %.2f%n", a, b, calculadora.dividir(a, b));
        } catch (RemoteException e) {
            System.out.println("Error en división: " + e.getMessage());
        }
    }

    private void menuOperacionesAvanzadas() throws RemoteException {
        System.out.println("\n--- OPERACIONES AVANZADAS ---");
        System.out.println("1. Potencia");
        System.out.println("2. Raíz cuadrada");
        System.out.print("Opción: ");

        int opcion = leerEntero();

        if (opcion == 1) {
            System.out.print("Base: ");
            double base = leerDouble();
            System.out.print("Exponente: ");
            double exp = leerDouble();

            double resultado = calculadora.potencia(base, exp);
            System.out.printf("%.2f ^ %.2f = %.2f%n", base, exp, resultado);

        } else if (opcion == 2) {
            System.out.print("Número: ");
            double numero = leerDouble();

            try {
                double resultado = calculadora.raizCuadrada(numero);
                System.out.printf("sqrt(%.2f) = %.2f%n", numero, resultado);
            } catch (RemoteException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }

    private void menuOperacionesVectoriales() throws RemoteException {
        System.out.println("\n--- OPERACIONES VECTORIALES ---");
        System.out.print("¿Cuántos números? ");
        int cantidad = leerEntero();

        double[] numeros = new double[cantidad];
        for (int i = 0; i < cantidad; i++) {
            System.out.printf("Número %d: ", i + 1);
            numeros[i] = leerDouble();
        }

        System.out.println("Array original: " + Arrays.toString(numeros));

        System.out.println("Operaciones disponibles: cuadrado, doble, negativo");
        System.out.print("Operación: ");
        String operacion = scanner.nextLine();

        try {
            double[] resultado = calculadora.operacionVector(numeros, operacion);
            System.out.println("Resultado: " + Arrays.toString(resultado));
        } catch (RemoteException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private void menuGestionResultados() throws RemoteException {
        System.out.println("\n--- GESTIÓN DE RESULTADOS ---");
        System.out.println("1. Guardar resultado");
        System.out.println("2. Recuperar resultado");
        System.out.println("3. Listar claves");
        System.out.print("Opción: ");

        int opcion = leerEntero();

        switch (opcion) {
            case 1:
                System.out.print("Clave: ");
                String clave = scanner.nextLine();
                System.out.print("Valor: ");
                double valor = leerDouble();

                try {
                    calculadora.guardarResultado(clave, valor);
                    System.out.println("¡Resultado guardado exitosamente!");
                } catch (RemoteException e) {
                    System.out.println("Error: " + e.getMessage());
                }
                break;

            case 2:
                System.out.print("Clave a buscar: ");
                String claveABuscar = scanner.nextLine();

                try {
                    double valorRecuperado = calculadora.obtenerResultado(claveABuscar);
                    System.out.printf("'%s' = %.2f%n", claveABuscar, valorRecuperado);
                } catch (RemoteException e) {
                    System.out.println("Error: " + e.getMessage());
                }
                break;

            case 3:
                String[] claves = calculadora.listarClaves();
                System.out.println("Claves disponibles:");
                for (String key : claves) {
                    try {
                        double val = calculadora.obtenerResultado(key);
                        System.out.printf("  '%s' = %.2f%n", key, val);
                    } catch (RemoteException e) {
                        System.out.printf("  '%s' = [error]%n", key);
                    }
                }
                break;
        }
    }

    private void mostrarInfoServidor() throws RemoteException {
        System.out.println("\n--- INFORMACIÓN DEL SERVIDOR ---");
        String info = calculadora.obtenerInfoServidor();
        System.out.println(info);

        long tiempoServidor = calculadora.obtenerTiempoServidor();
        long tiempoCliente = System.currentTimeMillis();
        long diferencia = Math.abs(tiempoCliente - tiempoServidor);

        System.out.println("\n--- SINCRONIZACIÓN ---");
        System.out.println("Tiempo servidor: " + tiempoServidor);
        System.out.println("Tiempo cliente:  " + tiempoCliente);
        System.out.println("Diferencia: " + diferencia + " ms");
    }

    private void pruebaRendimiento() throws RemoteException {
        System.out.println("\n--- PRUEBA DE RENDIMIENTO RMI ---");
        System.out.print("¿Cuántas operaciones realizar? ");
        int operaciones = leerEntero();

        System.out.println("Realizando " + operaciones + " sumas remotas...");

        long inicio = System.currentTimeMillis();

        for (int i = 0; i < operaciones; i++) {
            calculadora.sumar(i, i + 1);

            // Mostrar progreso cada 100 operaciones
            if (i > 0 && i % 100 == 0) {
                System.out.print(".");
            }
        }

        long fin = System.currentTimeMillis();
        long tiempoTotal = fin - inicio;

        System.out.println("\n\n--- RESULTADOS ---");
        System.out.println("Operaciones: " + operaciones);
        System.out.println("Tiempo total: " + tiempoTotal + " ms");
        System.out.println("Tiempo promedio por operación: " +
                (tiempoTotal / (double) operaciones) + " ms");
        System.out.println("Operaciones por segundo: " +
                (operaciones * 1000.0 / tiempoTotal));
    }

    private int leerEntero() {
        while (true) {
            try {
                String input = scanner.nextLine();
                return Integer.parseInt(input);
            } catch (NumberFormatException e) {
                System.out.print("Por favor ingresa un número entero válido: ");
            }
        }
    }

    private double leerDouble() {
        while (true) {
            try {
                String input = scanner.nextLine();
                return Double.parseDouble(input);
            } catch (NumberFormatException e) {
                System.out.print("Por favor ingresa un número válido: ");
            }
        }
    }

    public static void main(String[] args) {
        ClienteCalculadora cliente = new ClienteCalculadora();
        cliente.conectar();
        cliente.mostrarMenu();
    }
}