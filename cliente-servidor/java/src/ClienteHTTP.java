import java.io.*;
import java.net.*;
import java.util.Scanner;

/**
 * Cliente HTTP que realiza peticiones GET/POST a servidores web
 * Demuestra el patrón Cliente-Servidor en HTTP
 */
public class ClienteHTTP {

    public static void main(String[] args) {
        System.out.println("=== CLIENTE HTTP ===");
        try (Scanner scanner = new Scanner(System.in)) {

            while (true) {
                System.out.println("\n1. GET a servidor local");
                System.out.println("2. GET a API externa");
                System.out.println("3. POST datos");
                System.out.println("4. Salir");
                System.out.print("Opción: ");

                int opcion = scanner.nextInt();
                scanner.nextLine(); // Consumir newline

                switch (opcion) {
                    case 1:
                        hacerGETLocal();
                        break;
                    case 2:
                        hacerGETExterno();
                        break;
                    case 3:
                        hacerPOST();
                        break;
                    case 4:
                        System.out.println("¡Adiós!");
                        return;
                    default:
                        System.out.println("Opción inválida");
                }
            }
        }
    }

    private static void hacerGETLocal() {
        try {
            System.out.println("\n--- GET a servidor local ---");
            String respuesta = enviarGET("http://localhost:8080/api/usuarios");
            System.out.println("Respuesta del servidor:");
            System.out.println(respuesta);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            System.err.println("Asegúrate de que ServidorAplicacion esté ejecutándose");
        }
    }

    private static void hacerGETExterno() {
        try {
            System.out.println("\n--- GET a API externa ---");
            String respuesta = enviarGET("https://jsonplaceholder.typicode.com/posts/1");
            System.out.println("Respuesta de la API:");
            System.out.println(respuesta);
        } catch (Exception e) {
            System.err.println("Error conectando a API externa: " + e.getMessage());
        }
    }

    private static void hacerPOST() {
        try {
            System.out.println("\n--- POST datos ---");
            String jsonData = "{\"nombre\":\"Juan\",\"email\":\"juan@example.com\"}";
            String respuesta = enviarPOST("http://localhost:8080/api/usuarios", jsonData);
            System.out.println("Respuesta del servidor:");
            System.out.println(respuesta);
        } catch (Exception e) {
            System.err.println("Error en POST: " + e.getMessage());
        }
    }

    private static String enviarGET(String urlString) throws IOException {
        URL url = new URL(urlString);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        // Configurar la petición GET
        connection.setRequestMethod("GET");
        connection.setRequestProperty("User-Agent", "ClienteHTTP/1.0");
        connection.setRequestProperty("Accept", "application/json");
        connection.setConnectTimeout(5000); // 5 segundos timeout
        connection.setReadTimeout(5000);

        // Leer la respuesta
        int responseCode = connection.getResponseCode();
        System.out.println("Código de respuesta: " + responseCode);

        BufferedReader reader;
        if (responseCode >= 200 && responseCode < 300) {
            reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        } else {
            reader = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
        }

        StringBuilder response = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            response.append(line).append("\n");
        }
        reader.close();

        return response.toString();
    }

    private static String enviarPOST(String urlString, String jsonData) throws IOException {
        URL url = new URL(urlString);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        // Configurar la petición POST
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setRequestProperty("Accept", "application/json");
        connection.setDoOutput(true);
        connection.setConnectTimeout(5000);
        connection.setReadTimeout(5000);

        // Enviar datos JSON
        try (DataOutputStream out = new DataOutputStream(connection.getOutputStream())) {
            out.writeBytes(jsonData);
            out.flush();
        }

        // Leer respuesta
        int responseCode = connection.getResponseCode();
        System.out.println("Código de respuesta: " + responseCode);

        BufferedReader reader;
        if (responseCode >= 200 && responseCode < 300) {
            reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        } else {
            reader = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
        }

        StringBuilder response = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            response.append(line).append("\n");
        }
        reader.close();

        return response.toString();
    }
}