from abc import ABC, abstractmethod

from modelo.clientes import Cliente
from modelo.pagos import MetodoPago
from modelo.productos import Producto


class ItemPedido:
    def __init__(self, producto, cantidad=1):
        if not isinstance(producto, Producto):
            raise TypeError("El ítem debe contener un producto")
        if not 1 <= int(cantidad) <= 20:
            raise ValueError("La cantidad debe estar entre 1 y 20")
        self._producto = producto
        self._cantidad = int(cantidad)

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    def subtotal(self, dia=None):
        return self.producto.precio_para_cantidad(self.cantidad, dia)


class Pedido(ABC):
    REGISTRADO = "REGISTRADO"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

    _TRANSICIONES = {
        REGISTRADO: {EN_PREPARACION, CANCELADO},
        EN_PREPARACION: {LISTO},
        LISTO: {ENTREGADO},
        ENTREGADO: set(),
        CANCELADO: set(),
    }

    def __init__(self, cliente, items=None):
        if not isinstance(cliente, Cliente):
            raise TypeError("El pedido debe tener un cliente válido")
        self._cliente = cliente
        self._items = []
        self._estado = self.REGISTRADO
        self._pago = None
        for producto, cantidad in items or []:
            self.agregar_producto(producto, cantidad)

    @property
    def cliente(self):
        return self._cliente

    @property
    def estado(self):
        return self._estado

    @property
    def items(self):
        return tuple(self._items)

    @property
    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def calcular_cargos(self, dia=None):
        pass

    def agregar_producto(self, producto, cantidad=1):
        if self.estado != self.REGISTRADO:
            raise ValueError("Solo se agregan productos en estado REGISTRADO")
        self._items.append(ItemPedido(producto, cantidad))

    def quitar_producto(self, producto):
        if self.estado != self.REGISTRADO:
            raise ValueError("Solo se quitan productos en estado REGISTRADO")
        for indice, item in enumerate(self._items):
            if item.producto is producto:
                self._items.pop(indice)
                return
        raise ValueError("El producto no está en el pedido")

    def cambiar_estado(self, nuevo_estado):
        nuevo_estado = str(nuevo_estado).upper()
        permitidos = self._TRANSICIONES[self.estado]
        if nuevo_estado not in permitidos:
            raise ValueError(
                f"No se puede pasar de {self.estado} a {nuevo_estado}"
            )
        self._estado = nuevo_estado

    def calcular_subtotal(self, dia=None):
        return round(sum(item.subtotal(dia) for item in self._items), 2)

    def calcular_total(self, dia=None):
        return round(self.calcular_subtotal(dia) + self.calcular_cargos(dia), 2)

    def permite_metodo_pago(self, metodo):
        return True

    def cobrar(self, metodo, dia=None):
        if not isinstance(metodo, MetodoPago):
            raise TypeError("El cobro requiere un método de pago válido")
        if not self.permite_metodo_pago(metodo):
            raise ValueError("El delivery solo acepta efectivo o QR")
        self._pago = metodo.procesar_pago(self.calcular_total(dia))
        return self._pago

    def entregar(self):
        if self.estado != self.LISTO:
            raise ValueError("Solo se puede entregar un pedido LISTO")
        self.cambiar_estado(self.ENTREGADO)

    def detalle(self, dia=None):
        return {
            "tipo": self.tipo,
            "estado": self.estado,
            "subtotal": self.calcular_subtotal(dia),
            "cargos": self.calcular_cargos(dia),
            "total": self.calcular_total(dia),
        }


class PedidoLocal(Pedido):
    def __init__(self, cliente, mesa, items=None):
        mesa = int(mesa)
        if not 1 <= mesa <= 15:
            raise ValueError("La mesa debe estar entre 1 y 15")
        self._mesa = mesa
        super().__init__(cliente, items)

    @property
    def tipo(self):
        return "local"

    @property
    def mesa(self):
        return self._mesa

    def calcular_cargos(self, dia=None):
        return 0


class PedidoLlevar(Pedido):
    COSTO_ENVASE = 2.50

    @property
    def tipo(self):
        return "llevar"

    def calcular_cargos(self, dia=None):
        platos = sum(
            item.producto.contar_platos() * item.cantidad for item in self.items
        )
        return round(platos * self.COSTO_ENVASE, 2)


class PedidoDelivery(Pedido):
    TARIFAS = {
        "Cercado": 8,
        "Quillacollo": 15,
        "Sacaba": 15,
        "Vinto": 20,
    }
    PEDIDO_MINIMO = 50
    ENVIO_GRATIS_DESDE = 120

    def __init__(self, cliente, zona, items=None):
        if zona not in self.TARIFAS:
            raise ValueError("La zona de delivery no es válida")
        self._zona = zona
        super().__init__(cliente, items)

    @property
    def tipo(self):
        return "delivery"

    @property
    def zona(self):
        return self._zona

    def calcular_cargos(self, dia=None):
        subtotal = self.calcular_subtotal(dia)
        if subtotal < self.PEDIDO_MINIMO:
            raise ValueError("El pedido mínimo de delivery es Bs 50")
        if subtotal >= self.ENVIO_GRATIS_DESDE:
            return 0
        return self.TARIFAS[self.zona]

    def permite_metodo_pago(self, metodo):
        return metodo.permite_delivery

