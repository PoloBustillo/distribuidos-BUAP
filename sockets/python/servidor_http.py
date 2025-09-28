#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP básico que responde a peticiones GET simples
"""

import socket
import threading
import datetime
import urllib.parse
import sys
import os

HOST = 'localhost'
PUERTO = 8083
peticiones_atendidas = 0
lock = threading.Lock()

def main():
    print("=== SERVIDOR HTTP BÁSICO ===")
    print(f"Iniciando servidor HTTP en puerto {PUERTO}")
    print(f"Accede desde: http://{HOST}:{PUERTO}")
    
    # Crear socket del servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Permitir reutilizar la dirección
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen(10)
        
        print("Servidor HTTP iniciado. Esperando peticiones...")
        
        while True:
            cliente_socket, direccion_cliente = servidor.accept()
            
            # Manejar cada petición en un hilo separado
            hilo_peticion = threading.Thread(
                target=manejar_peticion_http,
                args=(cliente_socket, direccion_cliente),
                daemon=True
            )
            hilo_peticion.start()
            
    except KeyboardInterrupt:
        print("\nServidor HTTP interrumpido")
    except Exception as e:
        print(f"Error del servidor HTTP: {e}")
    finally:
        servidor.close()
        print("Servidor HTTP cerrado")

def manejar_peticion_http(cliente_socket, direccion_cliente):
    """
    Maneja una petición HTTP en un hilo separado
    """
    global peticiones_atendidas
    
    try:
        # Leer la petición HTTP
        peticion = cliente_socket.recv(1024).decode('utf-8')
        
        if not peticion:
            return
            
        # Parsear la primera línea de la petición
        lineas = peticion.split('\r\n')
        if lineas:
            primera_linea = lineas[0]
            print(f"Petición: {primera_linea}")
            
            partes = primera_linea.split()
            if len(partes) >= 2 and partes[0] == 'GET':
                ruta = partes[1]
                
                # Generar respuesta según la ruta
                contenido_html = generar_contenido_html(ruta)
                enviar_respuesta_http(cliente_socket, contenido_html)
                
                with lock:
                    peticiones_atendidas += 1
                    numero_peticion = peticiones_atendidas
                
                print(f"Petición {numero_peticion} atendida: {ruta}")
            
    except Exception as e:
        print(f"Error manejando petición HTTP: {e}")
    finally:
        cliente_socket.close()

def generar_contenido_html(ruta):
    """
    Genera el contenido HTML según la ruta solicitada
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = [
        "<!DOCTYPE html>",
        "<html><head><title>Servidor Python</title></head><body>",
        "<h1>Servidor HTTP Básico en Python</h1>",
        f"<p><strong>Ruta solicitada:</strong> {ruta}</p>",
        f"<p><strong>Timestamp:</strong> {timestamp}</p>",
        f"<p><strong>Peticiones atendidas:</strong> {peticiones_atendidas + 1}</p>"
    ]
    
    if ruta == "/":
        html.extend([
            "<h2>Página de Inicio</h2>",
            "<ul>",
            "<li><a href='/info'>Información del servidor</a></li>",
            "<li><a href='/tiempo'>Hora actual</a></li>",
            "<li><a href='/estado'>Estado del servidor</a></li>",
            "</ul>"
        ])
    elif ruta == "/info":
        html.extend([
            "<h2>Información del Servidor</h2>",
            f"<p>Python Version: {sys.version}</p>",
            f"<p>Puerto: {PUERTO}</p>",
            f"<p>Host: {HOST}</p>"
        ])
    elif ruta == "/tiempo":
        html.extend([
            "<h2>Hora Actual</h2>",
            f"<p>Hora del servidor: {timestamp}</p>"
        ])
    elif ruta == "/estado":
        try:
            # Información básica del sistema sin dependencias externas
            html.extend([
                "<h2>Estado del Servidor</h2>",
                f"<p>Hilos activos: {threading.active_count()}</p>",
                f"<p>ID del proceso: {os.getpid()}</p>",
                f"<p>Directorio actual: {os.getcwd()}</p>"
            ])
        except:
            html.extend([
                "<h2>Estado del Servidor</h2>",
                f"<p>Hilos activos: {threading.active_count()}</p>",
                "<p>Información del sistema limitada</p>"
            ])
    else:
        html.extend([
            "<h2>Página No Encontrada</h2>",
            f"<p>La ruta '{ruta}' no existe en este servidor.</p>",
            "<p><a href='/'>Volver al inicio</a></p>"
        ])
    
    html.extend([
        "<hr><p><small>Servidor HTTP Básico - Python</small></p>",
        "</body></html>"
    ])
    
    return "\n".join(html)

def enviar_respuesta_http(cliente_socket, contenido_html):
    """
    Envía una respuesta HTTP completa
    """
    contenido_bytes = contenido_html.encode('utf-8')
    
    # Headers HTTP
    respuesta = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html; charset=UTF-8",
        f"Content-Length: {len(contenido_bytes)}",
        "Connection: close",
        "",  # Línea vacía separa headers del contenido
        contenido_html
    ]
    
    respuesta_completa = "\r\n".join(respuesta)
    cliente_socket.send(respuesta_completa.encode('utf-8'))

if __name__ == "__main__":
    main()