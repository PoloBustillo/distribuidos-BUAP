"""Comparación entre ejecución secuencial y concurrente usando hilos."""

import threading
import time


def tarea(nombre: str, duracion: float) -> None:
    print(f"{nombre} iniciada por {threading.current_thread().name}")
    time.sleep(duracion)
    print(f"{nombre} completada")


def run_demo() -> None:
    print("=== IMPORTANCIA DE LOS HILOS EN PYTHON ===")

    print("\n1. EJECUCIÓN SECUENCIAL:")
    inicio_seq = time.perf_counter()
    tarea("Tarea-A", 2)
    tarea("Tarea-B", 2)
    tarea("Tarea-C", 2)
    fin_seq = time.perf_counter()
    print(f"Tiempo total secuencial: {fin_seq - inicio_seq:.2f} s\n")

    print("2. EJECUCIÓN CONCURRENTE:")
    inicio_conc = time.perf_counter()
    hilos = [
        threading.Thread(target=tarea, args=("Tarea-A", 2)),
        threading.Thread(target=tarea, args=("Tarea-B", 2)),
        threading.Thread(target=tarea, args=("Tarea-C", 2)),
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    fin_conc = time.perf_counter()
    print(f"Tiempo total concurrente: {fin_conc - inicio_conc:.2f} s")

    mejora = (fin_seq - inicio_seq) / (fin_conc - inicio_conc)
    print(f"\nMejora aproximada: {mejora:.2f}x más rápido")

    print("\n3. RESPONSIVIDAD: tarea de fondo vs interfaz simulada")

    def tarea_larga() -> None:
        for i in range(1, 11):
            print(f"Procesando... {i * 10}%")
            time.sleep(0.4)

    def interfaz_responsiva() -> None:
        for i in range(15):
            print(f"[UI] Interfaz respondiendo tick {i}")
            time.sleep(0.25)

    hilo_largo = threading.Thread(target=tarea_larga)
    hilo_ui = threading.Thread(target=interfaz_responsiva)

    hilo_largo.start()
    hilo_ui.start()

    hilo_largo.join()
    hilo_ui.join()

    print("La interfaz se mantuvo responsiva durante la tarea larga.\n")

if __name__ == "__main__":
    run_demo()
