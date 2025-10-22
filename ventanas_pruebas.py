# ventanas_pruebas.py
import tkinter as tk
from tkinter import ttk, messagebox
import math
import statistics as stats
from scipy.stats import chi2
from historial import cargar_historial

Z_CRIT = {0.10: 1.6448536269514722, 0.05: 1.959963984540054, 0.01: 2.5758293035489004}
KS_C = {0.10: 1.22, 0.05: 1.36, 0.01: 1.63}

def prueba_medias(samples, alpha=0.05):
    n = len(samples)
    if n == 0:
        return {'error': 'NO HAY DATOS'}
    mu = sum(samples) / n
    z = (mu - 0.5) / math.sqrt(1 / (12 * n))
    zc = Z_CRIT.get(alpha, Z_CRIT[0.05])
    ok = abs(z) <= zc
    return {"nombre": "Prueba de Medias", "resultado": "ACEPTA" if ok else "RECHAZA", "z": z, "zc": zc, "media": mu}

def prueba_varianza(samples, alpha=0.05):
    n = len(samples)
    if n < 2:
        return {'error': 'NO HAY DATOS'}
    s2 = stats.variance(samples)
    sigma2 = 1 / 12
    k = n - 1
    chi = k * s2 / sigma2
    low = chi2.ppf(alpha / 2, k)
    high = chi2.ppf(1 - alpha / 2, k)
    ok = low <= chi <= high
    return {"nombre": "Prueba de Varianza", "resultado": "ACEPTA" if ok else "RECHAZA", "chi2": chi, "rango": [low, high]}

def prueba_uniformidad(samples, alpha=0.05):
    n = len(samples)
    if n == 0:
        return {'error': 'NO HAY DATOS'}
    xs = sorted(samples)
    d_plus = max((i + 1) / n - x for i, x in enumerate(xs))
    d_minus = max(x - i / n for i, x in enumerate(xs))
    d = max(d_plus, d_minus)
    c = KS_C.get(alpha, KS_C[0.05])
    dcrit = c / math.sqrt(n)
    ok = d <= dcrit
    return {"nombre": "Prueba de Uniformidad (K-S)", "resultado": "ACEPTA" if ok else "RECHAZA", "D": d, "Dcrit": dcrit}

class VentanaPruebas(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Pruebas Estadísticas")
        self.geometry("800x600")

        self.frame_historial = ttk.LabelFrame(self, text="Seleccionar Datos del Historial"); self.frame_historial.pack(pady=10, padx=10, fill=tk.X)
        self.tree_historial = ttk.Treeview(self.frame_historial, columns=("Algoritmo", "Iteraciones"), show="headings")
        self.tree_historial.heading("Algoritmo", text="Algoritmo")
        self.tree_historial.heading("Iteraciones", text="Iteraciones")
        self.tree_historial.pack(fill=tk.BOTH, expand=True)

        self.frame_pruebas = ttk.LabelFrame(self, text="Seleccionar Prueba"); self.frame_pruebas.pack(pady=10, padx=10, fill=tk.X)
        ttk.Button(self.frame_pruebas, text="Prueba de Medias", command=lambda: self.ejecutar_prueba("medias")).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame_pruebas, text="Prueba de Varianza", command=lambda: self.ejecutar_prueba("varianza")).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame_pruebas, text="Prueba de Uniformidad", command=lambda: self.ejecutar_prueba("uniformidad")).pack(side=tk.LEFT, padx=5)

        self.frame_resultados = ttk.LabelFrame(self, text="Resultados"); self.frame_resultados.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.text_resultados = tk.Text(self.frame_resultados, wrap=tk.WORD, width=80, height=15); self.text_resultados.pack(fill=tk.BOTH, expand=True)

        ttk.Button(self, text="Volver atrás", width=15, command=self.destroy).pack(pady=10)
        self.cargar_historial()

    def cargar_historial(self):
        historial = cargar_historial()
        for item in historial:
            self.tree_historial.insert("", tk.END, values=(item["algoritmo"], len(item["data"])))

    def ejecutar_prueba(self, tipo_prueba):
        seleccion = self.tree_historial.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un registro del historial")
            return
        item_sel = self.tree_historial.item(seleccion)
        algoritmo = item_sel["values"][0]
        historial = cargar_historial()
        for it in historial:
            if it["algoritmo"] == algoritmo:
                samples = [fila[4] for fila in it["data"]] if algoritmo == "Cuadrados Medios" else [fila[5] for fila in it["data"]]
                resultado = self.realizar_prueba(tipo_prueba, samples)
                self.mostrar_resultado(resultado)
                break

    def realizar_prueba(self, tipo_prueba, samples):
        if tipo_prueba == "medias":
            return prueba_medias(samples)
        elif tipo_prueba == "varianza":
            return prueba_varianza(samples)
        elif tipo_prueba == "uniformidad":
            return prueba_uniformidad(samples)
        else:
            return {"error": "Prueba no reconocida"}

    def mostrar_resultado(self, resultado):
        self.text_resultados.delete(1.0, tk.END)
        if "error" in resultado:
            self.text_resultados.insert(tk.END, resultado["error"]); return
        self.text_resultados.insert(tk.END, f"{resultado['nombre']}\n")
        self.text_resultados.insert(tk.END, f"Resultado: {resultado['resultado']}\n")
        if resultado['nombre'] == "Prueba de Medias":
            self.text_resultados.insert(tk.END, f"Z calculado: {resultado['z']:.4f}\n")
            self.text_resultados.insert(tk.END, f"Z crítico: {resultado['zc']:.4f}\n")
            self.text_resultados.insert(tk.END, f"Media muestral: {resultado['media']:.4f}\n")
        elif resultado['nombre'] == "Prueba de Varianza":
            self.text_resultados.insert(tk.END, f"Chi² calculado: {resultado['chi2']:.4f}\n")
            self.text_resultados.insert(tk.END, f"Rango crítico: [{resultado['rango'][0]:.4f}, {resultado['rango'][1]:.4f}]\n")
        elif resultado['nombre'] == "Prueba de Uniformidad (K-S)":
            self.text_resultados.insert(tk.END, f"D calculado: {resultado['D']:.4f}\n")
            self.text_resultados.insert(tk.END, f"D crítico: {resultado['Dcrit']:.4f}\n")
