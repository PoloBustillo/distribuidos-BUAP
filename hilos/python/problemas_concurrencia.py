"""Demostración de problemas comunes de concurrencia."""

import threading
import time

contador = 0
saldo = 1000


def incrementar_contador(repeticiones: int) -> None:
    """Función con race condition en contador global."""
    global contador
    for _ in range(repeticiones):
        contador += 1  # Operación no atómica


def incrementar_contador(repeticiones: int) -> None:
    """Función con race condition en contador global."""
    global contador
    for _ in range(repeticiones):
        # Forzar race condition haciendo la operación más explícita
        temp = contador
        # Simular un pequeño procesamiento que aumenta la ventana de race condition
        # En Python, el GIL previene muchas race conditions, pero no todas
        for _ in range(10):  # Pequeño loop para crear más oportunidades
            pass
        contador = temp + 1


def demostrar_race_condition() -> None:
    """Demuestra race condition en contador."""
    global contador
    contador = 0
    
    print("1. RACE CONDITION - Contador:")
    # Usar parámetros que hagan más visible el problema
    repeticiones = 1000
    num_hilos = 10
    
    print(f"Ejecutando {num_hilos} hilos, cada uno incrementa {repeticiones} veces")
    print("(El GIL de Python puede prevenir algunas race conditions)")
    
    hilos = [
        threading.Thread(target=incrementar_contador, args=(repeticiones,)) 
        for _ in range(num_hilos)
    ]
    
    inicio = time.perf_counter()
    for hilo in hilos:
        hilo.start()
    
    for hilo in hilos:
        hilo.join()
    fin = time.perf_counter()
    
    esperado = repeticiones * num_hilos
    print(f"Valor esperado: {esperado}")
    print(f"Valor obtenido: {contador}")
    diferencia = abs(contador - esperado)
    print(f"¿Resultado correcto? {contador == esperado}")
    if diferencia > 0:
        print(f"¡RACE CONDITION DETECTADA! Perdidos: {diferencia} incrementos")
        print(f"Porcentaje de error: {(diferencia/esperado)*100:.2f}%")
    else:
        print("No se detectó race condition esta vez")
    print(f"Tiempo total: {fin - inicio:.3f}s")


def realizar_deposito(cantidad: int) -> None:
    """Simula depósito bancario sin sincronización."""
    global saldo
    saldo_actual = saldo
    # Simular procesamiento más largo para aumentar race condition
    time.sleep(0.01)  # 10ms para hacer más visible el problema
    saldo = saldo_actual + cantidad
    print(f"Depósito ${cantidad}, nuevo saldo: ${saldo}")


def realizar_retiro(cantidad: int) -> None:
    """Simula retiro bancario sin sincronización."""
    global saldo
    saldo_actual = saldo
    if saldo_actual >= cantidad:
        # Simular procesamiento más largo
        time.sleep(0.01)  # 10ms
        saldo = saldo_actual - cantidad
        print(f"Retiro ${cantidad}, nuevo saldo: ${saldo}")
    else:
        print(f"Fondos insuficientes para retirar ${cantidad}")


def demostrar_inconsistencia_bancaria() -> None:
    """Demuestra inconsistencia en operaciones bancarias."""
    global saldo
    saldo = 1000
    
    print("\n2. INCONSISTENCIA - Operaciones bancarias:")
    print(f"Saldo inicial: ${saldo}")
    
    def depositos() -> None:
        for i in range(5):  # Menos operaciones para que sea más claro
            realizar_deposito(50)
            time.sleep(0.02)
    
    def retiros() -> None:
        for i in range(5):
            realizar_retiro(30)
            time.sleep(0.025)
    
    hilo_dep = threading.Thread(target=depositos)
    hilo_ret = threading.Thread(target=retiros)
    
    hilo_dep.start()
    hilo_ret.start()
    
    hilo_dep.join()
    hilo_ret.join()
    
    esperado = 1000 + 5*50 - 5*30  # = 1100
    print(f"Saldo final: ${saldo}")
    print(f"Saldo esperado: ${esperado}")
    if saldo != esperado:
        diferencia = saldo - esperado
        print(f"¡INCONSISTENCIA DETECTADA! Diferencia: ${diferencia}")
    else:
        print("No se detectó inconsistencia esta vez")


class DatosCompartidos:
    """Clase para demostrar lecturas inconsistentes."""
    
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
    
    def actualizar(self, nuevo_x: int, nuevo_y: int) -> None:
        print(f"[Escritor] Actualizando x={nuevo_x}, y={nuevo_y}")
        self.x = nuevo_x
        # Simular retraso más largo entre actualizaciones
        time.sleep(0.05)  # 50ms para hacer más visible la inconsistencia
        self.y = nuevo_y
    
    def leer(self) -> None:
        valor_x = self.x
        # Pequeño retraso para aumentar chance de inconsistencia
        time.sleep(0.001)
        valor_y = self.y
        consistente = (valor_y == valor_x * 10)
        print(f"[Lector] x={valor_x}, y={valor_y} (consistente: {consistente})")


def demostrar_lecturas_inconsistentes() -> None:
    """Demuestra lecturas inconsistentes de datos."""
    print("\n3. LECTURAS INCONSISTENTES - Invariante x*10=y:")
    datos = DatosCompartidos()
    
    def escritor() -> None:
        for i in range(1, 6):  # Menos iteraciones para que sea más claro
            datos.actualizar(i, i * 10)
            time.sleep(0.1)  # Pausa entre actualizaciones
    
    def lector() -> None:
        for _ in range(15):  # Más lecturas que escrituras
            datos.leer()
            time.sleep(0.05)  # Leer más frecuentemente que escribir
    
    hilo_escritor = threading.Thread(target=escritor)
    hilo_lector = threading.Thread(target=lector)
    
    hilo_escritor.start()
    hilo_lector.start()
    
    hilo_escritor.join()
    hilo_lector.join()


