"""Demostración básica de creación de hilos en Python."""

import threading
import time

class WorkerThread(threading.Thread):
    def __init__(self, name: str, delay: float) -> None:
        super().__init__(name=name)
        self.delay = delay

    def run(self) -> None:
        for i in range(5):
            print(f"[{self.name}] iteración {i + 1}")
            time.sleep(self.delay)
        print(f"[{self.name}] finalizó")

def run_demo() -> None:
    print("=== EJEMPLO BÁSICO DE HILOS EN PYTHON ===")
    print(f"Hilo principal: {threading.current_thread().name}")

    hilo_1 = WorkerThread(name="Hilo-Personalizado", delay=0.5)
    def lambda_worker() -> None:
        for i in range(5):
            print(f"[LambdaThread] iteración {i + 1}")
            time.sleep(0.5)

    hilo_2 = threading.Thread(target=lambda_worker, name="LambdaThread")

    hilo_1.start()
    hilo_2.start()

    hilo_1.join()
    hilo_2.join()

    print("Todos los hilos han terminado.\n")

if __name__ == "__main__":
    run_demo()
