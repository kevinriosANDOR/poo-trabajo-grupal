class Pedido_Local(Pedido):
    def __init__(self, nombre, precio, estado, objetos, cliente, mesa):
        super().__init__(nombre, precio, estado, objetos, cliente)
        self.mesa = mesa
    def calcular_cargos(self):
        super().calcular_cargos()
        return 0