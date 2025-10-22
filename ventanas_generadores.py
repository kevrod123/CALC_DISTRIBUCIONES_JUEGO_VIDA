# ventanas_generadores.py
import tkinter as tk
from tkinter import ttk
from ventanas import VentanaCuadradosMedios, VentanaProductosMedios, VentanaMultiplicadorConstante

class VentanaGeneradores(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Generadores de Números Pseudoaleatorios")
        self.geometry("600x400")
        self.resizable(False, False)

        ttk.Label(self, text="Seleccione un método", font=("Arial", 14)).pack(pady=20)
        ttk.Button(self, text="Cuadrados Medios", width=30, command=self.abrir_cuadrados_medios).pack(pady=10)
        ttk.Button(self, text="Productos Medios", width=30, command=self.abrir_productos_medios).pack(pady=10)
        ttk.Button(self, text="Multiplicador Constante", width=30, command=self.abrir_multiplicador_constante).pack(pady=10)
        ttk.Button(self, text="Volver atrás", width=15, command=self.destroy).pack(pady=10)

    def abrir_cuadrados_medios(self):
        VentanaCuadradosMedios(self)

    def abrir_productos_medios(self):
        VentanaProductosMedios(self)

    def abrir_multiplicador_constante(self):
        VentanaMultiplicadorConstante(self)
