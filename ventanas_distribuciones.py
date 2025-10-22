# ventanas_distribuciones.py
import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import RNGStream

class VentanaDistribuciones(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Distribuciones Aleatorias (con generadores propios)")
        self.geometry("980x700")
        self.configure(bg="#F4F6F7")

        # ======= FRAME DE CONTROLES =======
        control = ttk.LabelFrame(self, text="Parámetros")
        control.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(control, text="Distribución:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cb_dist = ttk.Combobox(control, values=["Uniforme", "Normal (Box-Muller)", "Exponencial", "Poisson"], state="readonly")
        self.cb_dist.current(0)
        self.cb_dist.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(control, text="Generador:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.cb_gen = ttk.Combobox(control, values=["Cuadrados", "Productos", "Constante"], state="readonly")
        self.cb_gen.current(0)
        self.cb_gen.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(control, text="X0 / Semilla o Constante:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.e_x0 = ttk.Entry(control, width=12)
        self.e_x0.insert(0, "5735")
        self.e_x0.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(control, text="X1 (si aplica):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.e_x1 = ttk.Entry(control, width=12)
        self.e_x1.insert(0, "1234")
        self.e_x1.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(control, text="n (muestras):").grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.e_n = ttk.Entry(control, width=10)
        self.e_n.insert(0, "1000")
        self.e_n.grid(row=1, column=5, padx=5, pady=5)

        # ======= PARÁMETROS EXTRA =======
        ex = ttk.LabelFrame(self, text="Parámetros específicos")
        ex.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(ex, text="Normal: mu").grid(row=0, column=0, padx=5, pady=5)
        self.e_mu = ttk.Entry(ex, width=10)
        self.e_mu.insert(0, "0")
        self.e_mu.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(ex, text="Normal: sigma").grid(row=0, column=2, padx=5, pady=5)
        self.e_sigma = ttk.Entry(ex, width=10)
        self.e_sigma.insert(0, "1")
        self.e_sigma.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(ex, text="Exponencial: lambda").grid(row=0, column=4, padx=5, pady=5)
        self.e_lam = ttk.Entry(ex, width=10)
        self.e_lam.insert(0, "1")
        self.e_lam.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(ex, text="Poisson: lambda").grid(row=0, column=6, padx=5, pady=5)
        self.e_lam_pois = ttk.Entry(ex, width=10)
        self.e_lam_pois.insert(0, "3")
        self.e_lam_pois.grid(row=0, column=7, padx=5, pady=5)

        # ======= BOTÓN DE ACCIÓN =======
        ttk.Button(self, text="Generar y graficar", command=self.generar).pack(pady=8)

        # ======= ÁREA DE GRÁFICO =======
        self.fig = plt.Figure(figsize=(8,5))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _stream(self, metodo, x0, x1, n):
        if metodo == "Cuadrados":
            m = "cuadrados"
        elif metodo == "Productos":
            m = "productos"
        else:
            m = "constante"
        return RNGStream(m, x0, x1, n=max(n*2, 2000))

    def generar(self):
        try:
            dist = self.cb_dist.get()
            gen = self.cb_gen.get()
            x0 = int(self.e_x0.get())
            x1 = int(self.e_x1.get()) if self.e_x1.get().strip() else None
            n = int(self.e_n.get())

            mu = float(self.e_mu.get())
            sigma = float(self.e_sigma.get())
            lam = float(self.e_lam.get())
            lam_p = float(self.e_lam_pois.get())

            rng = self._stream(gen, x0, x1, n)
            vals = []

            if dist == "Uniforme":
                vals = [rng.u() for _ in range(n)]

            elif dist == "Normal (Box-Muller)":
                while len(vals) < n:
                    u1, u2 = rng.pair()
                    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)
                    vals.append(mu + sigma * z0)

            elif dist == "Exponencial":
                vals = [-math.log(1.0 - rng.u()) / lam for _ in range(n)]

            elif dist == "Poisson":
                for _ in range(n):
                    L = math.exp(-lam_p)
                    k = 0
                    p = 1.0
                    while p > L:
                        k += 1
                        p *= rng.u()
                    vals.append(k - 1)
            else:
                vals = [rng.u() for _ in range(n)]

            # ======= CONFIGURAR EL GRÁFICO =======
            self.ax.clear()

            if dist == "Uniforme":
                # Ajustes específicos para lograr un histograma plano
                self.ax.hist(
                    vals, bins=10, edgecolor='black', color='#5DADE2',
                    alpha=0.8, rwidth=0.9, range=(0, 1)
                )
            else:
                bins = 30 if dist != "Poisson" else max(10, min(50, int(max(vals)+3)))
                self.ax.hist(
                    vals, bins=bins, edgecolor='black', alpha=0.75, color='#58D68D'
                )

            self.ax.set_title(f"{dist} usando generador: {gen}", fontsize=12, fontweight="bold", color="#1B4F72")
            self.ax.set_xlabel("Valor", fontsize=10)
            self.ax.set_ylabel("Frecuencia", fontsize=10)
            self.ax.grid(True, linestyle="--", alpha=0.5)
            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")
