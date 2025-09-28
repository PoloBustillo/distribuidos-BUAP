#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor TCP concurrente que maneja múltiples clientes simultáneamente
Cada cliente se maneja en un hilo separado
"""

import socket
import threading
import datetime
import time

HOST = 'localhost'
PUERTO = 8081
clientes_activos = 0
lock = threading.Lock()

def main():
    print("=== SERVIDOR CONCURRENTE ===")
    print(f"Iniciando servidor en {HOST}:{PUERTO}")
    print("Este servidor puede manejar múltiples clientes simultáneamente")
    
    # Crear socket del servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Permitir reutilizar la dirección
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen(10)
        
        print("Servidor iniciado. Esperando conexiones...")
        
        while True:
            # Aceptar conexión del cliente
            cliente_socket, direccion_cliente = servidor.accept()
            
            # Crear hilo para manejar este cliente
            hilo_cliente = threading.Thread(
                target=manejar_cliente,
                args=(cliente_socket, direccion_cliente)
            )
            hilo_cliente.daemon = True  # El hilo terminará cuando termine el programa principal
            hilo_cliente.start()
            
    except KeyboardInterrupt:
        print("\nServidor interrumpido por el usuario")
    except Exception as e:
        print(f"Error del servidor: {e}")
    finally:
        servidor.close()
        print("Servidor cerrado")

def manejar_cliente(cliente_socket, direccion_cliente):
    """
    Maneja la comunicación con un cliente específico en un hilo separado
    """
    global clientes_activos
    
    # Incrementar contador de clientes (thread-safe)
    with lock:
        clientes_activos += 1
        numero_cliente = clientes_activos
    
    print(f"Cliente {numero_cliente} conectado desde {direccion_cliente}")
    print(f"Clientes activos: {threading.active_count() - 1}")  # -1 por el hilo principal
    
    try:
        # Enviar mensaje de bienvenida
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bienvenida = (
            f"¡Bienvenido cliente {numero_cliente}!\n"
            f"Hora de conexión: {timestamp}\n"
            f"Hilo actual: {threading.current_thread().name}\n"
            f"Clientes concurrentes: {threading.active_count() - 1}\n"
        )
        cliente_socket.send(bienvenida.encode('utf-8'))
        
        # Leer datos del cliente
        while True:
            datos = cliente_socket.recv(1024)
            if not datos:
                break
                
            mensaje_recibido = datos.decode('utf-8').strip()
            print(f"Cliente {numero_cliente}: {mensaje_recibido}")
            
            # Procesar comandos especiales
            if mensaje_recibido.lower() == "adios":
                respuesta = "¡Hasta luego!\n"
                cliente_socket.send(respuesta.encode('utf-8'))
                break
            elif mensaje_recibido.lower() == "estado":
                respuesta = (
                    f"Estado del servidor:\n"
                    f"- Hilos activos: {threading.active_count()}\n"
                    f"- Tu cliente número: {numero_cliente}\n"
                    f"- Tu hilo: {threading.current_thread().name}\n"
                )
                cliente_socket.send(respuesta.encode('utf-8'))
            elif mensaje_recibido.lower() == "esperar":
                respuesta = "Simulando trabajo pesado... esperando 3 segundos\n"
                cliente_socket.send(respuesta.encode('utf-8'))
                time.sleep(3)  # Simular trabajo pesado
                respuesta = "¡Trabajo completado!\n"
                cliente_socket.send(respuesta.encode('utf-8'))
            else:
                # Echo con información del hilo
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                respuesta = (
                    f"[{timestamp}] Procesado por {threading.current_thread().name}\n"
                    f"Echo: {mensaje_recibido}\n"
                )
                cliente_socket.send(respuesta.encode('utf-8'))
                
    except Exception as e:
        print(f"Error manejando cliente {numero_cliente}: {e}")
    finally:
        cliente_socket.close()
        print(f"Cliente {numero_cliente} desconectado")
        print(f"Hilos restantes: {threading.active_count() - 1}")

if __name__ == "__main__":
    main()