# simulador_covid.py (versión mejorada y coloreada)
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap


class VentanaCovid(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("🦠 Simulación tipo COVID-19 (Versión mejorada)")
        self.geometry("1000x720")
        self.configure(bg="#222831")

        # Estilo visual uniforme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#222831")
        style.configure("TLabel", background="#222831", foreground="white", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TLabelframe", background="#393E46", foreground="white", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", background="#393E46", foreground="white")

        # ======== Panel de controles ========
        ctrl = ttk.LabelFrame(self, text="Panel de Control")
        ctrl.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(ctrl, text="Filas").grid(row=0, column=0, padx=5)
        self.r = tk.IntVar(value=60)
        ttk.Entry(ctrl, textvariable=self.r, width=6).grid(row=0, column=1)

        ttk.Label(ctrl, text="Columnas").grid(row=0, column=2, padx=5)
        self.c = tk.IntVar(value=60)
        ttk.Entry(ctrl, textvariable=self.c, width=6).grid(row=0, column=3)

        ttk.Label(ctrl, text="Infectados iniciales").grid(row=0, column=4, padx=5)
        self.init_inf = tk.IntVar(value=8)
        ttk.Entry(ctrl, textvariable=self.init_inf, width=6).grid(row=0, column=5)

        ttk.Label(ctrl, text="P(infect)").grid(row=0, column=6, padx=5)
        self.p_inf = tk.DoubleVar(value=0.25)
        ttk.Entry(ctrl, textvariable=self.p_inf, width=6).grid(row=0, column=7)

        ttk.Label(ctrl, text="P(recuperar)").grid(row=0, column=8, padx=5)
        self.p_rec = tk.DoubleVar(value=0.03)
        ttk.Entry(ctrl, textvariable=self.p_rec, width=6).grid(row=0, column=9)

        ttk.Label(ctrl, text="P(morir)").grid(row=0, column=10, padx=5)
        self.p_die = tk.DoubleVar(value=0.01)
        ttk.Entry(ctrl, textvariable=self.p_die, width=6).grid(row=0, column=11)

        ttk.Button(ctrl, text="🧬 Crear", command=self.cv_create).grid(row=0, column=12, padx=5)
        ttk.Button(ctrl, text="⏩ Paso", command=self.cv_step).grid(row=0, column=13, padx=5)
        self.btn_run = ttk.Button(ctrl, text="▶ Ejecutar", command=self.cv_toggle)
        self.btn_run.grid(row=0, column=14, padx=5)
        ttk.Button(ctrl, text="⟳ Reiniciar", command=self.cv_reset).grid(row=0, column=15, padx=5)

        # ======== Segunda fila de controles ========
        ttk.Label(ctrl, text="Velocidad (ms)").grid(row=1, column=0, padx=5, pady=6)
        self.speed = tk.DoubleVar(value=150)
        tk.Scale(ctrl, variable=self.speed, from_=50, to=500, orient="horizontal", length=150,
                 bg="#393E46", fg="white", troughcolor="#00ADB5").grid(row=1, column=1, columnspan=3, padx=5)

        ttk.Label(ctrl, text="Esquema de color").grid(row=1, column=4, padx=5)
        self.color_scheme = tk.StringVar(value="turquesa")
        self.cb_color = ttk.Combobox(ctrl, textvariable=self.color_scheme,
                                     values=["turquesa", "calor", "frío", "monocromo"],
                                     width=10, state="readonly")
        self.cb_color.grid(row=1, column=5, padx=5)

        # ======== Estadísticas ========
        stats_frame = ttk.LabelFrame(self, text="Estadísticas en tiempo real")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        self.lbl_stats = ttk.Label(stats_frame, text="Esperando simulación...")
        self.lbl_stats.pack(padx=10, pady=5)

        # ======== Gráficos ========
        self.fig = plt.Figure(figsize=(8, 6), facecolor="#222831")
        self.ax_grid = self.fig.add_subplot(211)
        self.ax_chart = self.fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.grid = None
        self.t = 0
        self.running = False
        self.hist = []

    # ======== Creación inicial ========
    def cv_create(self):
        rows = max(5, int(self.r.get()))
        cols = max(5, int(self.c.get()))
        self.grid = np.ones((rows, cols), dtype=int)  # 1 = susceptible
        self.t = 0
        self.hist = []
        rng = np.random.default_rng()
        for _ in range(int(self.init_inf.get())):
            r = rng.integers(0, rows)
            c = rng.integers(0, cols)
            self.grid[r, c] = 2  # infectado
        self._cv_draw()

    # ======== Contador de estados ========
    def _counts(self):
        u, cnt = np.unique(self.grid, return_counts=True)
        d = {k: 0 for k in range(5)}
        for k, c in zip(u, cnt):
            d[int(k)] = int(c)
        return d

    # ======== Paso de simulación ========
    def cv_step(self):
        if self.grid is None:
            self.cv_create()

        rows, cols = self.grid.shape
        new = self.grid.copy()
        pinf = float(self.p_inf.get())
        prec = float(self.p_rec.get())
        pdie = float(self.p_die.get())

        for r in range(rows):
            for c in range(cols):
                st = self.grid[r, c]
                if st == 1:  # susceptible
                    neigh = self.grid[max(0, r - 1):r + 2, max(0, c - 1):c + 2]
                    infected = np.sum(neigh == 2)
                    if infected > 0:
                        p = 1 - ((1 - pinf) ** infected)
                        if np.random.random() < p:
                            new[r, c] = 2
                elif st == 2:  # infectado
                    u = np.random.random()
                    if u < pdie:
                        new[r, c] = 4  # muerto
                    elif u < pdie + prec:
                        new[r, c] = 3  # recuperado

        self.grid = new
        self.t += 1
        self._cv_draw()

    # ======== Dibujo ========
    def _cv_draw(self):
        self.ax_grid.clear()
        scheme = self.color_scheme.get()

        # Colormap dinámico
        if scheme == "turquesa":
            cmap = ListedColormap(["#1E1E1E", "#00ADB5", "#FF5722", "#8BC34A", "#444444"])
        elif scheme == "calor":
            cmap = ListedColormap(["black", "#ffcc80", "#ff5722", "#ffeb3b", "#6d4c41"])
        elif scheme == "frío":
            cmap = ListedColormap(["#0d1117", "#90caf9", "#2196f3", "#00e5ff", "#455a64"])
        else:
            cmap = ListedColormap(["white", "gray", "red", "green", "black"])

        self.ax_grid.imshow(self.grid, interpolation="nearest", cmap=cmap, vmin=0, vmax=4)
        self.ax_grid.set_title(f"Simulación COVID-19 — Paso {self.t}", color="white")
        self.ax_grid.axis("off")

        # Actualizar estadísticas
        self.hist.append(self._counts())
        counts = self.hist[-1]
        stats_text = (
            f"🧍 Susceptibles: {counts[1]}   🧫 Infectados: {counts[2]}   "
            f"💊 Recuperados: {counts[3]}   ⚰️ Muertos: {counts[4]}"
        )
        self.lbl_stats.config(text=stats_text)

        # Gráfico de líneas
        times = list(range(len(self.hist)))
        s = [h[1] for h in self.hist]
        i = [h[2] for h in self.hist]
        r = [h[3] for h in self.hist]
        d = [h[4] for h in self.hist]

        self.ax_chart.clear()
        self.ax_chart.plot(times, s, color="#00E0A1", label="Susceptibles")
        self.ax_chart.plot(times, i, color="#FF5722", label="Infectados")
        self.ax_chart.plot(times, r, color="#8BC34A", label="Recuperados")
        self.ax_chart.plot(times, d, color="#9E9E9E", label="Muertos")
        self.ax_chart.set_facecolor("#222831")
        self.ax_chart.legend(facecolor="#393E46", edgecolor="white", labelcolor="white")
        self.ax_chart.tick_params(colors="white")
        self.ax_chart.set_xlabel("Tiempo", color="white")
        self.ax_chart.set_ylabel("Población", color="white")

        self.canvas.draw()

    # ======== Ejecutar / Pausar ========
    def cv_toggle(self):
        if self.grid is None:
            self.cv_create()
        self.running = not self.running
        self.btn_run.config(text="⏸️ Pausar" if self.running else "▶ Ejecutar")
        if self.running:
            self._loop()

    # ======== Bucle de simulación ========
    def _loop(self):
        if not self.running:
            return
        self.cv_step()
        delay = int(self.speed.get())
        self.after(delay, self._loop)

    # ======== Reinicio ========
    def cv_reset(self):
        if self.grid is not None:
            self.cv_create()
            self.lbl_stats.config(text="Simulación reiniciada ✅")
