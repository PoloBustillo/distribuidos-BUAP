import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;
import java.util.Set;

/**
 * Servidor RMI que implementa la interfaz CalculadoraRemota
 * Demuestra Remote Procedure Calls con Java RMI
 */
public class ServidorCalculadora implements CalculadoraRemota {

    // Almacenamiento de resultados (estado del servidor)
    private final Map<String, Double> resultados = new ConcurrentHashMap<>();
    private final String nombreServidor;
    private final LocalDateTime tiempoInicio;
    private int contadorOperaciones = 0;

    public ServidorCalculadora() {
        this.nombreServidor = "CalculadoraRMI-" + System.currentTimeMillis();
        this.tiempoInicio = LocalDateTime.now();

        // Agregar algunos resultados de ejemplo
        resultados.put("PI", Math.PI);
        resultados.put("E", Math.E);
        System.out.println("Servidor de calculadora inicializado: " + nombreServidor);
    }

    @Override
    public double sumar(double a, double b) throws RemoteException {
        contadorOperaciones++;
        double resultado = a + b;
        System.out.println(String.format("[%s] SUMA: %.2f + %.2f = %.2f",
                obtenerTimestamp(), a, b, resultado));
        return resultado;
    }

    @Override
    public double restar(double a, double b) throws RemoteException {
        contadorOperaciones++;
        double resultado = a - b;
        System.out.println(String.format("[%s] RESTA: %.2f - %.2f = %.2f",
                obtenerTimestamp(), a, b, resultado));
        return resultado;
    }

    @Override
    public double multiplicar(double a, double b) throws RemoteException {
        contadorOperaciones++;
        double resultado = a * b;
        System.out.println(String.format("[%s] MULTIPLICACIÓN: %.2f * %.2f = %.2f",
                obtenerTimestamp(), a, b, resultado));
        return resultado;
    }

    @Override
    public double dividir(double a, double b) throws RemoteException {
        contadorOperaciones++;
        if (b == 0) {
            throw new RemoteException("Error: División por cero no permitida");
        }
        double resultado = a / b;
        System.out.println(String.format("[%s] DIVISIÓN: %.2f / %.2f = %.2f",
                obtenerTimestamp(), a, b, resultado));
        return resultado;
    }

    @Override
    public double potencia(double base, double exponente) throws RemoteException {
        contadorOperaciones++;
        double resultado = Math.pow(base, exponente);
        System.out.println(String.format("[%s] POTENCIA: %.2f ^ %.2f = %.2f",
                obtenerTimestamp(), base, exponente, resultado));
        return resultado;
    }

    @Override
    public double raizCuadrada(double numero) throws RemoteException {
        contadorOperaciones++;
        if (numero < 0) {
            throw new RemoteException("Error: Raíz cuadrada de número negativo");
        }
        double resultado = Math.sqrt(numero);
        System.out.println(String.format("[%s] RAÍZ: sqrt(%.2f) = %.2f",
                obtenerTimestamp(), numero, resultado));
        return resultado;
    }

    @Override
    public double[] operacionVector(double[] numeros, String operacion) throws RemoteException {
        contadorOperaciones++;
        if (numeros == null || numeros.length == 0) {
            throw new RemoteException("Error: Array vacío o nulo");
        }

        double[] resultado = new double[numeros.length];

        switch (operacion.toLowerCase()) {
            case "cuadrado":
                for (int i = 0; i < numeros.length; i++) {
                    resultado[i] = numeros[i] * numeros[i];
                }
                break;
            case "doble":
                for (int i = 0; i < numeros.length; i++) {
                    resultado[i] = numeros[i] * 2;
                }
                break;
            case "negativo":
                for (int i = 0; i < numeros.length; i++) {
                    resultado[i] = -numeros[i];
                }
                break;
            default:
                throw new RemoteException("Operación no soportada: " + operacion);
        }

        System.out.println(String.format("[%s] VECTOR %s: %d elementos procesados",
                obtenerTimestamp(), operacion.toUpperCase(), numeros.length));
        return resultado;
    }

    @Override
    public String obtenerInfoServidor() throws RemoteException {
        String info = String.format(
                "Servidor: %s\nIniciado: %s\nOperaciones realizadas: %d\nResultados almacenados: %d",
                nombreServidor,
                tiempoInicio.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")),
                contadorOperaciones,
                resultados.size());
        System.out.println("[" + obtenerTimestamp() + "] Información del servidor solicitada");
        return info;
    }

    @Override
    public long obtenerTiempoServidor() throws RemoteException {
        return System.currentTimeMillis();
    }

    @Override
    public void guardarResultado(String clave, double valor) throws RemoteException {
        if (clave == null || clave.trim().isEmpty()) {
            throw new RemoteException("Error: Clave no puede estar vacía");
        }
        resultados.put(clave.trim(), valor);
        System.out.println(String.format("[%s] GUARDADO: '%s' = %.2f",
                obtenerTimestamp(), clave, valor));
    }

    @Override
    public double obtenerResultado(String clave) throws RemoteException {
        if (clave == null || clave.trim().isEmpty()) {
            throw new RemoteException("Error: Clave no puede estar vacía");
        }

        Double valor = resultados.get(clave.trim());
        if (valor == null) {
            throw new RemoteException("Error: Clave '" + clave + "' no encontrada");
        }

        System.out.println(String.format("[%s] RECUPERADO: '%s' = %.2f",
                obtenerTimestamp(), clave, valor));
        return valor;
    }

    @Override
    public String[] listarClaves() throws RemoteException {
        Set<String> claves = resultados.keySet();
        String[] array = claves.toArray(new String[0]);
        System.out.println(String.format("[%s] LISTADO: %d claves disponibles",
                obtenerTimestamp(), array.length));
        return array;
    }

    private String obtenerTimestamp() {
        return LocalDateTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
    }

    public static void main(String[] args) {
        try {
            System.out.println("=== SERVIDOR RMI CALCULADORA ===");

            // Crear la instancia del servidor
            ServidorCalculadora servidor = new ServidorCalculadora();

            // Exportar el objeto remoto
            CalculadoraRemota stub = (CalculadoraRemota) UnicastRemoteObject.exportObject(servidor, 0);

            // Crear el registro RMI en el puerto 1099
            Registry registry;
            try {
                registry = LocateRegistry.createRegistry(1099);
                System.out.println("Registro RMI creado en puerto 1099");
            } catch (RemoteException e) {
                // Si el registro ya existe, obténelo
                registry = LocateRegistry.getRegistry(1099);
                System.out.println("Usando registro RMI existente en puerto 1099");
            }

            // Registrar el objeto remoto
            registry.bind("CalculadoraServicio", stub);

            System.out.println("Servidor RMI listo y esperando peticiones...");
            System.out.println("Servicio registrado como: 'CalculadoraServicio'");
            System.out.println("Los clientes pueden conectarse con:");
            System.out.println("  rmi://localhost:1099/CalculadoraServicio");
            System.out.println("\nPresiona Ctrl+C para detener el servidor\n");

            // Mantener el servidor corriendo
            Thread.currentThread().join();

        } catch (Exception e) {
            System.err.println("Error del servidor RMI: " + e.getMessage());
            e.printStackTrace();
        }
    }
}