import java.io.*;
import java.net.*;
import java.util.Scanner;

/**
 * Cliente de chat que se conecta al servidor y permite chatear con otros usuarios
 */
public class ClienteChat {
    private static final String HOST = "localhost";
    private static final int PUERTO = 8082;
    
    public static void main(String[] args) {
        System.out.println("=== CLIENTE DE CHAT ===");
        System.out.println("Conectando al chat en " + HOST + ":" + PUERTO);
        
        try (
            Socket socket = new Socket(HOST, PUERTO);
            BufferedReader entrada = new BufferedReader(
                new InputStreamReader(socket.getInputStream()));
            PrintWriter salida = new PrintWriter(
                socket.getOutputStream(), true);
            Scanner scanner = new Scanner(System.in)
        ) {
            System.out.println("Conectado al servidor de chat!");
            
            // Crear hilo para leer mensajes del servidor
            Thread lectorMensajes = new Thread(() -> {
                try {
                    String mensaje;
                    while ((mensaje = entrada.readLine()) != null) {
                        System.out.println(mensaje);
                    }
                } catch (IOException e) {
                    if (!socket.isClosed()) {
                        System.err.println("Error leyendo mensajes: " + e.getMessage());
                    }
                }
            });
            
            lectorMensajes.setDaemon(true);
            lectorMensajes.start();
            
            // Leer entrada del usuario y enviar al servidor
            String mensaje;
            while (true) {
                mensaje = scanner.nextLine();
                
                if ("/salir".equalsIgnoreCase(mensaje.trim())) {
                    salida.println("/salir");
                    break;
                }
                
                salida.println(mensaje);
            }
            
        } catch (ConnectException e) {
            System.err.println("No se pudo conectar al servidor de chat.");
            System.err.println("Ejecuta primero: java ServidorChat");
        } catch (IOException e) {
            System.err.println("Error de conexión: " + e.getMessage());
        }
        
        System.out.println("Desconectado del chat");
    }
}