import java.rmi.Remote;
import java.rmi.RemoteException;

/**
 * Interfaz remota para servicios de calculadora
 * Define los métodos que pueden ser invocados remotamente
 */
public interface CalculadoraRemota extends Remote {

    // Operaciones básicas
    double sumar(double a, double b) throws RemoteException;

    double restar(double a, double b) throws RemoteException;

    double multiplicar(double a, double b) throws RemoteException;

    double dividir(double a, double b) throws RemoteException;

    // Operaciones avanzadas
    double potencia(double base, double exponente) throws RemoteException;

    double raizCuadrada(double numero) throws RemoteException;

    // Operaciones con arrays
    double[] operacionVector(double[] numeros, String operacion) throws RemoteException;

    // Información del servidor
    String obtenerInfoServidor() throws RemoteException;

    long obtenerTiempoServidor() throws RemoteException;

    // Operaciones de estado
    void guardarResultado(String clave, double valor) throws RemoteException;

    double obtenerResultado(String clave) throws RemoteException;

    String[] listarClaves() throws RemoteException;
}