#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor RPC usando XML-RPC de la biblioteca estándar de Python
Demuestra Remote Procedure Calls sin dependencias externas
"""

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import time
from datetime import datetime
import math
import json

class CalculadoraRPC:
    """Clase que expone métodos como servicios RPC"""
    
    def __init__(self):
        self.nombre_servidor = f"CalculadoraXMLRPC-{int(time.time())}"
        self.tiempo_inicio = datetime.now()
        self.contador_operaciones = 0
        self.resultados = {
            "PI": math.pi,
            "E": math.e,
            "SQRT2": math.sqrt(2)
        }
        print(f"Servidor RPC inicializado: {self.nombre_servidor}")
    
    def sumar(self, a, b):
        """Suma dos números"""
        self.contador_operaciones += 1
        resultado = float(a) + float(b)
        self._log_operacion("SUMA", f"{a} + {b} = {resultado}")
        return resultado
    
    def restar(self, a, b):
        """Resta dos números"""
        self.contador_operaciones += 1
        resultado = float(a) - float(b)
        self._log_operacion("RESTA", f"{a} - {b} = {resultado}")
        return resultado
    
    def multiplicar(self, a, b):
        """Multiplica dos números"""
        self.contador_operaciones += 1
        resultado = float(a) * float(b)
        self._log_operacion("MULTIPLICACIÓN", f"{a} * {b} = {resultado}")
        return resultado
    
    def dividir(self, a, b):
        """Divide dos números"""
        self.contador_operaciones += 1
        if float(b) == 0:
            raise ValueError("División por cero no permitida")
        resultado = float(a) / float(b)
        self._log_operacion("DIVISIÓN", f"{a} / {b} = {resultado}")
        return resultado
    
    def potencia(self, base, exponente):
        """Calcula base elevado a exponente"""
        self.contador_operaciones += 1
        resultado = math.pow(float(base), float(exponente))
        self._log_operacion("POTENCIA", f"{base} ^ {exponente} = {resultado}")
        return resultado
    
    def raiz_cuadrada(self, numero):
        """Calcula la raíz cuadrada"""
        self.contador_operaciones += 1
        if float(numero) < 0:
            raise ValueError("Raíz cuadrada de número negativo no está definida")
        resultado = math.sqrt(float(numero))
        self._log_operacion("RAÍZ", f"sqrt({numero}) = {resultado}")
        return resultado
    
    def operacion_lista(self, numeros, operacion):
        """Aplica una operación a una lista de números"""
        self.contador_operaciones += 1
        if not numeros:
            raise ValueError("Lista vacía")
        
        resultado = []
        operacion = operacion.lower()
        
        for num in numeros:
            if operacion == "cuadrado":
                resultado.append(float(num) ** 2)
            elif operacion == "doble":
                resultado.append(float(num) * 2)
            elif operacion == "negativo":
                resultado.append(-float(num))
            elif operacion == "raiz":
                if float(num) >= 0:
                    resultado.append(math.sqrt(float(num)))
                else:
                    resultado.append(0)  # O manejar error
            else:
                raise ValueError(f"Operación '{operacion}' no soportada")
        
        self._log_operacion("VECTOR", f"{operacion.upper()}: {len(numeros)} elementos")
        return resultado
    
    def estadisticas_lista(self, numeros):
        """Calcula estadísticas básicas de una lista"""
        self.contador_operaciones += 1
        if not numeros:
            raise ValueError("Lista vacía")
        
        numeros_float = [float(x) for x in numeros]
        
        estadisticas = {
            "cantidad": len(numeros_float),
            "suma": sum(numeros_float),
            "promedio": sum(numeros_float) / len(numeros_float),
            "minimo": min(numeros_float),
            "maximo": max(numeros_float),
            "mediana": self._calcular_mediana(numeros_float)
        }
        
        self._log_operacion("ESTADÍSTICAS", f"{len(numeros)} elementos analizados")
        return estadisticas
    
    def _calcular_mediana(self, numeros):
        """Calcula la mediana de una lista"""
        sorted_nums = sorted(numeros)
        n = len(sorted_nums)
        
        if n % 2 == 0:
            return (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
        else:
            return sorted_nums[n//2]
    
    def guardar_resultado(self, clave, valor):
        """Guarda un resultado con una clave"""
        if not clave or not clave.strip():
            raise ValueError("Clave no puede estar vacía")
        
        self.resultados[str(clave).strip()] = float(valor)
        self._log_operacion("GUARDADO", f"'{clave}' = {valor}")
        return True
    
    def obtener_resultado(self, clave):
        """Recupera un resultado por su clave"""
        if not clave or not clave.strip():
            raise ValueError("Clave no puede estar vacía")
        
        clave = str(clave).strip()
        if clave not in self.resultados:
            raise ValueError(f"Clave '{clave}' no encontrada")
        
        valor = self.resultados[clave]
        self._log_operacion("RECUPERADO", f"'{clave}' = {valor}")
        return valor
    
    def listar_claves(self):
        """Lista todas las claves disponibles"""
        claves = list(self.resultados.keys())
        self._log_operacion("LISTADO", f"{len(claves)} claves disponibles")
        return claves
    
    def obtener_info_servidor(self):
        """Retorna información del servidor"""
        info = {
            "nombre": self.nombre_servidor,
            "tiempo_inicio": self.tiempo_inicio.isoformat(),
            "operaciones_realizadas": self.contador_operaciones,
            "resultados_almacenados": len(self.resultados),
            "hilos_activos": threading.active_count(),
            "tiempo_actual": datetime.now().isoformat()
        }
        self._log_operacion("INFO", "Información solicitada")
        return info
    
    def obtener_tiempo_servidor(self):
        """Retorna timestamp del servidor"""
        return time.time()
    
    def ping(self, mensaje="ping"):
        """Método simple para probar conectividad"""
        return f"pong: {mensaje} (servidor: {self.nombre_servidor})"
    
    def factorial(self, n):
        """Calcula el factorial de un número"""
        self.contador_operaciones += 1
        n = int(n)
        if n < 0:
            raise ValueError("Factorial no definido para números negativos")
        
        resultado = math.factorial(n)
        self._log_operacion("FACTORIAL", f"{n}! = {resultado}")
        return resultado
    
    def fibonacci(self, n):
        """Calcula el n-ésimo número de Fibonacci"""
        self.contador_operaciones += 1
        n = int(n)
        if n < 0:
            raise ValueError("Fibonacci no definido para números negativos")
        
        if n <= 1:
            resultado = n
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            resultado = b
        
        self._log_operacion("FIBONACCI", f"F({n}) = {resultado}")
        return resultado
    
    def _log_operacion(self, tipo, detalle):
        """Log interno de operaciones"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {tipo}: {detalle}")

