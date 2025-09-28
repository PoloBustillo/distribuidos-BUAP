#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente TCP básico que se conecta al servidor
Ejemplo simple de cliente que envía y recibe mensajes
"""

import socket

HOST = 'localhost'
PUERTO = 8080

def main():
    print("=== CLIENTE BÁSICO ===")
    print(f"Conectando al servidor {HOST}:{PUERTO}")
    
    try:
        # Crear socket del cliente y conectar
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PUERTO))
        
        print("Conectado al servidor!")
        
        # Recibir mensaje de bienvenida
        bienvenida = cliente.recv(1024).decode('utf-8')
        print(f"Servidor: {bienvenida}", end='')
        
        # Bucle de comunicación
        while True:
            # Leer mensaje del usuario
            mensaje = input("Tú: ")
            
            if not mensaje:
                break
                
            # Enviar mensaje al servidor
            cliente.send(mensaje.encode('utf-8'))
            
            # Recibir respuesta del servidor
            respuesta = cliente.recv(1024).decode('utf-8')
            print(f"Servidor: {respuesta}", end='')
            
            # Si enviamos "adios", salir del bucle
            if mensaje.lower() == "adios":
                break
                
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor.")
        print("Ejecuta primero: python servidor_basico.py")
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        cliente.close()
        print("Desconectado del servidor")

if __name__ == "__main__":
    main()