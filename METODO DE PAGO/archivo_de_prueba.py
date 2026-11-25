from pago_efectivo import PagoEfectivo
from pago_qr import PagoQR
from pago_tarjeta import PagoTarjeta

# Pruebas
pago1 = PagoEfectivo(100.0)
print(pago1.procesar_pago(80.50))

pago2 = PagoQR("1234567890")
print(pago2.procesar_pago(150.00))

pago3 = PagoTarjeta("4500123456789012")
print(pago3.procesar_pago(320.00))
