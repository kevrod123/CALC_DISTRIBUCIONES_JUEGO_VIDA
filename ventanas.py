# ventanas.py
import tkinter as tk
from tkinter import ttk, messagebox
from algoritmos import cuadrados_medios, productos_medios, multiplicador_constante
from utils import exportar_a_excel, mostrar_grafico_en_ventana
from historial import guardar_en_historial

class VentanaBase(tk.Toplevel):
    def __init__(self, parent, title, geometry):
        super().__init__(parent)
        self.title(title)
        self.geometry(geometry)

class VentanaCuadradosMedios(VentanaBase):
    def __init__(self, parent):
        super().__init__(parent, "Cuadrados Medios", "900x600")
        self.crear_widgets()

    def crear_widgets(self):
        frame_botones = ttk.Frame(self); frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Exportar a Excel", command=self.exportar_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Volver atrás", command=self.destroy).pack(side=tk.LEFT, padx=5)

        frame_entrada = ttk.Frame(self); frame_entrada.pack(pady=10, fill=tk.X, padx=10)
        ttk.Label(frame_entrada, text="Semilla (X0):").grid(row=0, column=0, padx=5, pady=5)
        self.semilla_entry = ttk.Entry(frame_entrada); self.semilla_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_entrada, text="Iteraciones:").grid(row=0, column=2, padx=5, pady=5)
        self.iter_entry = ttk.Entry(frame_entrada); self.iter_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(frame_entrada, text="Generar", command=self.generar_tabla).grid(row=0, column=4, padx=5, pady=5)

        self.frame_tabla = ttk.Frame(self); self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.frame_grafico = ttk.Frame(self); self.frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def generar_tabla(self):
        try:
            semilla = int(self.semilla_entry.get())
            n = int(self.iter_entry.get())
            tabla = cuadrados_medios(semilla, n)

            for w in self.frame_tabla.winfo_children(): w.destroy()
            for w in self.frame_grafico.winfo_children(): w.destroy()

            columns = ("Iteración", "Xi", "Xi^2", "Xi+1", "ri")
            self.tree = ttk.Treeview(self.frame_tabla, columns=columns, show="headings")
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor=tk.CENTER)
            for fila in tabla:
                i, xi, y_str, xi1, ri = fila
                self.tree.insert("", tk.END, values=(i, xi, y_str, xi1, f"{ri:.4f}"))
            self.tree.pack(fill=tk.BOTH, expand=True)

            guardar_en_historial(tabla, "Cuadrados Medios")
            data = {"Iteración": [f[0] for f in tabla], "ri": [f[4] for f in tabla]}
            mostrar_grafico_en_ventana(self.frame_grafico, data, "Gráfico de ri - Cuadrados Medios", "Iteración", "ri")

        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def exportar_excel(self):
        try:
            semilla = int(self.semilla_entry.get())
            n = int(self.iter_entry.get())
            tabla = cuadrados_medios(semilla, n)
            data = [{"Iteración": f[0], "Xi": f[1], "Resultado": f[2], "Xi+1": f[3], "ri": f[4]} for f in tabla]
            exportar_a_excel(data, "cuadrados_medios.xlsx")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

