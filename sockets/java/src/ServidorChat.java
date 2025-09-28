import java.io.*;
import java.net.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Servidor de chat que permite comunicación entre múltiples usuarios
 */
public class ServidorChat {
    private static final int PUERTO = 8082;
    private static final AtomicInteger contadorClientes = new AtomicInteger(0);
    private static final Map<String, PrintWriter> clientes = new ConcurrentHashMap<>();
    
    public static void main(String[] args) {
        System.out.println("=== SERVIDOR DE CHAT MULTI-USUARIO ===");
        System.out.println("Iniciando servidor de chat en puerto " + PUERTO);
        
        try (ServerSocket servidor = new ServerSocket(PUERTO)) {
            System.out.println("Servidor de chat iniciado. Esperando usuarios...");
            
            while (true) {
                Socket cliente = servidor.accept();
                int numeroCliente = contadorClientes.incrementAndGet();
                
                System.out.println("Nuevo usuario conectado desde: " + 
                    cliente.getInetAddress());
                
                Thread hiloCliente = new Thread(
                    new ManejadorUsuario(cliente, numeroCliente));
                hiloCliente.start();
            }
            
        } catch (IOException e) {
            System.err.println("Error del servidor de chat: " + e.getMessage());
        }
    }
    
    /**
     * Difunde un mensaje a todos los usuarios conectados
     */
    public static synchronized void difundirMensaje(String mensaje, String remitente) {
        String timestamp = LocalDateTime.now().format(
            DateTimeFormatter.ofPattern("HH:mm:ss"));
        String mensajeCompleto = "[" + timestamp + "] " + mensaje;
        
        System.out.println("Difundiendo: " + mensajeCompleto);
        
        // Crear una copia para evitar ConcurrentModificationException
        Map<String, PrintWriter> clientesCopia = new HashMap<>(clientes);
        
        for (Map.Entry<String, PrintWriter> entry : clientesCopia.entrySet()) {
            if (!entry.getKey().equals(remitente)) {
                try {
                    entry.getValue().println(mensajeCompleto);
                } catch (Exception e) {
                    System.err.println("Error enviando mensaje a " + entry.getKey());
                    clientes.remove(entry.getKey());
                }
            }
        }
    }
    
    /**
     * Clase que maneja un usuario del chat
     */
    static class ManejadorUsuario implements Runnable {
        private final Socket socket;
        private final int numeroUsuario;
        private String nombreUsuario;
        
        public ManejadorUsuario(Socket socket, int numeroUsuario) {
            this.socket = socket;
            this.numeroUsuario = numeroUsuario;
        }
        
        @Override
        public void run() {
            try (
                BufferedReader entrada = new BufferedReader(
                    new InputStreamReader(socket.getInputStream()));
                PrintWriter salida = new PrintWriter(
                    socket.getOutputStream(), true)
            ) {
                // Solicitar nombre de usuario
                salida.println("Bienvenido al chat! ¿Cuál es tu nombre?");
                nombreUsuario = entrada.readLine();
                
                if (nombreUsuario == null || nombreUsuario.trim().isEmpty()) {
                    nombreUsuario = "Usuario" + numeroUsuario;
                }
                
                // Registrar usuario
                clientes.put(nombreUsuario, salida);
                difundirMensaje(nombreUsuario + " se unió al chat", nombreUsuario);
                
                salida.println("Conectado como: " + nombreUsuario);
                salida.println("Usuarios conectados: " + clientes.size());
                salida.println("Escribe '/salir' para desconectar o '/usuarios' para ver usuarios");
                
                String mensaje;
                while ((mensaje = entrada.readLine()) != null) {
                    if ("/salir".equalsIgnoreCase(mensaje.trim())) {
                        break;
                    } else if ("/usuarios".equalsIgnoreCase(mensaje.trim())) {
                        salida.println("Usuarios conectados: " + 
                            String.join(", ", clientes.keySet()));
                    } else {
                        difundirMensaje(nombreUsuario + ": " + mensaje, nombreUsuario);
                    }
                }
                
            } catch (IOException e) {
                System.err.println("Error con usuario " + nombreUsuario + ": " + e.getMessage());
            } finally {
                // Desconectar usuario
                if (nombreUsuario != null) {
                    clientes.remove(nombreUsuario);
                    difundirMensaje(nombreUsuario + " salió del chat", nombreUsuario);
                    System.out.println("Usuario " + nombreUsuario + " desconectado");
                }
                
                try {
                    socket.close();
                } catch (IOException e) {
                    System.err.println("Error cerrando socket: " + e.getMessage());
                }
            }
        }
    }
}