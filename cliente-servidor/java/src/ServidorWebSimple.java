import java.io.*;
import java.net.*;
import java.util.Date;

/**
 * Servidor Web Simple en Java
 * Demuestra un servidor HTTP básico que sirve páginas web simples
 */
public class ServidorWebSimple {
    private static final int PUERTO = 8080;

    public static void main(String[] args) {
        System.out.println("=== SERVIDOR WEB SIMPLE ===");
        System.out.println("Iniciando servidor en puerto " + PUERTO);

        try (ServerSocket servidor = new ServerSocket(PUERTO)) {
            System.out.println("Servidor iniciado en http://localhost:" + PUERTO);
            System.out.println("Presiona Ctrl+C para detener\n");

            while (true) {
                Socket cliente = servidor.accept();
                // Manejar cada cliente en un hilo separado
                new Thread(() -> manejarCliente(cliente)).start();
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
                        cliente.getOutputStream(), true)) {
            // Leer la petición HTTP
            String lineaPeticion = entrada.readLine();
            if (lineaPeticion == null)
                return;

            System.out.println("Petición recibida: " + lineaPeticion);

            // Extraer la ruta de la petición
            String[] partes = lineaPeticion.split(" ");
            String ruta = partes.length > 1 ? partes[1] : "/";

            // Consumir el resto de headers (obligatorio en HTTP)
            String linea;
            while ((linea = entrada.readLine()) != null && !linea.isEmpty()) {
                // Leer headers pero no hacer nada con ellos
            }

            // Generar respuesta según la ruta solicitada
            String contenido = generarContenido(ruta);

            // Enviar respuesta HTTP
            salida.println("HTTP/1.1 200 OK");
            salida.println("Content-Type: text/html; charset=UTF-8");
            salida.println("Content-Length: " + contenido.getBytes().length);
            salida.println("Connection: close");
            salida.println(); // Línea vacía separa headers del cuerpo
            salida.print(contenido);
            salida.flush();

        } catch (IOException e) {
            System.err.println("Error manejando cliente: " + e.getMessage());
        } finally {
            try {
                cliente.close();
            } catch (IOException e) {
                System.err.println("Error cerrando conexión: " + e.getMessage());
            }
        }
    }

    private static String generarContenido(String ruta) {
        Date ahora = new Date();

        if ("/".equals(ruta) || "/inicio".equals(ruta)) {
            return generarPaginaInicio(ahora);
        } else if ("/saludo".equals(ruta)) {
            return generarPaginaSaludo(ahora);
        } else if ("/info".equals(ruta)) {
            return generarPaginaInfo(ahora);
        } else {
            return generarPagina404(ruta, ahora);
        }
    }

    private static String generarPaginaInicio(Date fecha) {
        return "<!DOCTYPE html>" +
                "<html><head><title>Servidor Web Simple</title></head>" +
                "<body>" +
                "<h1>🌐 Bienvenido al Servidor Web Simple</h1>" +
                "<p><strong>Fecha y hora:</strong> " + fecha + "</p>" +
                "<p>Este es un servidor web básico escrito en Java.</p>" +
                "<h2>Páginas disponibles:</h2>" +
                "<ul>" +
                "<li><a href='/'>Inicio</a> (esta página)</li>" +
                "<li><a href='/saludo'>Saludo</a></li>" +
                "<li><a href='/info'>Información del servidor</a></li>" +
                "</ul>" +
                "<p><em>Creado con ❤️ en Java</em></p>" +
                "</body></html>";
    }

    private static String generarPaginaSaludo(Date fecha) {
        return "<!DOCTYPE html>" +
                "<html><head><title>Saludo - Servidor Simple</title></head>" +
                "<body>" +
                "<h1>👋 ¡Hola desde Java!</h1>" +
                "<p><strong>Hora actual:</strong> " + fecha + "</p>" +
                "<p>Este saludo es generado dinámicamente por el servidor.</p>" +
                "<p>Cada vez que recargas la página, la hora se actualiza.</p>" +
                "<p><a href='/'>← Volver al inicio</a></p>" +
                "</body></html>";
    }

    private static String generarPaginaInfo(Date fecha) {
        Runtime runtime = Runtime.getRuntime();
        long memoriaTotal = runtime.totalMemory() / 1024 / 1024; // MB
        long memoriaLibre = runtime.freeMemory() / 1024 / 1024; // MB
        int hilosActivos = Thread.activeCount();

        return "<!DOCTYPE html>" +
                "<html><head><title>Info - Servidor Simple</title></head>" +
                "<body>" +
                "<h1>ℹ️ Información del Servidor</h1>" +
                "<p><strong>Fecha y hora:</strong> " + fecha + "</p>" +
                "<p><strong>Puerto:</strong> " + PUERTO + "</p>" +
                "<p><strong>Versión de Java:</strong> " + System.getProperty("java.version") + "</p>" +
                "<p><strong>Sistema Operativo:</strong> " + System.getProperty("os.name") + "</p>" +
                "<p><strong>Memoria total:</strong> " + memoriaTotal + " MB</p>" +
                "<p><strong>Memoria libre:</strong> " + memoriaLibre + " MB</p>" +
                "<p><strong>Hilos activos:</strong> " + hilosActivos + "</p>" +
                "<p><a href='/'>← Volver al inicio</a></p>" +
                "</body></html>";
    }

    private static String generarPagina404(String ruta, Date fecha) {
        return "<!DOCTYPE html>" +
                "<html><head><title>404 - Página no encontrada</title></head>" +
                "<body>" +
                "<h1>❌ 404 - Página no encontrada</h1>" +
                "<p>La página <code>" + ruta + "</code> no existe en este servidor.</p>" +
                "<p><strong>Fecha:</strong> " + fecha + "</p>" +
                "<p><a href='/'>← Ir al inicio</a></p>" +
                "</body></html>";
    }
}