#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor de chat multi-usuario que permite comunicación entre clientes
Cada cliente se maneja en un hilo separado y los mensajes se difunden a todos
"""

import socket
import threading
import datetime

HOST = 'localhost'
PUERTO = 8082

# Diccionario thread-safe para almacenar clientes conectados
clientes_conectados = {}
lock = threading.Lock()

def main():
    print("=== SERVIDOR DE CHAT ===")
    print(f"Iniciando servidor de chat en {HOST}:{PUERTO}")
    
    # Crear socket del servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Permitir reutilizar la dirección
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen(10)
        
        print("Servidor de chat iniciado. Esperando usuarios...")
        
        while True:
            # Aceptar conexión del cliente
            cliente_socket, direccion_cliente = servidor.accept()
            
            # Crear hilo para manejar este cliente
            hilo_cliente = threading.Thread(
                target=manejar_cliente_chat,
                args=(cliente_socket, direccion_cliente)
            )
            hilo_cliente.daemon = True
            hilo_cliente.start()
            
    except KeyboardInterrupt:
        print("\nServidor de chat interrumpido")
    except Exception as e:
        print(f"Error del servidor: {e}")
    finally:
        servidor.close()
        print("Servidor de chat cerrado")

def manejar_cliente_chat(cliente_socket, direccion_cliente):
    """
    Maneja un cliente del chat en un hilo separado
    """
    nombre_cliente = None
    
    try:
        # Pedir nombre del usuario
        cliente_socket.send("Ingresa tu nombre: ".encode('utf-8'))
        nombre_cliente = cliente_socket.recv(1024).decode('utf-8').strip()
        
        if not nombre_cliente:
            nombre_cliente = f"Usuario_{direccion_cliente[1]}"
        
        # Agregar cliente al diccionario (thread-safe)
        with lock:
            clientes_conectados[nombre_cliente] = cliente_socket
            numero_clientes = len(clientes_conectados)
        
        print(f"Usuario '{nombre_cliente}' conectado desde {direccion_cliente}")
        
        # Notificar a todos que se unió un nuevo usuario
        mensaje_union = f"*** {nombre_cliente} se unió al chat ({numero_clientes} usuarios conectados) ***"
        difundir_mensaje(mensaje_union, excluir=nombre_cliente)
        
        # Enviar mensaje de bienvenida al nuevo usuario
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        bienvenida = (
            f"\n=== BIENVENIDO AL CHAT ===\n"
            f"Hora: {timestamp}\n"
            f"Usuarios conectados: {numero_clientes}\n"
            f"Comandos: /usuarios, /salir\n"
            f"==========================\n"
        )
        cliente_socket.send(bienvenida.encode('utf-8'))
        
        # Bucle principal del chat
        while True:
            datos = cliente_socket.recv(1024)
            if not datos:
                break
                
            mensaje = datos.decode('utf-8').strip()
            
            if mensaje.lower() == "/salir":
                break
            elif mensaje.lower() == "/usuarios":
                with lock:
                    lista_usuarios = list(clientes_conectados.keys())
                respuesta = f"Usuarios conectados ({len(lista_usuarios)}): {', '.join(lista_usuarios)}\n"
                cliente_socket.send(respuesta.encode('utf-8'))
            else:
                # Difundir mensaje a todos los usuarios
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                mensaje_completo = f"[{timestamp}] {nombre_cliente}: {mensaje}"
                print(mensaje_completo)  # Log en el servidor
                difundir_mensaje(mensaje_completo, excluir=nombre_cliente)
                
    except Exception as e:
        print(f"Error con usuario '{nombre_cliente}': {e}")
    finally:
        # Remover cliente del diccionario
        if nombre_cliente:
            with lock:
                clientes_conectados.pop(nombre_cliente, None)
                numero_clientes = len(clientes_conectados)
            
            # Notificar a todos que el usuario se desconectó
            mensaje_salida = f"*** {nombre_cliente} abandonó el chat ({numero_clientes} usuarios restantes) ***"
            difundir_mensaje(mensaje_salida)
            print(f"Usuario '{nombre_cliente}' desconectado")
        
        cliente_socket.close()

def difundir_mensaje(mensaje, excluir=None):
    """
    Envía un mensaje a todos los clientes conectados
    """
    mensaje_con_newline = mensaje + "\n"
    clientes_desconectados = []
    
    with lock:
        for nombre, socket_cliente in clientes_conectados.items():
            if nombre != excluir:  # No enviar al remitente
                try:
                    socket_cliente.send(mensaje_con_newline.encode('utf-8'))
                except:
                    # Cliente desconectado, marcarlo para eliminación
                    clientes_desconectados.append(nombre)
        
        # Eliminar clientes desconectados
        for nombre in clientes_desconectados:
            clientes_conectados.pop(nombre, None)
            print(f"Cliente {nombre} eliminado (conexión perdida)")

if __name__ == "__main__":
    main()