import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
for carpeta in ("PRODUCTOS", "PEDIDOS", "METODO DE PAGO"):
    sys.path.insert(0, str(ROOT / carpeta))

from combo import Combo
from gaseosa import Gaseosa
from pago_efectivo import PagoEfectivo
from pago_qr import PagoQR
from pago_tarjeta import PagoTarjeta
from Pedido_Delivery import Pedido_Delivery
from Pedido_Llevar import Pedido_Llevar
from Pedido_Local import Pedido_Local
from plato import Plato
from refresco_natural import RefrescoNatural
from modelo.clientes import Cliente


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
                    isinstance(pedido, Pedido_Local)
                    and pedido.mesa == int(mesa)
                    and pedido.estado not in (pedido.ENTREGADO, pedido.CANCELADO)
                ):
                    raise ValueError("La mesa ya tiene un pedido abierto")
            nuevo_pedido = Pedido_Local(cliente, mesa, items)
        elif tipo == "llevar":
            nuevo_pedido = Pedido_Llevar(cliente, items)
        elif tipo == "delivery":
            nuevo_pedido = Pedido_Delivery(
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


def crear_restaurante_inicial():
    restaurante = Restaurante()
    platos = [
        Plato("Silpancho", 35, ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]),
        Plato("Pique macho", 45, ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]),
        Plato("Chicharrón", 40, ["domingo"]),
        Plato("Sopa de maní", 25, ["lunes", "martes", "miércoles", "jueves", "viernes"]),
    ]
    bebidas = [
        RefrescoNatural("Mocochinchi", 6, "vaso"),
        RefrescoNatural("Mocochinchi en jarra", 6, "jarra"),
        Gaseosa("Gaseosa", 5, "vaso"),
    ]
    combo = Combo("Combo silpancho y mocochinchi", [platos[0], bebidas[0]])

    for producto in platos + bebidas + [combo]:
        restaurante.agregar_producto(producto)
    return restaurante


def mostrar_menu(restaurante, dia):
    print(f"\n=== MENÚ DISPONIBLE EL {dia.upper()} ===")
    for indice, producto in enumerate(restaurante.menu, start=1):
        if producto.esta_disponible(dia):
            print(f"{indice}. {producto.nombre} - Bs. {producto.calcular_precio():.2f}")


def cobrar_pedido(pedido, dia):
    print(f"Total del pedido: Bs. {pedido.calcular_total(dia):.2f}")
    opcion = input("Pago (1 efectivo, 2 QR, 3 tarjeta): ").strip()
    if opcion == "1":
        metodo = PagoEfectivo(float(input("Monto recibido: Bs. ")))
    elif opcion == "2":
        metodo = PagoQR(input("Código QR de 10 dígitos: ").strip())
    elif opcion == "3":
        metodo = PagoTarjeta(input("Número de tarjeta: ").strip())
    else:
        raise ValueError("Método de pago no válido")
    comprobante = pedido.cobrar(metodo, dia)
    print("Pago aprobado:", comprobante)


def menu_consola():
    restaurante = crear_restaurante_inicial()
    while True:
        print("\n=== SABOR VALLUNO ===")
        print("1. Mostrar menú")
        print("2. Registrar cliente")
        print("3. Crear pedido")
        print("4. Reporte de ventas")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                mostrar_menu(restaurante, input("Día: ").strip())
            elif opcion == "2":
                cliente = Cliente(input("Nombre: "), input("Teléfono: "))
                restaurante.agregar_cliente(cliente)
                print("Cliente registrado correctamente")
            elif opcion == "3":
                if not restaurante.cliente:
                    print("Primero registre un cliente")
                    continue
                for indice, cliente in enumerate(restaurante.cliente, start=1):
                    print(f"{indice}. {cliente}")
                cliente = restaurante.cliente[int(input("Cliente: ")) - 1]
                mostrar_menu(restaurante, "domingo")
                indices = input("Productos separados por coma: ")
                productos = [restaurante.menu[int(indice.strip()) - 1] for indice in indices.split(",")]
                tipo = input("Tipo (local, llevar, delivery): ").strip().lower()
                datos = {}
                if tipo == "local":
                    datos["mesa"] = int(input("Mesa (1-15): "))
                elif tipo == "delivery":
                    datos["zona"] = input("Zona: ").strip()
                pedido = restaurante.crear_pedido(cliente, productos, tipo, **datos)
                pedido.cambiar_estado("EN_PREPARACION")
                pedido.cambiar_estado("LISTO")
                cobrar_pedido(pedido, "domingo")
                pedido.entregar()
            elif opcion == "4":
                print(restaurante.reporte_ventastas("domingo"))
            elif opcion == "5":
                break
            else:
                print("Opción no válida")
        except (ValueError, IndexError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    menu_consola()
