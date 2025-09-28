import java.io.*;
import java.net.*;
import java.util.Scanner;

/**
 * Cliente básico que se conecta al servidor y envía mensajes
 */
public class ClienteBasico {
    private static final String HOST = "localhost";
    private static final int PUERTO = 8080;
    
    public static void main(String[] args) {
        System.out.println("=== CLIENTE BÁSICO ===");
        System.out.println("Conectando a " + HOST + ":" + PUERTO);
        
        try (
            Socket socket = new Socket(HOST, PUERTO);
            BufferedReader entrada = new BufferedReader(
                new InputStreamReader(socket.getInputStream()));
            PrintWriter salida = new PrintWriter(
                socket.getOutputStream(), true);
            Scanner scanner = new Scanner(System.in)
        ) {
            System.out.println("Conectado al servidor!");
            
            // Leer mensaje de bienvenida del servidor
            String bienvenida = entrada.readLine();
            System.out.println("Servidor: " + bienvenida);
            
            String mensaje;
            while (true) {
                System.out.print("Tu mensaje (o 'salir'): ");
                mensaje = scanner.nextLine();
                
                // Enviar mensaje al servidor
                salida.println(mensaje);
                
                if ("salir".equalsIgnoreCase(mensaje.trim())) {
                    break;
                }
                
                // Leer respuesta del servidor
                String respuesta = entrada.readLine();
                if (respuesta != null) {
                    System.out.println("Servidor: " + respuesta);
                } else {
                    System.out.println("El servidor cerró la conexión");
                    break;
                }
            }
            
        } catch (ConnectException e) {
            System.err.println("No se pudo conectar al servidor. ¿Está ejecutándose?");
            System.err.println("Ejecuta primero: java ServidorBasico");
        } catch (IOException e) {
            System.err.println("Error de conexión: " + e.getMessage());
        }
        
        System.out.println("Cliente desconectado");
    }
}