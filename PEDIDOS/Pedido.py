class Pedido(Producto):
    def __init__(self, nombre, precio, estado, objetos, cliente):
        super().__init__(nombre, precio)
        self.estado = estado
        self.objetos = objetos
        self.cliente = cliente
    def agregar_producto(self, producto):
        self.objetos.append(producto)
    def quitar_producto(self, producto):
        self.objetos.remove(producto)
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
    def calcular_total(self):
        total = 0
        for producto in self.objetos:
            total += producto.precio
        return total
    def calcular_cargos(self):
        return 