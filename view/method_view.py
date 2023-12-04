import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from model.graphic_method import Graphicmethod


class Vista:
    def __init__(self, root):
        self.modelo = Graphicmethod()
        self.root = root
        self.root.title("Metodo Grafico")
        self.root.geometry("400x600")  # Establece el tamaño de la ventana a 400x300 píxeles
        self.label_funcobj = tk.Label(root, text="Ingrese la Funcion Objetivo Z=")
        self.label_funcobj.pack()
        frame = tk.Frame(root)
        frame.pack(pady=10)

        self.label_a = tk.Label(frame, text="A:")
        self.label_a.pack(side=tk.LEFT)
        self.txtfield_a = tk.Entry(frame)
        self.txtfield_a.configure(width=4)
        self.txtfield_a.pack(side=tk.LEFT)

        self.sign = ttk.Combobox(frame, values=["+", "-"], state="readonly")
        self.sign.configure(width=3)
        self.sign.pack(side=tk.LEFT, padx=5)  # Añade espacio entre el Combobox y los campos de entrada

        self.label_b = tk.Label(frame, text="B:")
        self.label_b.pack(side=tk.LEFT)
        self.txtfield_b = tk.Entry(frame)
        self.txtfield_b.configure(width=4)
        self.txtfield_b.pack(side=tk.LEFT)

        self.objective_var = tk.StringVar(value="maximize")  # Inicialmente, se establece en "maximizar"
        tk.Label(root, text="Objetivo:").pack()
        maximize_radio = tk.Radiobutton(root, text="Maximizar", variable=self.objective_var, value="maximize")
        maximize_radio.pack()
        minimize_radio = tk.Radiobutton(root, text="Minimizar", variable=self.objective_var, value="minimize")
        minimize_radio.pack()

        self.button_add_restriction = tk.Button(root, text="Añadir Restricción", command=self.open_restriction_window)
        self.button_add_restriction.pack()

        self.label_restricciones = tk.Label(root, text="Restricciones:")
        self.label_restricciones.pack()

        frame_table = tk.Frame(root, width=300, height=200)
        frame_table.pack()  # Expande el Frame al tamaño de la ventana

        self.tree = ttk.Treeview(frame_table, columns=("Coeff A", "Signo", "Coeff B", "Equal", "Coeff C"),
                                 show="headings")
        self.tree.heading("Coeff A", text="Coeff A")
        self.tree.heading("Signo", text="Signo")
        self.tree.heading("Coeff B", text="Coeff B")
        self.tree.heading("Equal", text="Equal")
        self.tree.heading("Coeff C", text="Coeff C")
        self.tree.pack(fill="both", expand=True)  # Expande la tabla

        self.root.bind("<Configure>", self.on_resize)

        self.button_solve = tk.Button(root, text="Resolver",
                                      command=self.plot_graphic_method)  # , command=self.open_restriction_window
        self.button_solve.pack()

        # Lista de restricciones
        self.constraint_list = []

    def on_resize(self, event):
        # Obtener el ancho de la ventana
        window_width = self.root.winfo_width()

        # Ajustar el ancho de las columnas en función del ancho de la ventana
        self.tree.column("Coeff A", width=window_width // 4)
        self.tree.column("Coeff B", width=window_width // 4)
        self.tree.column("Equal", width=window_width // 4)
        self.tree.column("Coeff C", width=window_width // 4)

    def open_restriction_window(self):
        # Crear una ventana emergente para agregar restricciones
        restriction_window = tk.Toplevel(self.root)
        restriction_window.title("Agregar Restricción")

        # Campos de entrada para la restricción
        coeff_a_entry = tk.Entry(restriction_window)
        coeff_b_entry = tk.Entry(restriction_window)
        sign = ttk.Combobox(restriction_window, values=["+", "-"], state='readonly')

        equal_combobox = ttk.Combobox(restriction_window, values=["=", "<=", ">="], state='readonly')
        coeff_c_entry = tk.Entry(restriction_window)

        coeff_a_entry.grid(row=0, column=1)
        sign.grid(row=1, column=1)
        coeff_b_entry.grid(row=2, column=1)
        equal_combobox.grid(row=3, column=1)
        coeff_c_entry.grid(row=4, column=1)

        tk.Label(restriction_window, text="Coeff A:").grid(row=0, column=0)
        tk.Label(restriction_window, text="Signo:").grid(row=1, column=0)
        tk.Label(restriction_window, text="Coeff B:").grid(row=2, column=0)
        tk.Label(restriction_window, text="Equal:").grid(row=3, column=0)
        tk.Label(restriction_window, text="Coeff C:").grid(row=4, column=0)

        # Botón para cargar restricción en la tabla principal
        add_button = tk.Button(restriction_window, text="Añadir a la Tabla",
                               command=lambda: self.add_restriction_to_table(coeff_a_entry.get(), coeff_b_entry.get(),
                                                                             equal_combobox.get(), coeff_c_entry.get(),
                                                                             sign.get(), restriction_window))
        add_button.grid(row=5, column=0, columnspan=2)

    def add_restriction_to_table(self, coeff_a, coeff_b, equal, coeff_c, sign, window):
        if not coeff_a or not coeff_b or not equal or not coeff_c or not sign:
            self.show_rest_error("Todos los campos deben estar llenos")
        else:
            # Agregar los valores a la tabla
            constraint = {
                "X": float(coeff_a),
                "Sign": sign,
                "Y": float(coeff_b),
                "Equal": equal,
                "C": float(coeff_c)
            }
            self.constraint_list.append(constraint)
            self.tree.insert("", "end", values=(coeff_a, sign, coeff_b, equal, coeff_c))
            # Cerrar la ventana emergente
            window.destroy()

    def show_rest_error(self, message):
        # Crear una ventana emergente para mostrar el mensaje de error
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        tk.Label(error_window, text=message).pack()
        tk.Button(error_window, text="Cerrar", command=error_window.destroy).pack()

    def update_table(self):
        # Borrar todas las filas actuales en la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Agregar restricciones de la lista a la tabla
        for constraint in self.constraint_list:
            self.tree.insert("", "end",
                             values=(constraint.coeff_a, constraint.coeff_b, constraint.equal, constraint.coeff_c))

    def get_objective_func(self):
        objective = self.objective_var.get()
        coeff_a = int(self.txtfield_a.get())
        coeff_b = int(self.txtfield_b.get())
        sign = self.sign.get()
        func_obj = {
            "Objective": objective,
            "X": coeff_a,
            "Y": coeff_b,
            "Sign": sign
        }
        return func_obj

    def plot_graphic_method(self):
        self.modelo.find_points(self.constraint_list)
        self.modelo.find_intersections(self.constraint_list)
        self.modelo.find_closest_intersections()
        self.modelo.find_closest_points()
        vortex = self.modelo.get_vortex()
        x, y = self.modelo.get_x_y()
        intersections = self.modelo.get_intersections()
        for constraint in self.constraint_list:
            coeff_a = constraint["X"]
            sign = constraint["Sign"]
            coeff_b = constraint["Y"]
            coeff_c = constraint["C"]
            equal = constraint["Equal"]

            if coeff_b == 0:
                x_vals = [coeff_c / coeff_a, coeff_c / coeff_a]
                y_vals = [min(y), max(y)]
            else:
                x_vals = [min(x), max(x)]
                y_vals = [(coeff_c - coeff_a * x) / coeff_b for x in x_vals]

            plt.plot(x_vals, y_vals, label=f'{coeff_a}x {sign} {coeff_b}y {equal} {coeff_c}')
            plt.scatter(x_vals, y_vals, color='red', marker='o')  # Marcar puntos de las rectas
        intersection_x, intersection_y = zip(*intersections)
        plt.scatter(intersection_x, intersection_y, marker='x')
        polygon = plt.Polygon(vortex, closed=True, color='gray', alpha=0.5)
        plt.gca().add_patch(polygon)
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.legend()

        plt.grid(True)
        self.show_solved_window()
        plt.show()


    def get_max_min_selection(self):
        selected_value = self.objective_var.get()
        if selected_value == 'maximize':
            return selected_value
        elif selected_value == 'minimize':
            return selected_value

    def show_solved_window(self):
        resolved_window = tk.Toplevel(self.root)
        option = self.get_max_min_selection()
        message = self.modelo.find_solution(option, self.get_objective_func(), self.constraint_list)
        resolved_label = tk.Label(resolved_window, text=message)
        resolved_label.pack()
