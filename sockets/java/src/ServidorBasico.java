import java.io.*;
import java.net.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Servidor básico mono-hilo que maneja un cliente a la vez
 */
public class ServidorBasico {
    private static final int PUERTO = 8080;
    
    public static void main(String[] args) {
        System.out.println("=== SERVIDOR BÁSICO MONO-HILO ===");
        System.out.println("Iniciando servidor en puerto " + PUERTO);
        
        try (ServerSocket servidor = new ServerSocket(PUERTO)) {
            System.out.println("Servidor iniciado. Esperando conexiones...");
            
            while (true) {
                // Acepta una conexión (BLOQUEA hasta que llegue un cliente)
                Socket cliente = servidor.accept();
                System.out.println("Cliente conectado desde: " + cliente.getInetAddress());
                
                // Maneja el cliente (UN SOLO CLIENTE A LA VEZ)
                manejarCliente(cliente);
            }
            
        } catch (IOException e) {
            System.err.println("Error del servidor: " + e.getMessage());
        }
    }
    
    private static void manejarCliente(Socket cliente) {
        try (
            BufferedReader entrada = new BufferedReader(
                new InputStreamReader(cliente.getInputStream()));
            PrintWriter salida = new PrintWriter(
                cliente.getOutputStream(), true)
        ) {
            String mensaje;
            salida.println("Conectado al servidor. Escribe 'salir' para desconectar.");
            
            while ((mensaje = entrada.readLine()) != null) {
                String timestamp = LocalDateTime.now().format(
                    DateTimeFormatter.ofPattern("HH:mm:ss"));
                
                System.out.println("[" + timestamp + "] Cliente: " + mensaje);
                
                if ("salir".equalsIgnoreCase(mensaje.trim())) {
                    salida.println("Desconectando...");
                    break;
                }
                
                // Echo del mensaje con timestamp
                String respuesta = "[" + timestamp + "] Servidor recibió: " + mensaje;
                salida.println(respuesta);
            }
            
        } catch (IOException e) {
            System.err.println("Error manejando cliente: " + e.getMessage());
        } finally {
            try {
                cliente.close();
                System.out.println("Cliente desconectado");
            } catch (IOException e) {
                System.err.println("Error cerrando conexión: " + e.getMessage());
            }
        }
    }
}