# utils.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

def exportar_a_excel(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a Excel: {e}")
        return False

def mostrar_grafico_en_ventana(ventana, data, titulo, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(data["Iteración"], data["ri"], marker='o')
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def mostrar_histograma_en_ventana(ventana, data, titulo):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(data["ri"], bins=10, edgecolor='black', alpha=0.7)
    ax.set_title(titulo)
    ax.set_xlabel("Valor de ri")
    ax.set_ylabel("Frecuencia")
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ======= Puente de RNG (convierte tus generadores en flujo uniforme 0-1) =======
class RNGStream:
    """
    Iterador de U(0,1) a partir de tus métodos:
      - 'cuadrados' -> usa cuadrados_medios(x0, n)
      - 'productos' -> usa productos_medios(x0, x1, n)
      - 'constante' -> usa multiplicador_constante(x0, x1, n)
    """
    def __init__(self, metodo, x0, x1=None, n=10000):
        from algoritmos import cuadrados_medios, productos_medios, multiplicador_constante
        self.buf = []
        metodo = metodo.lower()
        if metodo == 'cuadrados':
            self.buf = [fila[4] for fila in cuadrados_medios(int(x0), int(n))]
        elif metodo == 'productos':
            if x1 is None:
                raise ValueError("Se requiere x1 para productos medios")
            self.buf = [fila[5] for fila in productos_medios(int(x0), int(x1), int(n))]
        elif metodo == 'constante':
            if x1 is None:
                raise ValueError("Se requiere x1 para multiplicador constante")
            self.buf = [fila[5] for fila in multiplicador_constante(int(x0), int(x1), int(n))]
        else:
            raise ValueError("Método no reconocido")
        # Evitar exactos 0 o 1 en transformadas (clipping suave)
        self.idx = 0
        self.eps = 1e-12
        self.one = 1 - 1e-12

    def u(self):
        """Devuelve un U(0,1) del buffer, con clipping para Box-Muller/Exponencial."""
        if self.idx >= len(self.buf):
            # reciclado simple (también podría regenerarse)
            self.idx = 0
        val = self.buf[self.idx]
        self.idx += 1
        if val <= 0.0: val = self.eps
        if val >= 1.0: val = self.one
        return float(val)

    def pair(self):
        """Devuelve dos U(0,1) para Box-Muller."""
        return self.u(), self.u()
