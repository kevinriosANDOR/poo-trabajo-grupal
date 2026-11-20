from producto import Producto


class Bebida(Producto):
    def __init__(self, nombre, precio, tamano_bebida, gaseosa, refresco_natural):
        super().__init__(nombre, precio)
        self.tamano_bebida = tamano_bebida
        self.gaseosa = gaseosa
        self.refresco_natural = refresco_natural
