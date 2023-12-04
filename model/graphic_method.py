from pulp import LpProblem, LpVariable, value, LpMinimize, LpMaximize


class Graphicmethod:
    def __init__(self):
        self.x = []
        self.y = []
        self.intersections = []
        self.closest_x_intersection = tuple()
        self.closest_y_intersection = tuple()
        self.closest_x = tuple()
        self.closest_y = tuple()

    def find_points(self, constraints):
        for constraint in constraints:
            coeff_a = constraint["X"]
            coeff_b = constraint["Y"]
            coeff_c = constraint["C"]

            if coeff_a == 0:
                y_val = coeff_c / coeff_b
                self.x.append(0)
                self.y.append(y_val)
            elif coeff_b == 0:
                x_val = coeff_c / coeff_a
                self.x.append(x_val)
                self.y.append(0)
            else:
                x1 = 0
                y1 = coeff_c / coeff_b
                x2 = coeff_c / coeff_a
                y2 = 0
                self.x.extend([x1, x2])
                self.y.extend([y1, y2])

    def find_intersections(self, constraints):
        for i in range(len(constraints)):
            for j in range(i + 1, len(constraints)):
                A1 = constraints[i]["X"]
                B1 = constraints[i]["Y"]
                C1 = constraints[i]["C"]
                A2 = constraints[j]["X"]
                B2 = constraints[j]["Y"]
                C2 = constraints[j]["C"]

                det = A1 * B2 - A2 * B1

                if det != 0:
                    x_val = (C1 * B2 - C2 * B1) / det
                    y_val = (A1 * C2 - A2 * C1) / det
                    self.intersections.append((x_val, y_val))

    def find_closest_intersections(self):
        # Encontrar la intersección más cercana al eje x
        self.closest_x_intersection = min(self.intersections, key=lambda p: abs(p[1]))

        # Encontrar la intersección más cercana al eje y
        self.closest_y_intersection = min(self.intersections, key=lambda p: abs(p[0]))

    def find_closest_points(self):
        self.closest_x = (min(self.x, key=lambda val: abs(val) if val != 0 else float('inf')), 0)
        self.closest_y = (0, min(self.y, key=lambda val: abs(val) if val != 0 else float('inf')))

    def get_lines(self, constraints):
        for constraint in constraints:
            coeff_a = constraint["Coeff A"]
            coeff_b = constraint["Coeff B"]
            coeff_c = constraint["Coeff C"]
            equal = constraint["Equal"]

            if coeff_b == 0:
                x_vals = [coeff_c / coeff_a, coeff_c / coeff_a]
                y_vals = [min(self.y), max(self.y)]
            else:
                x_vals = [min(self.x), max(self.x)]
                y_vals = [(coeff_c - coeff_a * x) / coeff_b for x in x_vals]

            return x_vals, y_vals

    def get_vortex(self):
        vertices = [
            (0, 0),
            self.closest_x,
            self.closest_x_intersection,
            self.closest_y_intersection,
            self.closest_y
        ]
        return vertices

    def get_x_y(self):
        return self.x, self.y

    def get_intersections(self):
        return self.intersections

    def get_ordinal(self, number):
        if 10 <= number % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
        return f"{number}{suffix}"

    def find_solution(self, option, func_obj, constraints):
        print(f"OPCION SELECCIONADA {option}")
        print(func_obj)
        print(constraints)

        if func_obj.get('Objective', None) == 'maximize':
            problem = LpProblem("GM_problem", LpMaximize)
            x1 = LpVariable("x1", 0)
            x2 = LpVariable("x2", 0)
            problem += func_obj['X'] * x1 + func_obj['Y'] * x2

            for index, constraint in enumerate(constraints, start=1):
                x_coeff = constraint['X']
                y_coeff = constraint['Y']
                equality = constraint['Equal']
                constant = constraint['C']

                constraint_name = f"{self.get_ordinal(index)} constraint"
                if equality == '=':
                    problem += x_coeff * x1 + y_coeff * x2 == constant, constraint_name
                elif equality == '>=':
                    problem += x_coeff * x1 + y_coeff * x2 >= constant, constraint_name
                elif equality == '<=':
                    problem += x_coeff * x1 + y_coeff * x2 <= constant, constraint_name
            problem.solve()
            message = ""
            for v in problem.variables():
                message += f"{v.name} = {v.varValue} \n"
            message += f"The optimal value of the objective function is = {value(problem.objective)} "
            return message
        elif func_obj.get('Objective', None) == 'minimize':
            problem = LpProblem("GM_problem", LpMinimize)
            x1 = LpVariable("x1", 0)
            x2 = LpVariable("x2", 0)
            problem += func_obj['X'] * x1 + func_obj['Y'] * x2

            for index, constraint in enumerate(constraints, start=1):
                x_coeff = constraint['X']
                y_coeff = constraint['Y']
                equality = constraint['Equal']
                constant = constraint['C']

                constraint_name = f"{self.get_ordinal(index)} constraint"
                if equality == '=':
                    problem += x_coeff * x1 + y_coeff * x2 == constant, constraint_name
                elif equality == '>=':
                    problem += x_coeff * x1 + y_coeff * x2 >= constant, constraint_name
                elif equality == '<=':
                    problem += x_coeff * x1 + y_coeff * x2 <= constant, constraint_name
            problem.solve()
            message = ""
            for v in problem.variables():
                message += f"{v.name} = {v.varValue} \n"
            message += f"The optimal value of the objective function is = {value(problem.objective)} "
            return message
        else:
            return "NO SE SOLUCIONO"
