from abc import ABC, abstractmethod
from math import ceil


class Producto(ABC):
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self.precio = precio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not str(valor).strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        self._nombre = str(valor).strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        valor = float(valor)
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        self._precio = round(valor, 2)

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass

    def precio_para_cantidad(self, cantidad, dia=None):
        if not 1 <= int(cantidad) <= 20:
            raise ValueError("La cantidad debe estar entre 1 y 20")
        return round(self.calcular_precio() * int(cantidad), 2)

    def productos_contenidos(self):
        return [self]


class Plato(Producto):
    def __init__(self, nombre, precio, dias_venta):
        super().__init__(nombre, precio)
        if not dias_venta:
            raise ValueError("Un plato debe tener al menos un día de venta")
        self._dias_venta = {str(dia).strip().lower() for dia in dias_venta}

    @property
    def dias_venta(self):
        return tuple(sorted(self._dias_venta))

    def calcular_precio(self):
        return self.precio

    def esta_disponible(self, dia):
        return str(dia).strip().lower() in self._dias_venta

    def contar_platos(self):
        return 1


class Bebida(Producto):
    def __init__(self, nombre, precio_vaso, tamano="vaso"):
        super().__init__(nombre, precio_vaso)
        tamano = str(tamano).strip().lower()
        if tamano not in ("vaso", "jarra"):
            raise ValueError("El tamaño debe ser vaso o jarra")
        self._tamano = tamano

    @property
    def tamano(self):
        return self._tamano

    def calcular_precio(self):
        return round(self.precio * (3 if self.tamano == "jarra" else 1), 2)

    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0

    def es_refresco_natural(self):
        return False

    def precio_para_cantidad(self, cantidad, dia=None):
        if not 1 <= int(cantidad) <= 20:
            raise ValueError("La cantidad debe estar entre 1 y 20")
        cantidad = int(cantidad)
        precio_unitario = self.calcular_precio()
        martes = str(dia).strip().lower() == "martes" if dia else False
        if self.es_refresco_natural() and self.tamano == "vaso" and martes:
            return round(ceil(cantidad / 2) * precio_unitario, 2)
        return round(precio_unitario * cantidad, 2)


class RefrescoNatural(Bebida):
    def es_refresco_natural(self):
        return True


class Gaseosa(Bebida):
    pass


class Combo(Producto):
    DESCUENTO_VARIANTE_B = 0.12

    def __init__(self, nombre, productos):
        if len(productos) < 2:
            raise ValueError("Un combo debe contener al menos 2 productos")
        super().__init__(nombre, 0.01)
        self._productos = []
        for producto in productos:
            self.agregar_producto(producto)

    @property
    def productos(self):
        return tuple(self._productos)

    def agregar_producto(self, producto):
        if producto is self:
            raise ValueError("Un combo no puede contenerse a sí mismo")
        if not hasattr(producto, "calcular_precio"):
            raise TypeError("El combo solo acepta productos")
        self._productos.append(producto)
        self._precio = self.calcular_precio()

    def quitar_producto(self, producto):
        if len(self._productos) <= 2:
            raise ValueError("Un combo debe conservar al menos 2 productos")
        self._productos.remove(producto)
        self._precio = self.calcular_precio()

    def calcular_precio(self):
        subtotal = sum(producto.calcular_precio() for producto in self._productos)
        return round(subtotal * (1 - self.DESCUENTO_VARIANTE_B), 2)

    def esta_disponible(self, dia):
        return all(producto.esta_disponible(dia) for producto in self._productos)

    def contar_platos(self):
        return sum(producto.contar_platos() for producto in self._productos)

    def productos_contenidos(self):
        productos = []
        for producto in self._productos:
            productos.extend(producto.productos_contenidos())
        return productos
