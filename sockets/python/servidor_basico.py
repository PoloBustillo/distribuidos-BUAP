#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor TCP básico que acepta conexiones secuenciales
Ejemplo simple de servidor que maneja un cliente a la vez
"""

import socket
import datetime

HOST = 'localhost'
PUERTO = 8080

def main():
    print("=== SERVIDOR BÁSICO ===")
    print(f"Iniciando servidor en {HOST}:{PUERTO}")
    
    # Crear socket del servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Permitir reutilizar la dirección
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen(5)
        
        print("Servidor iniciado. Esperando conexiones...")
        cliente_num = 0
        
        while True:
            # Aceptar conexión del cliente (BLOQUEA hasta que llegue una)
            cliente_socket, direccion_cliente = servidor.accept()
            cliente_num += 1
            
            print(f"Cliente {cliente_num} conectado desde {direccion_cliente}")
            
            # Manejar el cliente
            manejar_cliente(cliente_socket, cliente_num)
            
    except KeyboardInterrupt:
        print("\nServidor interrumpido por el usuario")
    except Exception as e:
        print(f"Error del servidor: {e}")
    finally:
        servidor.close()
        print("Servidor cerrado")

def manejar_cliente(cliente_socket, numero_cliente):
    """
    Maneja la comunicación con un cliente específico
    """
    try:
        # Enviar mensaje de bienvenida
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensaje_bienvenida = f"Bienvenido cliente {numero_cliente}! Hora: {timestamp}\n"
        cliente_socket.send(mensaje_bienvenida.encode('utf-8'))
        
        # Leer datos del cliente
        while True:
            datos = cliente_socket.recv(1024)
            if not datos:
                break
                
            mensaje_recibido = datos.decode('utf-8').strip()
            print(f"Cliente {numero_cliente}: {mensaje_recibido}")
            
            # Si el cliente dice "adios", terminar conexión
            if mensaje_recibido.lower() == "adios":
                respuesta = "¡Hasta luego!\n"
                cliente_socket.send(respuesta.encode('utf-8'))
                break
            
            # Echo: devolver el mismo mensaje con timestamp
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            respuesta = f"[{timestamp}] Echo: {mensaje_recibido}\n"
            cliente_socket.send(respuesta.encode('utf-8'))
            
    except Exception as e:
        print(f"Error manejando cliente {numero_cliente}: {e}")
    finally:
        cliente_socket.close()
        print(f"Cliente {numero_cliente} desconectado")

if __name__ == "__main__":
    main()