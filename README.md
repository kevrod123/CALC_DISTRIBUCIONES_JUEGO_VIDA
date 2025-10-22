# CALC_DISTRIBUCIONES_JUEGO_VIDA
Simulador Interactivo de Números Pseudoaleatorios y Simulaciones Dinámicas (Tkinter)
Definición del Sistema
Este proyecto es un simulador interactivo y didáctico desarrollado en Python (Tkinter + Matplotlib) que combina métodos de generación pseudoaleatoria, distribuciones probabilísticas, simulaciones visuales y herramientas estadísticas en una aplicación con menú unificado y modular.

Permite:
- Generar números pseudoaleatorios mediante distintos algoritmos clásicos.
- Aplicar distribuciones estadísticas (Uniforme, Normal, Exponencial, Poisson) usando esos generadores como fuente de aleatoriedad.
- Simular sistemas dinámicos:
   - Juego de la Vida (1D y 2D).
   - Simulación tipo COVID-19 con propagación visual.
- Realizar análisis, gráficos e historial de resultados.
- Exportar datos generados a Excel y realizar pruebas estadísticas.

# ELEMENTOS DEL PROGRAMA
1. Menú principal (main.py)
Ventana inicial que permite navegar entre módulos:
- Generadores de números pseudoaleatorios.
- Pruebas estadísticas.
- Distribuciones probabilísticas.
- Simulaciones (Vida, COVID).

2. Generadores pseudoaleatorios
Implementados en algoritmos.py y visualizados en ventanas.py.
Historial y exportaciones.

Cada generador muestra:
- Tabla iterativa de resultados.
- Gráfico de evolución (ri vs. Iteración).
- Opción para exportar a Excel.
- Almacenamiento automático en el historial.

3. Distribuciones aleatorias (ventanas_distribuciones.py)
Usan los generadores pseudoaleatorios como base para crear las siguientes distribuciones
Cada distribución genera un histograma visual con colores, bordes y cuadrícula, de apariencia profesional.

4. Juego de la Vida (1D y 2D)
- Simulación del autómata celular de Conway:
- Configuración de tamaño y velocidad.
- Animación en tiempo real mediante after().
- Control de inicio, pausa y reinicio.
- En la versión 2D se usan celdas vivas/muertas en una cuadrícula de colores.
