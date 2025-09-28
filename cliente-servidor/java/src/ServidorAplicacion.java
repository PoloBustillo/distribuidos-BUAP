import java.io.*;
import java.net.*;
import java.util.Date;

/**
 * Servidor de Aplicación Simple en Java
 * Demuestra un servidor HTTP básico con respuestas JSON
 */
public class ServidorAplicacion {
    private static final int PUERTO = 8080;

    public static void main(String[] args) {
        System.out.println("=== SERVIDOR DE APLICACIÓN SIMPLE ===");
        System.out.println("Iniciando servidor en puerto " + PUERTO);

        try (ServerSocket servidor = new ServerSocket(PUERTO)) {
            System.out.println("Servidor iniciado en http://localhost:" + PUERTO);
            System.out.println("Endpoints disponibles:");
            System.out.println("  GET  /api/saludo    - Saludo simple");
            System.out.println("  GET  /api/fecha     - Fecha actual");
            System.out.println("  GET  /api/usuarios  - Lista de usuarios");
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

            System.out.println("Petición: " + lineaPeticion);

            // Extraer método y ruta
            String[] partes = lineaPeticion.split(" ");
            String metodo = partes.length > 0 ? partes[0] : "GET";
            String ruta = partes.length > 1 ? partes[1] : "/";

            // Consumir headers (obligatorio en HTTP)
            String linea;
            while ((linea = entrada.readLine()) != null && !linea.isEmpty()) {
                // Leer headers pero no procesarlos en este ejemplo simple
            }

            // Procesar la petición
            if ("GET".equals(metodo)) {
                procesarGET(salida, ruta);
            } else {
                enviarError(salida, 405, "Método no permitido");
            }

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

    private static void procesarGET(PrintWriter salida, String ruta) {
        String respuesta;

        switch (ruta) {
            case "/api/saludo":
                respuesta = "{\"mensaje\": \"¡Hola desde el servidor!\", \"timestamp\": \"" + new Date() + "\"}";
                break;

            case "/api/fecha":
                respuesta = "{\"fecha\": \"" + new Date() + "\", \"servidor\": \"Java Simple\"}";
                break;

            case "/api/usuarios":
                respuesta = "[\n" +
                        "  {\"id\": 1, \"nombre\": \"Ana García\", \"email\": \"ana@example.com\"},\n" +
                        "  {\"id\": 2, \"nombre\": \"Carlos López\", \"email\": \"carlos@example.com\"},\n" +
                        "  {\"id\": 3, \"nombre\": \"María Rodríguez\", \"email\": \"maria@example.com\"}\n" +
                        "]";
                break;

            case "/":
                respuesta = "{\"mensaje\": \"Servidor funcionando\", \"endpoints\": [\"/api/saludo\", \"/api/fecha\", \"/api/usuarios\"]}";
                break;

            default:
                enviarError(salida, 404, "Endpoint no encontrado");
                return;
        }

        enviarRespuestaJSON(salida, respuesta);
    }

    private static void enviarRespuestaJSON(PrintWriter salida, String json) {
        salida.println("HTTP/1.1 200 OK");
        salida.println("Content-Type: application/json; charset=UTF-8");
        salida.println("Content-Length: " + json.getBytes().length);
        salida.println("Access-Control-Allow-Origin: *");
        salida.println("Connection: close");
        salida.println(); // Línea vacía separa headers del cuerpo
        salida.print(json);
        salida.flush();
    }

    private static void enviarError(PrintWriter salida, int codigo, String mensaje) {
        String errorJson = "{\"error\": " + codigo + ", \"mensaje\": \"" + mensaje + "\"}";

        String estadoHTTP = codigo == 404 ? "404 Not Found"
                : codigo == 405 ? "405 Method Not Allowed" : codigo + " Error";

        salida.println("HTTP/1.1 " + estadoHTTP);
        salida.println("Content-Type: application/json; charset=UTF-8");
        salida.println("Content-Length: " + errorJson.getBytes().length);
        salida.println("Connection: close");
        salida.println();
        salida.print(errorJson);
        salida.flush();
    }
}