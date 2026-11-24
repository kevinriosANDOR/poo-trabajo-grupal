from collections import Counter, defaultdict

from modelo.clientes import Cliente
from modelo.pedidos import PedidoDelivery, PedidoLlevar, PedidoLocal


class Restaurante:
    def __init__(self):
        self.cliente = []
        self.menu = []
        self.pedido = []

    def agregar_producto(self, producto):
        self.menu.append(producto)

    def agregar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise TypeError("Se debe agregar un objeto Cliente")
        self.cliente.append(cliente)

    def crear_pedido(self, cliente, productos, tipo="local", **datos):
        if cliente not in self.cliente:
            raise ValueError("El cliente debe estar registrado")
        if not productos:
            raise ValueError("El pedido debe tener al menos un producto")

        items = []
        for elemento in productos:
            if isinstance(elemento, tuple):
                producto, cantidad = elemento
            else:
                producto, cantidad = elemento, 1
            if producto not in self.menu:
                raise ValueError("El producto debe estar en el menú")
            items.append((producto, cantidad))

        tipo = str(tipo).lower()
        if tipo == "local":
            mesa = datos.get("mesa", 1)
            for pedido in self.pedido:
                if (
                    isinstance(pedido, PedidoLocal)
                    and pedido.mesa == int(mesa)
                    and pedido.estado not in (pedido.ENTREGADO, pedido.CANCELADO)
                ):
                    raise ValueError("La mesa ya tiene un pedido abierto")
            nuevo_pedido = PedidoLocal(cliente, mesa, items)
        elif tipo == "llevar":
            nuevo_pedido = PedidoLlevar(cliente, items)
        elif tipo == "delivery":
            nuevo_pedido = PedidoDelivery(
                cliente, datos.get("zona", "Cercado"), items
            )
        else:
            raise ValueError("El tipo debe ser local, llevar o delivery")

        self.pedido.append(nuevo_pedido)
        return nuevo_pedido

    def reporte_ventastas(self, dia=None):
        ventas_por_tipo = defaultdict(float)
        total_ventas = 0
        productos_vendidos = Counter()

        for pedido in self.pedido:
            total = pedido.calcular_total(dia)
            ventas_por_tipo[pedido.tipo] += total
            total_ventas += total
            for item in pedido.items:
                for producto in item.producto.productos_contenidos():
                    productos_vendidos[producto.nombre] += item.cantidad

        return {
            "cantidad_pedidos": len(self.pedido),
            "ventas_por_tipo": dict(ventas_por_tipo),
            "total_ventas": round(total_ventas, 2),
            "tres_productos_mas_vendidos": productos_vendidos.most_common(3),
        }
