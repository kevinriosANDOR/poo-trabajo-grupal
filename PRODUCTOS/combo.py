from producto import Producto


class Combo(Producto):
    def __init__(self, nombre, precio, productos):
        super().__init__(nombre, precio)
        self.productos = productos

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def quitar_producto(self, producto):
        self.productos.remove(producto)

    def calcular_precio(self):
        total_precio = sum(producto.calcular_precio() for producto in self.productos)
        return total_precio

    def esta_disponible(self, dia):
        return all(producto.esta_disponible(dia) for producto in self.productos)

    def contar_platos(self):
        total_platos = sum(producto.contar_platos() for producto in self.productos)
        return total_platos
