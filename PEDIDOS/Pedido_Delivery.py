class Pedido_Delivery(Pedido):
    def __init__(self, nombre, precio, estado, objetos, cliente, zona, pedido_gratis, pedido_minimo):
        super().__init__(nombre, precio, estado, objetos, cliente)
        self.zona = zona
        self.pedido_gratis = pedido_gratis
        self.pedido_minimo = pedido_minimo
    def calcular_cargos(self):
        super().calcular_cargos()
        if self.pedido_minimo >= 40:
            if self.zona == "Cercado":
                if self.pedido_gratis >= 150:
                    cargos = 0
                else:
                    cargos = 8
            elif self.zona == "Quillacollo":
                cargos = 15
            elif self.zona == "Sacaba":
                cargos = 15
            elif self.zona == "Vinto":
                cargos = 20
            else:
                print("Esa zona no es valida")
        else:
            print("no se puede realizar el pedido, el monto minimo es de 40 Bs")
        return cargos