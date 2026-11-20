from producto import Producto


class Plato(Producto):
    def __init__(self, nombre, precio, dias_venta):
        super().__init__(nombre, precio)
        self.dias_venta = dias_venta

    def calcular_precio(self):
        return super().calcular_precio()

    def esta_disponible(self, dia):
        return dia in self.dias_venta

    def contar_platos(self):
        return super().contar_platos()
