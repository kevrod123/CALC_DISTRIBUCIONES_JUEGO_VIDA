# main.py
import tkinter as tk
from tkinter import ttk
from ventanas_generadores import VentanaGeneradores
from ventanas_pruebas import VentanaPruebas
from ventanas_variables import VentanaVariables
from ventanas_distribuciones import VentanaDistribuciones
from simulador_vida import VentanaVida
from simulador_covid import VentanaCovid

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador Interactivo + Generadores Pseudoaleatorios")
        self.geometry("520x520")
        self.resizable(False, False)

        ttk.Label(self, text="Seleccione una opción", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self, text="Generadores de Números Pseudoaleatorios", width=40, command=self.abrir_generadores).pack(pady=8)
        ttk.Button(self, text="Distribuciones Aleatorias (con tus generadores)", width=40, command=self.abrir_distribuciones).pack(pady=8)
        ttk.Button(self, text="Juego de la Vida (1D / 2D)", width=40, command=self.abrir_vida).pack(pady=8)
        ttk.Button(self, text="Simulación tipo COVID-19", width=40, command=self.abrir_covid).pack(pady=8)
        ttk.Button(self, text="Pruebas Estadísticas", width=40, command=self.abrir_pruebas).pack(pady=8)
        ttk.Button(self, text="Historial / Variables", width=40, command=self.abrir_variables).pack(pady=8)

    def abrir_generadores(self): VentanaGeneradores(self)
    def abrir_pruebas(self): VentanaPruebas(self)
    def abrir_variables(self): VentanaVariables(self)
    def abrir_distribuciones(self): VentanaDistribuciones(self)
    def abrir_vida(self): VentanaVida(self)
    def abrir_covid(self): VentanaCovid(self)

if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()
