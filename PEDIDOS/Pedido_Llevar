class Pedido_Llevar(Pedido):
    def __init__(self, nombre, precio, estado, objetos, cliente, cantidad_envase):
        super().__init__(nombre, precio, estado, objetos, cliente)
        self.cantidad_envase = cantidad_envase
    def calcular_cargos(self):
        super().calcular_cargos()
        cargos= self.cantidad_envase * 2
        return cargos