class VentanaProductosMedios(VentanaBase):
    def __init__(self, parent):
        super().__init__(parent, "Productos Medios", "900x600")
        self.crear_widgets()

    def crear_widgets(self):
        frame_botones = ttk.Frame(self); frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Exportar a Excel", command=self.exportar_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Volver atrás", command=self.destroy).pack(side=tk.LEFT, padx=5)

        frame_entrada = ttk.Frame(self); frame_entrada.pack(pady=10, fill=tk.X, padx=10)
        ttk.Label(frame_entrada, text="X0:").grid(row=0, column=0, padx=5, pady=5)
        self.x0_entry = ttk.Entry(frame_entrada); self.x0_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_entrada, text="X1:").grid(row=0, column=2, padx=5, pady=5)
        self.x1_entry = ttk.Entry(frame_entrada); self.x1_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(frame_entrada, text="Iteraciones:").grid(row=0, column=4, padx=5, pady=5)
        self.iter_entry = ttk.Entry(frame_entrada); self.iter_entry.grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(frame_entrada, text="Generar", command=self.generar_tabla).grid(row=0, column=6, padx=5, pady=5)

        self.frame_tabla = ttk.Frame(self); self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.frame_grafico = ttk.Frame(self); self.frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def generar_tabla(self):
        try:
            x0 = int(self.x0_entry.get())
            x1 = int(self.x1_entry.get())
            n = int(self.iter_entry.get())
            tabla = productos_medios(x0, x1, n)

            for w in self.frame_tabla.winfo_children(): w.destroy()
            for w in self.frame_grafico.winfo_children(): w.destroy()

            columns = ("Iteración", "Xi", "Xi+1", "Xi*Xi+1", "Xi+2", "ri")
            self.tree = ttk.Treeview(self.frame_tabla, columns=columns, show="headings")
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor=tk.CENTER)
            for f in tabla:
                i, xi, xi1, y_str, xi2, ri = f
                self.tree.insert("", tk.END, values=(i, xi, xi1, y_str, xi2, f"{ri:.4f}"))
            self.tree.pack(fill=tk.BOTH, expand=True)

            guardar_en_historial(tabla, "Productos Medios")
            data = {"Iteración": [f[0] for f in tabla], "ri": [f[5] for f in tabla]}
            mostrar_grafico_en_ventana(self.frame_grafico, data, "Gráfico de ri - Productos Medios", "Iteración", "ri")
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def exportar_excel(self):
        try:
            x0 = int(self.x0_entry.get())
            x1 = int(self.x1_entry.get())
            n = int(self.iter_entry.get())
            tabla = productos_medios(x0, x1, n)
            data = [{"Iteración": f[0], "Xi": f[1], "Xi+1": f[2], "Resultado": f[3], "Xi+2": f[4], "ri": f[5]} for f in tabla]
            exportar_a_excel(data, "productos_medios.xlsx")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

class VentanaMultiplicadorConstante(VentanaBase):
    def __init__(self, parent):
        super().__init__(parent, "Multiplicador Constante", "900x600")
        self.crear_widgets()

    def crear_widgets(self):
        frame_botones = ttk.Frame(self); frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Exportar a Excel", command=self.exportar_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Volver atrás", command=self.destroy).pack(side=tk.LEFT, padx=5)

        frame_entrada = ttk.Frame(self); frame_entrada.pack(pady=10, fill=tk.X, padx=10)
        ttk.Label(frame_entrada, text="Constante (X0):").grid(row=0, column=0, padx=5, pady=5)
        self.x0_entry = ttk.Entry(frame_entrada); self.x0_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_entrada, text="X1:").grid(row=0, column=2, padx=5, pady=5)
        self.x1_entry = ttk.Entry(frame_entrada); self.x1_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(frame_entrada, text="Iteraciones:").grid(row=0, column=4, padx=5, pady=5)
        self.iter_entry = ttk.Entry(frame_entrada); self.iter_entry.grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(frame_entrada, text="Generar", command=self.generar_tabla).grid(row=0, column=6, padx=5, pady=5)

        self.frame_tabla = ttk.Frame(self); self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.frame_grafico = ttk.Frame(self); self.frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def generar_tabla(self):
        try:
            x0 = int(self.x0_entry.get())
            x1 = int(self.x1_entry.get())
            n = int(self.iter_entry.get())
            tabla = multiplicador_constante(x0, x1, n)

            for w in self.frame_tabla.winfo_children(): w.destroy()
            for w in self.frame_grafico.winfo_children(): w.destroy()

            columns = ("Iteración", "Xi", "Xi+1", "Xi*Xi+1", "Xi+2", "ri")
            self.tree = ttk.Treeview(self.frame_tabla, columns=columns, show="headings")
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor=tk.CENTER)
            for f in tabla:
                i, xi, xi1, y_str, xi2, ri = f
                self.tree.insert("", tk.END, values=(i, xi, xi1, y_str, xi2, f"{ri:.4f}"))
            self.tree.pack(fill=tk.BOTH, expand=True)

            guardar_en_historial(tabla, "Multiplicador Constante")
            data = {"Iteración": [f[0] for f in tabla], "ri": [f[5] for f in tabla]}
            mostrar_grafico_en_ventana(self.frame_grafico, data, "Gráfico de ri - Multiplicador Constante", "Iteración", "ri")
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def exportar_excel(self):
        try:
            x0 = int(self.x0_entry.get())
            x1 = int(self.x1_entry.get())
            n = int(self.iter_entry.get())
            tabla = multiplicador_constante(x0, x1, n)
            data = [{"Iteración": f[0], "Xi": f[1], "Xi+1": f[2], "Resultado": f[3], "Xi+2": f[4], "ri": f[5]} for f in tabla]
            exportar_a_excel(data, "multiplicador_constante.xlsx")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")
