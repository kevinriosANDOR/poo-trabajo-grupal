from modelo.pagos import PagoEfectivo, PagoQR, PagoTarjeta
from modelo.productos import Combo, Gaseosa, Plato, RefrescoNatural
from restaurante import Restaurante
from modelo.clientes import Cliente


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
