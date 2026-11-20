from bebida import Bebida


class RefrescoNatural(Bebida):
    def __init__(self, nombre, precio, tamano):
        super().__init__(
            nombre,
            precio,
            tamano_bebida=tamano,
            gaseosa=False,
            refresco_natural=True,
        )

    def calcular_precio(self):
        return super().calcular_precio()

refresco_natural = RefrescoNatural
