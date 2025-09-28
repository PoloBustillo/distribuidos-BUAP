#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente JSON-RPC 2.0 simple
Demuestra uso de RPC con JSON sobre HTTP
"""

import json
import requests
import time
from datetime import datetime

class ClienteJSONRPC:
    """Cliente para JSON-RPC 2.0"""
    
    def __init__(self, url="http://localhost:8889"):
        self.url = url
        self.request_id = 1
        
    def llamar_metodo(self, metodo, parametros=None, timeout=5.0):
        """Realiza una llamada JSON-RPC"""
        payload = {
            "jsonrpc": "2.0",
            "method": metodo,
            "id": self.request_id
        }
        
        if parametros:
            payload["params"] = parametros
        
        self.request_id += 1
        
        try:
            response = requests.post(
                self.url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    return result["result"]
                elif "error" in result:
                    raise Exception(f"Error RPC: {result['error']['message']}")
                else:
                    raise Exception("Respuesta JSON-RPC inválida")
            else:
                raise Exception(f"HTTP Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión: {str(e)}")
    
    def sumar(self, a, b):
        return self.llamar_metodo("sumar", [a, b])
    
    def restar(self, a, b):
        return self.llamar_metodo("restar", [a, b])
    
    def multiplicar(self, a, b):
        return self.llamar_metodo("multiplicar", [a, b])
    
    def dividir(self, a, b):
        return self.llamar_metodo("dividir", [a, b])
    
    def potencia(self, base, exp):
        return self.llamar_metodo("potencia", [base, exp])
    
    def info_servidor(self):
        return self.llamar_metodo("info_servidor")
    
    def listar_metodos(self):
        return self.llamar_metodo("listar_metodos")

def mostrar_menu():
    print("\n=== CLIENTE JSON-RPC 2.0 ===")
    print("1. Suma")
    print("2. Resta") 
    print("3. Multiplicación")
    print("4. División")
    print("5. Potencia")
    print("6. Info del servidor")
    print("7. Listar métodos")
    print("8. Prueba de rendimiento")
    print("0. Salir")
    print("-" * 30)

def prueba_rendimiento(cliente, num_operaciones=100):
    """Prueba de rendimiento del cliente RPC"""
    print(f"Realizando {num_operaciones} operaciones...")
    
    inicio = time.time()
    errores = 0
    
    for i in range(num_operaciones):
        try:
            a, b = i % 100, (i + 1) % 50 + 1  # Evitar división por 0
            resultado = cliente.sumar(a, b)
        except Exception as e:
            errores += 1
            if errores <= 5:  # Solo mostrar primeros errores
                print(f"Error en operación {i}: {e}")
    
    fin = time.time()
    tiempo_total = fin - inicio
    ops_por_segundo = num_operaciones / tiempo_total
    
    print(f"\nResultados de rendimiento:")
    print(f"  Operaciones: {num_operaciones}")
    print(f"  Tiempo total: {tiempo_total:.2f} segundos") 
    print(f"  Ops/segundo: {ops_por_segundo:.2f}")
    print(f"  Errores: {errores}")
    print(f"  Latencia promedio: {(tiempo_total/num_operaciones)*1000:.2f} ms")

def main():
    cliente = ClienteJSONRPC()
    
    # Verificar conexión
    try:
        info = cliente.info_servidor()
        print(f"Conectado a: {info['nombre']}")
        print(f"Servidor iniciado: {info['timestamp']}")
    except Exception as e:
        print(f"Error al conectar: {e}")
        print("Asegúrate de que el servidor esté ejecutándose en localhost:8889")
        return
    
    while True:
        try:
            mostrar_menu()
            opcion = input("Selecciona opción: ").strip()
            
            if opcion == "0":
                print("¡Hasta luego!")
                break
            elif opcion == "1":
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
                resultado = cliente.sumar(a, b)
                print(f"Resultado: {a} + {b} = {resultado}")
                
            elif opcion == "2":
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
                resultado = cliente.restar(a, b)
                print(f"Resultado: {a} - {b} = {resultado}")
                
            elif opcion == "3":
                a = float(input("Primer número: "))
                b = float(input("Segundo número: "))
                resultado = cliente.multiplicar(a, b)
                print(f"Resultado: {a} * {b} = {resultado}")
                
            elif opcion == "4":
                a = float(input("Dividendo: "))
                b = float(input("Divisor: "))
                try:
                    resultado = cliente.dividir(a, b)
                    print(f"Resultado: {a} / {b} = {resultado}")
                except Exception as e:
                    print(f"Error: {e}")
                    
            elif opcion == "5":
                base = float(input("Base: "))
                exp = float(input("Exponente: "))
                resultado = cliente.potencia(base, exp)
                print(f"Resultado: {base} ^ {exp} = {resultado}")
                
            elif opcion == "6":
                info = cliente.info_servidor()
                print("\nInformación del servidor:")
                for clave, valor in info.items():
                    print(f"  {clave}: {valor}")
                    
            elif opcion == "7":
                metodos = cliente.listar_metodos()
                print("\nMétodos disponibles:")
                for i, metodo in enumerate(metodos, 1):
                    print(f"  {i}. {metodo}")
                    
            elif opcion == "8":
                num_ops = int(input("Número de operaciones (default 100): ") or "100")
                prueba_rendimiento(cliente, num_ops)
                
            else:
                print("Opción no válida")
                
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()