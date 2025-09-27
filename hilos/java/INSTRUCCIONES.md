# Instrucciones de Uso

## Compilar los ejemplos

Para compilar todos los ejemplos, ejecuta desde la raíz del proyecto:

```bash
javac -d . src/ejemplos/*.java
```

## Ejecutar ejemplos individuales

```bash
# Ejemplo básico de hilos
java ejemplos.HiloBasico

# Demostración de importancia de hilos
java ejemplos.ImportanciaHilos

# Problemas de concurrencia sin sincronización
java ejemplos.ProblemasConcurrencia

# Sincronización básica con synchronized
java ejemplos.SincronizacionBasica

# Comparación de contadores thread-safe
java ejemplos.ContadorConcurrente

# Patrón Productor-Consumidor
java ejemplos.ProduccionConsumo

# Pool de hilos con ExecutorService
java ejemplos.PoolDeHilos
```