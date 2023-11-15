import tkinter as tk
from controller.method_controller import Controlador
from model.graphic_method import Graphicmethod
from view.method_view import Vista

if __name__ == "__main__":
    root = tk.Tk()
    modelo = Graphicmethod()
    vista = Vista(root)
    controlador = Controlador(modelo, vista)
    root.mainloop()

