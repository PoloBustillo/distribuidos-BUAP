#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor JSON-RPC simple usando solo HTTP y JSON
Demuestra RPC sin dependencias externas complejas
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import threading

class CalculadoraJSONRPC:
    """Calculadora que expone métodos vía JSON-RPC"""
    
    def __init__(self):
        self.contador = 0
        self.resultados = {}
    
    def sumar(self, a, b):
        self.contador += 1
        return float(a) + float(b)
    
    def restar(self, a, b):
        self.contador += 1
        return float(a) - float(b)
    
    def multiplicar(self, a, b):
        self.contador += 1
        return float(a) * float(b)
    
    def dividir(self, a, b):
        self.contador += 1
        if float(b) == 0:
            raise ValueError("División por cero")
        return float(a) / float(b)
    
    def potencia(self, base, exp):
        self.contador += 1
        return pow(float(base), float(exp))
    
    def info_servidor(self):
        return {
            "nombre": "JSON-RPC Calculadora",
            "operaciones": self.contador,
            "timestamp": datetime.now().isoformat(),
            "hilos": threading.active_count()
        }
    
    def listar_metodos(self):
        return [
            "sumar", "restar", "multiplicar", "dividir", 
            "potencia", "info_servidor", "listar_metodos"
        ]

class JSONRPCHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, calculadora=None, **kwargs):
        self.calculadora = calculadora
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        try:
            # Leer el cuerpo de la petición
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parsear JSON-RPC
            request = json.loads(post_data)
            
            # Procesar petición JSON-RPC
            response = self.procesar_jsonrpc(request)
            
            # Enviar respuesta
            self.enviar_respuesta_json(response)
            
        except json.JSONDecodeError:
            self.enviar_error_jsonrpc(-32700, "Parse error")
        except Exception as e:
            self.enviar_error_jsonrpc(-32603, f"Internal error: {str(e)}")
    
    def do_GET(self):
        # Servir información del servidor para peticiones GET
        if self.path == "/info":
            info = self.calculadora.info_servidor()
            self.enviar_respuesta_json(info, status=200)
        elif self.path == "/methods":
            methods = self.calculadora.listar_metodos()
            self.enviar_respuesta_json({"methods": methods}, status=200)
        else:
            # Documentación básica
            html = self.generar_documentacion()
            self.enviar_html(html)
    
    def procesar_jsonrpc(self, request):
        # Validar estructura JSON-RPC 2.0
        if not isinstance(request, dict):
            return self.crear_error_jsonrpc(-32600, "Invalid Request")
        
        jsonrpc = request.get("jsonrpc")
        method = request.get("method")
        params = request.get("params", [])
        request_id = request.get("id")
        
        if jsonrpc != "2.0":
            return self.crear_error_jsonrpc(-32600, "Invalid Request", request_id)
        
        if not method:
            return self.crear_error_jsonrpc(-32600, "Missing method", request_id)
        
        # Ejecutar método
        try:
            if hasattr(self.calculadora, method):
                metodo = getattr(self.calculadora, method)
                
                if isinstance(params, list):
                    resultado = metodo(*params)
                elif isinstance(params, dict):
                    resultado = metodo(**params)
                else:
                    resultado = metodo()
                
                return self.crear_respuesta_jsonrpc(resultado, request_id)
            else:
                return self.crear_error_jsonrpc(-32601, "Method not found", request_id)
                
        except TypeError as e:
            return self.crear_error_jsonrpc(-32602, f"Invalid params: {str(e)}", request_id)
        except Exception as e:
            return self.crear_error_jsonrpc(-32603, f"Internal error: {str(e)}", request_id)
    
    def crear_respuesta_jsonrpc(self, resultado, request_id):
        return {
            "jsonrpc": "2.0",
            "result": resultado,
            "id": request_id
        }
    
    def crear_error_jsonrpc(self, code, message, request_id=None):
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": request_id
        }
    
    def enviar_respuesta_json(self, data, status=200):
        json_data = json.dumps(data, indent=2)
        json_bytes = json_data.encode('utf-8')
        
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(json_bytes)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json_bytes)
    
    def enviar_error_jsonrpc(self, code, message):
        error_response = self.crear_error_jsonrpc(code, message)
        self.enviar_respuesta_json(error_response, status=400)
    
    def enviar_html(self, html):
        html_bytes = html.encode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html_bytes)))
        self.end_headers()
        
        self.wfile.write(html_bytes)
    
    def generar_documentacion(self):
        return f'''
<!DOCTYPE html>
<html><head><title>JSON-RPC Calculadora</title></head>
<body>
<h1>Servidor JSON-RPC 2.0</h1>
<p>Endpoint: <code>POST /</code></p>

<h2>Métodos Disponibles:</h2>
<ul>
    <li><strong>sumar(a, b)</strong> - Suma dos números</li>
    <li><strong>restar(a, b)</strong> - Resta dos números</li>
    <li><strong>multiplicar(a, b)</strong> - Multiplica dos números</li>
    <li><strong>dividir(a, b)</strong> - Divide dos números</li>
    <li><strong>potencia(base, exp)</strong> - Calcula potencia</li>
    <li><strong>info_servidor()</strong> - Información del servidor</li>
    <li><strong>listar_metodos()</strong> - Lista métodos disponibles</li>
</ul>

<h2>Ejemplo de Petición:</h2>
<pre>
{{
    "jsonrpc": "2.0",
    "method": "sumar",
    "params": [5, 3],
    "id": 1
}}
</pre>

<h2>Ejemplo de Respuesta:</h2>
<pre>
{{
    "jsonrpc": "2.0",
    "result": 8,
    "id": 1
}}
</pre>

<p><a href="/info">Información del servidor</a> | <a href="/methods">Métodos disponibles</a></p>
</body></html>
        '''
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] JSON-RPC: {format % args}")

def crear_handler_con_calculadora(calculadora):
    """Factory para crear handler con calculadora inyectada"""
    def handler(*args, **kwargs):
        return JSONRPCHandler(*args, calculadora=calculadora, **kwargs)
    return handler

def main():
    print("=== SERVIDOR JSON-RPC 2.0 ===")
    
    calculadora = CalculadoraJSONRPC()
    handler = crear_handler_con_calculadora(calculadora)
    
    servidor = HTTPServer(('localhost', 8889), handler)
    
    print("Servidor JSON-RPC iniciado en http://localhost:8889")
    print("\nEndpoints disponibles:")
    print("  POST /          - JSON-RPC 2.0 endpoint")
    print("  GET  /          - Documentación")
    print("  GET  /info      - Información del servidor")
    print("  GET  /methods   - Métodos disponibles")
    
    print("\nEjemplo con curl:")
    print('curl -X POST http://localhost:8889 \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"jsonrpc":"2.0","method":"sumar","params":[10,5],"id":1}\'')
    
    print("\nPresiona Ctrl+C para detener\n")
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor JSON-RPC...")
        servidor.shutdown()
        servidor.server_close()
        print("Servidor detenido")

if __name__ == "__main__":
    main()