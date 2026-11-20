from bebida import Bebida


class tamaño_bebida(Bebida):
    def __init__(self, nombre, precio, vaso, jarra):
        super().__init__(nombre, precio, tamaño_bebida=None, gaseosa=False, refresco_natural=False)
        self.vaso = vaso
        self.jarra = jarra
