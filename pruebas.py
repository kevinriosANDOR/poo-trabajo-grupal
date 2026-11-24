from modelo.clientes import Cliente
from modelo.pagos import PagoQR, PagoTarjeta
from modelo.pedidos import PedidoDelivery, PedidoLlevar, PedidoLocal
from modelo.productos import Combo, Gaseosa, Plato, RefrescoNatural
from restaurante import Restaurante


def debe_fallar(funcion):
    try:
        funcion()
    except (TypeError, ValueError):
        return
    raise AssertionError("La operación debía fallar")


def ejecutar_pruebas():
    cliente = Cliente("Ana", "70000000")
    silpancho = Plato("Silpancho", 35, ["lunes", "martes"])
    mocochinchi = RefrescoNatural("Mocochinchi", 6, "vaso")
    combo = Combo("Combo valluno", [silpancho, mocochinchi])

    # 1. Validación de precio y teléfono.
    debe_fallar(lambda: Plato("Inválido", 0, ["lunes"]))
    debe_fallar(lambda: Cliente("Ana", "12345678"))

    # 2. Variante B: combo con 12 % de descuento: 41 * 0,88 = 36,08.
    assert combo.calcular_precio() == 36.08

    # 3. Variante B: martes 2 x 1 en vasos de refresco natural.
    assert mocochinchi.precio_para_cantidad(3, "martes") == 12.00

    # 4. Combo que contiene otro combo.
    combo_anidado = Combo("Combo doble", [combo, Gaseosa("Gaseosa", 5)])
    assert combo_anidado.calcular_precio() == 36.15

    # 5. Variante B: envases a Bs 2,50 por plato, incluidos en un combo.
    pedido_llevar = PedidoLlevar(cliente, [(combo, 2)])
    assert pedido_llevar.calcular_cargos() == 5.00

    # 6. Variante B: delivery gratis desde Bs 120 en todas las zonas.
    plato_caro = Plato("Plato grande", 60, ["domingo"])
    pedido_gratis = PedidoDelivery(cliente, "Vinto", [(plato_caro, 2)])
    assert pedido_gratis.calcular_subtotal("domingo") == 120.00
    assert pedido_gratis.calcular_cargos("domingo") == 0

    # 7. Pedido mínimo de delivery de Bs 50.
    pedido_minimo = PedidoDelivery(cliente, "Quillacollo", [(silpancho, 2)])
    assert pedido_minimo.calcular_cargos("lunes") == 15
    debe_fallar(lambda: PedidoDelivery(cliente, "Cercado", [(silpancho, 1)]).calcular_cargos("lunes"))

    # 8. Estados y protección de los productos del pedido.
    pedido_local = PedidoLocal(cliente, 3, [(silpancho, 1)])
    pedido_local.cambiar_estado("EN_PREPARACION")
    debe_fallar(lambda: pedido_local.agregar_producto(mocochinchi))
    pedido_local.cambiar_estado("LISTO")
    pedido_local.entregar()
    assert pedido_local.estado == "ENTREGADO"

    # 9. Pago QR válido y comisión de tarjeta del 3 %.
    assert PagoQR("1234567890").procesar_pago(50)["aprobado"] is True
    assert PagoTarjeta("4500123456789012").procesar_pago(100)["total"] == 103.00
    debe_fallar(lambda: PagoQR("123"))

    # 10. El delivery no acepta tarjeta.
    debe_fallar(lambda: pedido_gratis.cobrar(PagoTarjeta("4500123456789012"), "domingo"))

    # 11. Reporte por tipo y tres productos más vendidos.
    restaurante = Restaurante()
    restaurante.agregar_cliente(cliente)
    restaurante.agregar_producto(silpancho)
    restaurante.crear_pedido(cliente, [silpancho], "local", mesa=1)
    reporte = restaurante.reporte_ventastas("lunes")
    assert reporte["cantidad_pedidos"] == 1
    assert reporte["tres_productos_mas_vendidos"][0][0] == "Silpancho"

    print("11 pruebas superadas correctamente")


if __name__ == "__main__":
    ejecutar_pruebas()
