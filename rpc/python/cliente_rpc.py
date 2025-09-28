#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente RPC usando XML-RPC de la biblioteca estándar de Python
Conecta al servidor RPC y consume sus servicios remotos
"""

import xmlrpc.client
import time
import json
from datetime import datetime

class ClienteRPC:
    """Cliente para consumir servicios RPC"""
    
    def __init__(self, url="http://localhost:8888"):
        self.url = url
        self.servidor = None
    
    def conectar(self):
        """Conecta al servidor RPC"""
        try:
            print("=== CLIENTE XML-RPC ===")
            print(f"Conectando a {self.url}...")
            
            # Crear proxy del servidor RPC
            self.servidor = xmlrpc.client.ServerProxy(self.url)
            
            # Probar conexión
            respuesta_ping = self.servidor.ping("test de conexión")
            print(f"Conexión exitosa: {respuesta_ping}")
            
            # Obtener información del servidor
            info = self.servidor.obtener_info_servidor()
            print("\n--- Información del Servidor ---")
            print(f"Servidor: {info['nombre']}")
            print(f"Iniciado: {info['tiempo_inicio']}")
            print(f"Operaciones: {info['operaciones_realizadas']}")
            print(f"Resultados: {info['resultados_almacenados']}")
            
            return True
            
        except Exception as e:
            print(f"Error conectando al servidor RPC: {e}")
            print("Asegúrate de que servidor_rpc.py esté ejecutándose")
            return False
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        while True:
            print("\n=== MENU CLIENTE RPC ===")
            print("1.  Operaciones básicas (+, -, *, /)")
            print("2.  Operaciones avanzadas (potencia, raíz, factorial, fibonacci)")
            print("3.  Operaciones con listas")
            print("4.  Estadísticas de listas")
            print("5.  Gestionar resultados")
            print("6.  Información del servidor")
            print("7.  Pruebas de rendimiento")
            print("8.  Introspection (métodos disponibles)")
            print("9.  Salir")
            
            try:
                opcion = input("\nOpción: ").strip()
                
                if opcion == "1":
                    self.operaciones_basicas()
                elif opcion == "2":
                    self.operaciones_avanzadas()
                elif opcion == "3":
                    self.operaciones_listas()
                elif opcion == "4":
                    self.estadisticas_listas()
                elif opcion == "5":
                    self.gestionar_resultados()
                elif opcion == "6":
                    self.info_servidor()
                elif opcion == "7":
                    self.pruebas_rendimiento()
                elif opcion == "8":
                    self.introspection()
                elif opcion == "9":
                    print("¡Hasta luego!")
                    break
                else:
                    print("Opción inválida")
                    
            except Exception as e:
                print(f"Error: {e}")
    
    def operaciones_basicas(self):
        """Menú de operaciones básicas"""
        try:
            print("\n--- OPERACIONES BÁSICAS ---")
            a = float(input("Primer número: "))
            b = float(input("Segundo número: "))
            
            print("\nResultados (RPC):")
            print(f"{a} + {b} = {self.servidor.sumar(a, b)}")
            print(f"{a} - {b} = {self.servidor.restar(a, b)}")
            print(f"{a} * {b} = {self.servidor.multiplicar(a, b)}")
            
            try:
                print(f"{a} / {b} = {self.servidor.dividir(a, b)}")
            except xmlrpc.client.Fault as e:
                print(f"Error en división: {e.faultString}")
                
        except ValueError:
            print("Error: Ingresa números válidos")
        except Exception as e:
            print(f"Error RPC: {e}")
    
    def operaciones_avanzadas(self):
        """Menú de operaciones avanzadas"""
        print("\n--- OPERACIONES AVANZADAS ---")
        print("1. Potencia")
        print("2. Raíz cuadrada")
        print("3. Factorial")
        print("4. Fibonacci")
        
        try:
            opcion = input("Opción: ").strip()
            
            if opcion == "1":
                base = float(input("Base: "))
                exp = float(input("Exponente: "))
                resultado = self.servidor.potencia(base, exp)
                print(f"{base} ^ {exp} = {resultado}")
                
            elif opcion == "2":
                num = float(input("Número: "))
                try:
                    resultado = self.servidor.raiz_cuadrada(num)
                    print(f"sqrt({num}) = {resultado}")
                except xmlrpc.client.Fault as e:
                    print(f"Error: {e.faultString}")
                    
            elif opcion == "3":
                n = int(input("Número para factorial: "))
                try:
                    resultado = self.servidor.factorial(n)
                    print(f"{n}! = {resultado}")
                except xmlrpc.client.Fault as e:
                    print(f"Error: {e.faultString}")
                    
            elif opcion == "4":
                n = int(input("Posición en Fibonacci: "))
                try:
                    resultado = self.servidor.fibonacci(n)
                    print(f"F({n}) = {resultado}")
                except xmlrpc.client.Fault as e:
                    print(f"Error: {e.faultString}")
                    
        except ValueError:
            print("Error: Ingresa valores válidos")
        except Exception as e:
            print(f"Error RPC: {e}")
    
    def operaciones_listas(self):
        """Operaciones con listas de números"""
        try:
            print("\n--- OPERACIONES CON LISTAS ---")
            
            # Obtener lista de números
            numeros_str = input("Ingresa números separados por comas: ")
            numeros = [float(x.strip()) for x in numeros_str.split(",")]
            
            print(f"Lista original: {numeros}")
            
            print("\nOperaciones disponibles:")
            print("1. Cuadrado")
            print("2. Doble")
            print("3. Negativo")
            print("4. Raíz")
            
            opcion = input("Operación: ").strip()
            operaciones = {"1": "cuadrado", "2": "doble", "3": "negativo", "4": "raiz"}
            
            if opcion in operaciones:
                operacion = operaciones[opcion]
                resultado = self.servidor.operacion_lista(numeros, operacion)
                print(f"Resultado ({operacion}): {resultado}")
            else:
                operacion = input("Escribe la operación (cuadrado, doble, negativo, raiz): ")
                resultado = self.servidor.operacion_lista(numeros, operacion)
                print(f"Resultado ({operacion}): {resultado}")
                
        except ValueError:
            print("Error: Formato de números inválido")
        except xmlrpc.client.Fault as e:
            print(f"Error RPC: {e.faultString}")
        except Exception as e:
            print(f"Error: {e}")
    
    def estadisticas_listas(self):
        """Calcula estadísticas de listas"""
        try:
            print("\n--- ESTADÍSTICAS DE LISTAS ---")
            
            numeros_str = input("Ingresa números separados por comas: ")
            numeros = [float(x.strip()) for x in numeros_str.split(",")]
            
            estadisticas = self.servidor.estadisticas_lista(numeros)
            
            print("\nEstadísticas calculadas remotamente:")
            print(f"  Cantidad: {estadisticas['cantidad']}")
            print(f"  Suma: {estadisticas['suma']:.2f}")
            print(f"  Promedio: {estadisticas['promedio']:.2f}")
            print(f"  Mínimo: {estadisticas['minimo']:.2f}")
            print(f"  Máximo: {estadisticas['maximo']:.2f}")
            print(f"  Mediana: {estadisticas['mediana']:.2f}")
            
        except ValueError:
            print("Error: Formato de números inválido")
        except xmlrpc.client.Fault as e:
            print(f"Error RPC: {e.faultString}")
        except Exception as e:
            print(f"Error: {e}")
    
    def gestionar_resultados(self):
        """Gestiona resultados almacenados en el servidor"""
        print("\n--- GESTIÓN DE RESULTADOS ---")
        print("1. Guardar resultado")
        print("2. Recuperar resultado")
        print("3. Listar todas las claves")
        
        try:
            opcion = input("Opción: ").strip()
            
            if opcion == "1":
                clave = input("Clave: ")
                valor = float(input("Valor: "))
                
                if self.servidor.guardar_resultado(clave, valor):
                    print("¡Resultado guardado exitosamente!")
                    
            elif opcion == "2":
                clave = input("Clave a buscar: ")
                try:
                    valor = self.servidor.obtener_resultado(clave)
                    print(f"'{clave}' = {valor}")
                except xmlrpc.client.Fault as e:
                    print(f"Error: {e.faultString}")
                    
            elif opcion == "3":
                claves = self.servidor.listar_claves()
                print(f"\nClaves disponibles ({len(claves)}):")
                
                for clave in claves:
                    try:
                        valor = self.servidor.obtener_resultado(clave)
                        print(f"  '{clave}' = {valor}")
                    except:
                        print(f"  '{clave}' = [error al obtener valor]")
                        
        except ValueError:
            print("Error: Valor numérico inválido")
        except xmlrpc.client.Fault as e:
            print(f"Error RPC: {e.faultString}")
        except Exception as e:
            print(f"Error: {e}")
    
    def info_servidor(self):
        """Muestra información del servidor"""
        try:
            print("\n--- INFORMACIÓN DEL SERVIDOR ---")
            
            info = self.servidor.obtener_info_servidor()
            
            print(f"Nombre: {info['nombre']}")
            print(f"Tiempo de inicio: {info['tiempo_inicio']}")
            print(f"Operaciones realizadas: {info['operaciones_realizadas']}")
            print(f"Resultados almacenados: {info['resultados_almacenados']}")
            print(f"Hilos activos: {info['hilos_activos']}")
            print(f"Tiempo actual servidor: {info['tiempo_actual']}")
            
            # Comprobar latencia
            tiempo_cliente = time.time()
            tiempo_servidor = self.servidor.obtener_tiempo_servidor()
            latencia = abs(tiempo_cliente - tiempo_servidor) * 1000
            
            print(f"\n--- LATENCIA ---")
            print(f"Tiempo cliente: {tiempo_cliente}")
            print(f"Tiempo servidor: {tiempo_servidor}")
            print(f"Latencia aprox: {latencia:.2f} ms")
            
        except Exception as e:
            print(f"Error obteniendo información: {e}")
    
    def pruebas_rendimiento(self):
        """Realiza pruebas de rendimiento RPC"""
        try:
            print("\n--- PRUEBAS DE RENDIMIENTO ---")
            operaciones = int(input("¿Cuántas operaciones? "))
            
            print(f"Realizando {operaciones} sumas remotas...")
            
            inicio = time.time()
            
            for i in range(operaciones):
                self.servidor.sumar(i, i + 1)
                
                if i > 0 and i % 50 == 0:
                    print(".", end="", flush=True)
            
            fin = time.time()
            tiempo_total = fin - inicio
            
            print("\n\n--- RESULTADOS RENDIMIENTO ---")
            print(f"Operaciones completadas: {operaciones}")
            print(f"Tiempo total: {tiempo_total:.2f} segundos")
            print(f"Tiempo promedio por operación: {(tiempo_total/operaciones)*1000:.2f} ms")
            print(f"Operaciones por segundo: {operaciones/tiempo_total:.2f}")
            
        except ValueError:
            print("Error: Ingresa un número válido")
        except Exception as e:
            print(f"Error en prueba de rendimiento: {e}")
    
    def introspection(self):
        """Muestra métodos disponibles usando introspection"""
        try:
            print("\n--- MÉTODOS DISPONIBLES (INTROSPECTION) ---")
            
            # Listar métodos disponibles
            metodos = self.servidor.system.listMethods()
            
            print(f"\nMétodos disponibles ({len(metodos)}):")
            for metodo in sorted(metodos):
                if not metodo.startswith("system."):
                    try:
                        # Obtener ayuda del método
                        ayuda = self.servidor.system.methodHelp(metodo)
                        if ayuda:
                            print(f"  {metodo}: {ayuda}")
                        else:
                            print(f"  {metodo}")
                    except:
                        print(f"  {metodo}")
            
            print("\nMétodos del sistema:")
            for metodo in sorted(metodos):
                if metodo.startswith("system."):
                    print(f"  {metodo}")
                    
        except Exception as e:
            print(f"Error en introspection: {e}")

def main():
    cliente = ClienteRPC()
    
    if cliente.conectar():
        print("\n¡Listo para realizar llamadas RPC!")
        cliente.mostrar_menu()
    else:
        print("No se pudo conectar al servidor RPC")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCliente interrumpido por el usuario")