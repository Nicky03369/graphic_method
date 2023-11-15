from model.graphic_method import Graphicmethod
from view.method_view import Vista


class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def solve_button(self):
        self.vista.button_solve["command"] = self.exec_method()

    def exec_method(self):
        self.modelo.find_points(self.vista.constraint_list)
        self.modelo.find_intersections(self.vista.constraint_list)
        self.modelo.find_closest_intersections()
        self.modelo.find_closest_points()
        vortex = self.modelo.get_vortex()
        x, y = self.modelo.get_x_y()
        intersections = self.modelo.get_intersections()
        self.vista.plot_graphic_method(x, y, vortex, intersections)