def ejecutar_trabajador(nombre: str, tareas: int, datos_compartidos: dict) -> None:
    """Trabajador que actualiza recursos compartidos."""
    for i in range(tareas):
        # Simular acceso a múltiples recursos
        for recurso in ['A', 'B', 'C']:
            valor_actual = datos_compartidos.get(recurso, 0)
            # Simular procesamiento
            time.sleep(0.01)
            datos_compartidos[recurso] = valor_actual + 1
            print(f"{nombre} procesó recurso {recurso}: {datos_compartidos[recurso]}")
        time.sleep(0.02)


def demostrar_interleaving() -> None:
    """Demuestra interleaving problemático."""
    print("\n4. INTERLEAVING PROBLEMÁTICO - Recursos compartidos:")
    print("Nota: En Python, el GIL puede limitar algunos problemas de concurrencia")
    
    datos_compartidos = {'A': 0, 'B': 0, 'C': 0}
    print(f"Estado inicial: {datos_compartidos}")
    
    hilos = [
        threading.Thread(target=ejecutar_trabajador, args=(f"Trabajador-{i}", 3, datos_compartidos))
        for i in range(1, 4)
    ]
    
    for hilo in hilos:
        hilo.start()
    
    for hilo in hilos:
        hilo.join()
    
    print(f"Estado final: {datos_compartidos}")
    esperado_por_recurso = 9  # 3 trabajadores * 3 tareas
    
    problemas_detectados = []
    for recurso, valor in datos_compartidos.items():
        if valor != esperado_por_recurso:
            problemas_detectados.append(f"Recurso {recurso}: esperado {esperado_por_recurso}, obtenido {valor}")
    
    if problemas_detectados:
        print("¡PROBLEMAS DE CONCURRENCIA DETECTADOS!")
        for problema in problemas_detectados:
            print(f"  - {problema}")
    else:
        print("No se detectaron problemas esta vez (puede ser por el GIL)")


def main() -> None:
    """Función principal que ejecuta todas las demostraciones."""
    print("=== PROBLEMAS DE CONCURRENCIA EN PYTHON ===")
    print("Nota: Python tiene el GIL (Global Interpreter Lock) que previene muchos")
    print("problemas de concurrencia, pero no todos. Los delays están aumentados")
    print("para hacer más visibles los problemas que pueden ocurrir.\n")
    
    demostrar_race_condition()
    demostrar_inconsistencia_bancaria() 
    demostrar_lecturas_inconsistentes()
    demostrar_interleaving()
    
    print("\n=== RESUMEN ===")
    print("Estos ejemplos muestran por qué necesitamos sincronización.")
    print("El GIL de Python previene muchos problemas, pero no todos.")
    print("En aplicaciones reales, usar threading.Lock, RLock, etc.")


if __name__ == "__main__":
    main()


class DatosCompartidos:
    """Clase para demostrar lecturas inconsistentes."""
    
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
    
    def actualizar(self, nuevo_x: int, nuevo_y: int) -> None:
        print(f"[Escritor] Actualizando x={nuevo_x}, y={nuevo_y}")
        self.x = nuevo_x
        # Simular retraso entre actualizaciones
        time.sleep(0.01)
        self.y = nuevo_y
    
    def leer(self) -> None:
        valor_x = self.x
        valor_y = self.y
        consistente = (valor_y == valor_x * 10)
        print(f"[Lector] x={valor_x}, y={valor_y} (consistente: {consistente})")

def demostrar_inconsistencia_bancaria() -> None:
    """Demuestra inconsistencia en operaciones bancarias."""
    global saldo
    saldo = 1000
    
    print("\n1. INCONSISTENCIA - Operaciones bancarias:")
    print(f"Saldo inicial: ${saldo}")
    
    def depositos() -> None:
        for _ in range(10):
            realizar_deposito(50)
            time.sleep(0.01)
    
    def retiros() -> None:
        for _ in range(10):
            realizar_retiro(30)
            time.sleep(0.015)
    
    hilo_dep = threading.Thread(target=depositos)
    hilo_ret = threading.Thread(target=retiros)
    
    hilo_dep.start()
    hilo_ret.start()
    
    hilo_dep.join()
    hilo_ret.join()
    
    print(f"Saldo final: ${saldo}")
    print(f"Saldo esperado: ${1000 + 10*50 - 10*30} = $1200")


def demostrar_lecturas_inconsistentes() -> None:
    """Demuestra lecturas inconsistentes."""
    print("\n2. LECTURAS INCONSISTENTES:")
    datos = DatosCompartidos()
    
    def escritor() -> None:
        for i in range(5):
            datos.actualizar(i, i * 10)
            time.sleep(0.1)
    
    def lector() -> None:
        for _ in range(10):
            datos.leer()
            time.sleep(0.05)
    
    hilo_escritor = threading.Thread(target=escritor)
    hilo_lector = threading.Thread(target=lector)
    
    hilo_escritor.start()
    hilo_lector.start()
    
    hilo_escritor.join()
    hilo_lector.join()


def run_demo() -> None:
    """Ejecuta la demostración completa."""
    print("=== PROBLEMAS DE CONCURRENCIA ===")
    
    demostrar_inconsistencia_bancaria()
    demostrar_lecturas_inconsistentes()
    print()


if __name__ == "__main__":
    run_demo()
