#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente de chat que se conecta al servidor y permite chatear con otros usuarios
"""

import socket
import threading

HOST = 'localhost'
PUERTO = 8082

def main():
    print("=== CLIENTE DE CHAT ===")
    print(f"Conectando al chat en {HOST}:{PUERTO}")
    
    try:
        # Crear socket del cliente y conectar
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PUERTO))
        
        print("Conectado al servidor de chat!")
        
        # Crear hilo para leer mensajes del servidor
        hilo_lector = threading.Thread(
            target=leer_mensajes_servidor,
            args=(cliente,),
            daemon=True
        )
        hilo_lector.start()
        
        # Bucle principal para enviar mensajes
        while True:
            mensaje = input()
            
            if mensaje.lower().strip() == "/salir":
                cliente.send("/salir".encode('utf-8'))
                break
                
            cliente.send(mensaje.encode('utf-8'))
            
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor de chat.")
        print("Ejecuta primero: python servidor_chat.py")
    except KeyboardInterrupt:
        print("\nDesconectando del chat...")
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        cliente.close()
        print("Desconectado del chat")

def leer_mensajes_servidor(cliente_socket):
    """
    Hilo separado para leer mensajes del servidor continuamente
    """
    try:
        while True:
            mensaje = cliente_socket.recv(1024)
            if not mensaje:
                break
                
            print(mensaje.decode('utf-8'), end='')
            
    except Exception as e:
        if not cliente_socket._closed:
            print(f"Error leyendo mensajes: {e}")

if __name__ == "__main__":
    main()