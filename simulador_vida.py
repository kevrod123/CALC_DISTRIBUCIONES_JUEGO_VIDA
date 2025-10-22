# simulador_vida.py (versión mejorada con color y velocidad)
import tkinter as tk
from tkinter import ttk, colorchooser
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VentanaVida(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🌱 Juego de la Vida (1D / 2D) - Versión Mejorada")
        self.geometry("1000x720")
        self.configure(bg="#222831")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#222831")
        style.configure("TLabel", background="#222831", foreground="white", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TLabelframe", background="#393E46", foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", background="#393E46", foreground="white")

        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab2d = ttk.Frame(nb)
        nb.add(self.tab2d, text="🧩 Vida 2D (Conway)")

        self.tab1d = ttk.Frame(nb)
        nb.add(self.tab1d, text="⚙️ Vida 1D (Regla Wolfram)")

        # ---- 2D ----
        ctrl2 = ttk.LabelFrame(self.tab2d, text="Controles 2D")
        ctrl2.pack(fill=tk.X, padx=8, pady=8)

        ttk.Label(ctrl2, text="Filas").grid(row=0, column=0, padx=5)
        self.r2 = tk.IntVar(value=50)
        ttk.Entry(ctrl2, textvariable=self.r2, width=8).grid(row=0, column=1)

        ttk.Label(ctrl2, text="Cols").grid(row=0, column=2, padx=5)
        self.c2 = tk.IntVar(value=50)
        ttk.Entry(ctrl2, textvariable=self.c2, width=8).grid(row=0, column=3)

        ttk.Label(ctrl2, text="p vivo").grid(row=0, column=4, padx=5)
        self.p2 = tk.DoubleVar(value=0.2)
        ttk.Entry(ctrl2, textvariable=self.p2, width=8).grid(row=0, column=5)

        ttk.Button(ctrl2, text="Crear", command=self.g2_create).grid(row=0, column=6, padx=5)
        ttk.Button(ctrl2, text="Paso", command=self.g2_step).grid(row=0, column=7, padx=5)
        self.btn_run2 = ttk.Button(ctrl2, text="▶ Ejecutar", command=self.g2_toggle)
        self.btn_run2.grid(row=0, column=8, padx=5)
        ttk.Button(ctrl2, text="⟳ Reiniciar", command=self.g2_reset).grid(row=0, column=9, padx=5)

        # selector de color
        ttk.Label(ctrl2, text="Colormap:").grid(row=0, column=10, padx=5)
        self.colormap2 = tk.StringVar(value="viridis")
        self.cb_color2 = ttk.Combobox(ctrl2, textvariable=self.colormap2,
                                      values=["gray", "viridis", "plasma", "inferno", "coolwarm"],
                                      width=10, state="readonly")
        self.cb_color2.grid(row=0, column=11, padx=5)

        ttk.Label(ctrl2, text="Velocidad").grid(row=0, column=12, padx=5)
        self.speed2 = tk.DoubleVar(value=150)
        tk.Scale(ctrl2, variable=self.speed2, from_=50, to=500, orient="horizontal",
                 length=150, bg="#393E46", fg="white", troughcolor="#00ADB5").grid(row=0, column=13, padx=5)

        self.fig2 = plt.Figure(figsize=(6, 5), facecolor="#222831")
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.tab2d)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.grid2 = None
        self.running2 = False

        # ---- 1D ----
        ctrl1 = ttk.LabelFrame(self.tab1d, text="Controles 1D")
        ctrl1.pack(fill=tk.X, padx=8, pady=8)

        ttk.Label(ctrl1, text="Longitud").grid(row=0, column=0, padx=5)
        self.len1 = tk.IntVar(value=200)
        ttk.Entry(ctrl1, textvariable=self.len1, width=8).grid(row=0, column=1)

        ttk.Label(ctrl1, text="Regla (0-255)").grid(row=0, column=2, padx=5)
        self.rule1 = tk.IntVar(value=30)
        ttk.Entry(ctrl1, textvariable=self.rule1, width=8).grid(row=0, column=3)

        ttk.Button(ctrl1, text="Crear", command=self.g1_create).grid(row=0, column=4, padx=5)
        ttk.Button(ctrl1, text="Paso", command=self.g1_step).grid(row=0, column=5, padx=5)
        self.btn_run1 = ttk.Button(ctrl1, text="▶ Ejecutar", command=self.g1_toggle)
        self.btn_run1.grid(row=0, column=6, padx=5)
        ttk.Button(ctrl1, text="⟳ Reiniciar", command=self.g1_reset).grid(row=0, column=7, padx=5)

        ttk.Label(ctrl1, text="Velocidad").grid(row=0, column=8, padx=5)
        self.speed1 = tk.DoubleVar(value=100)
        tk.Scale(ctrl1, variable=self.speed1, from_=30, to=300, orient="horizontal",
                 length=150, bg="#393E46", fg="white", troughcolor="#00ADB5").grid(row=0, column=9, padx=5)

        self.fig1 = plt.Figure(figsize=(7, 5), facecolor="#222831")
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab1d)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.state1 = None
        self.rule_map = None
        self.history1 = []
        self.running1 = False

    # ===== 2D =====
    def g2_create(self):
        r, c, p = max(5, int(self.r2.get())), max(5, int(self.c2.get())), float(self.p2.get())
        self.grid2 = (np.random.random((r, c)) < p).astype(int)
        self._g2_draw()

    def _g2_draw(self):
        cmap_name = self.colormap2.get()
        self.ax2.clear()
        self.ax2.imshow(self.grid2, interpolation="nearest", cmap=cmap_name)
        self.ax2.set_title(f"Vida 2D - t={getattr(self, 't2', 0)}", color="white")
        self.ax2.axis("off")
        self.canvas2.draw()

    def g2_step(self):
        if self.grid2 is None:
            self.g2_create()
        g = self.grid2
        new = np.zeros_like(g)
        R, C = g.shape
        for r in range(R):
            for c in range(C):
                total = np.sum(g[max(0, r - 1):r + 2, max(0, c - 1):c + 2]) - g[r, c]
                if g[r, c] == 1:
                    new[r, c] = 1 if total in (2, 3) else 0
                else:
                    new[r, c] = 1 if total == 3 else 0
        self.grid2 = new
        self.t2 = getattr(self, 't2', 0) + 1
        self._g2_draw()

    def g2_toggle(self):
        self.running2 = not self.running2
        self.btn_run2.config(text="⏸️ Pausar" if self.running2 else "▶ Ejecutar")
        if self.running2:
            self._g2_loop()

    def _g2_loop(self):
        if not self.running2:
            return
        self.g2_step()
        delay = int(self.speed2.get())
        self.after(delay, self._g2_loop)

    def g2_reset(self):
        if self.grid2 is not None:
            self.t2 = 0
            self.g2_create()

    # ===== 1D =====
    def g1_create(self):
        L = max(10, int(self.len1.get()))
        rule = min(255, max(0, int(self.rule1.get())))
        bits = [(rule >> i) & 1 for i in range(8)]
        trip = [(1, 1, 1), (1, 1, 0), (1, 0, 1), (1, 0, 0),
                (0, 1, 1), (0, 1, 0), (0, 0, 1), (0, 0, 0)]
        self.rule_map = {trip[i]: bits[7 - i] for i in range(8)}
        self.state1 = np.zeros(L, dtype=int)
        self.state1[L // 2] = 1
        self.history1 = [self.state1.copy()]
        self._g1_draw()

    def g1_step(self):
        if self.state1 is None:
            self.g1_create()
        L = len(self.state1)
        new = np.zeros_like(self.state1)
        for i in range(L):
            left = self.state1[(i - 1) % L]
            center = self.state1[i]
            right = self.state1[(i + 1) % L]
            new[i] = self.rule_map[(left, center, right)]
        self.state1 = new
        self.history1.append(new.copy())
        if len(self.history1) > 200:
            self.history1.pop(0)
        self._g1_draw()

    def _g1_draw(self):
        self.ax1.clear()
        self.ax1.imshow(np.array(self.history1), aspect="auto",
                        interpolation="nearest", cmap="coolwarm")
        self.ax1.set_title(f"Vida 1D - regla {self.rule1.get()}", color="white")
        self.ax1.axis("off")
        self.canvas1.draw()

    def g1_toggle(self):
        self.running1 = not self.running1
        self.btn_run1.config(text="⏸️ Pausar" if self.running1 else "▶ Ejecutar")
        if self.running1:
            self._g1_loop()

    def _g1_loop(self):
        if not self.running1:
            return
        self.g1_step()
        delay = int(self.speed1.get())
        self.after(delay, self._g1_loop)

    def g1_reset(self):
        if self.state1 is not None:
            self.history1 = []
            self.g1_create()