class CustomRequestHandler(SimpleXMLRPCRequestHandler):
    """Handler personalizado para mostrar información de peticiones"""
    
    def log_message(self, format, *args):
        """Override para personalizar el logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Petición RPC: {format % args}")

def main():
    print("=== SERVIDOR XML-RPC ===\n")
    
    # Crear el servidor XML-RPC
    servidor = SimpleXMLRPCServer(
        ("localhost", 8888),
        requestHandler=CustomRequestHandler,
        allow_none=True
    )
    
    print("Servidor XML-RPC iniciado en http://localhost:8888")
    
    # Crear instancia de la calculadora
    calculadora = CalculadoraRPC()
    
    # Registrar la instancia completa
    servidor.register_instance(calculadora)
    
    # También se pueden registrar funciones individuales
    servidor.register_function(lambda x, y: x + y, 'suma_simple')
    servidor.register_function(lambda: "Servidor RPC funcionando!", 'test_servidor')
    
    # Registrar introspection functions
    servidor.register_introspection_functions()
    
    print("\nMétodos RPC disponibles:")
    print("  - Operaciones básicas: sumar, restar, multiplicar, dividir")
    print("  - Operaciones avanzadas: potencia, raiz_cuadrada, factorial, fibonacci")
    print("  - Operaciones con listas: operacion_lista, estadisticas_lista")
    print("  - Gestión: guardar_resultado, obtener_resultado, listar_claves")
    print("  - Información: obtener_info_servidor, obtener_tiempo_servidor, ping")
    print("  - Utilidades: suma_simple, test_servidor")
    
    print("\nEl servidor está listo para recibir llamadas RPC...")
    print("Los clientes pueden conectarse a: http://localhost:8888")
    print("Presiona Ctrl+C para detener el servidor\n")
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n\nDeteniendo servidor RPC...")
        servidor.shutdown()
        servidor.server_close()
        print("Servidor detenido")

if __name__ == "__main__":
    main()