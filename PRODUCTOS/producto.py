class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def calcular_precio(self):
        return self.precio

    def contar_platos(self):
        return 1


def __getattr__(nombre):
    modulos = {
        "Plato": ("plato", "Plato"),
        "Bebida": ("bebida", "Bebida"),
        "tamaño_bebida": ("tamano_bebida", "tamaño_bebida"),
        "gaseosa": ("gaseosa", "gaseosa"),
        "refresco_natural": ("refresco_natural", "refresco_natural"),
        "Combo": ("combo", "Combo"),
        "Item_Pedido": ("item_pedido", "Item_Pedido"),
    }

    if nombre not in modulos:
        raise AttributeError(f"El modulo no tiene el atributo {nombre}")

    nombre_modulo, nombre_clase = modulos[nombre]
    modulo = __import__(nombre_modulo, fromlist=[nombre_clase])
    clase = getattr(modulo, nombre_clase)
    globals()[nombre] = clase
    return clase
