from bebida import Bebida


class gaseosa(Bebida):
    def __init__(self, nombre, precio, tamaño, gaseosa):
        super().__init__(
            nombre, precio, tamaño, gaseosa=gaseosa, refresco_natural=False
        )

    def calcular_precio(self):
        return super().calcular_precio()
