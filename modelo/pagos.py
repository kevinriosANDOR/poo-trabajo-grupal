from abc import ABC, abstractmethod
import re


class MetodoPago(ABC):
    nombre = "Método de pago"
    permite_delivery = True

    @abstractmethod
    def procesar_pago(self, total):
        pass


class PagoEfectivo(MetodoPago):
    nombre = "Efectivo"

    def __init__(self, monto_recibido):
        self.monto_recibido = float(monto_recibido)
        if self.monto_recibido < 0:
            raise ValueError("El monto recibido no puede ser negativo")

    def procesar_pago(self, total):
        total = round(float(total), 2)
        if self.monto_recibido < total:
            raise ValueError("El monto recibido no cubre el total")
        return {
            "metodo": self.nombre,
            "total": total,
            "aprobado": True,
            "cambio": round(self.monto_recibido - total, 2),
        }


class PagoQR(MetodoPago):
    nombre = "QR"

    def __init__(self, codigo_transaccion):
        codigo_transaccion = str(codigo_transaccion)
        if not re.fullmatch(r"\d{10}", codigo_transaccion):
            raise ValueError("El código QR debe tener 10 dígitos")
        self.codigo_transaccion = codigo_transaccion

    def procesar_pago(self, total):
        return {
            "metodo": self.nombre,
            "total": round(float(total), 2),
            "aprobado": True,
            "codigo": self.codigo_transaccion,
        }


class PagoTarjeta(MetodoPago):
    nombre = "Tarjeta"
    permite_delivery = False
    COMISION = 0.03

    def __init__(self, numero_tarjeta):
        numero_tarjeta = str(numero_tarjeta)
        if not numero_tarjeta.isdigit() or len(numero_tarjeta) < 4:
            raise ValueError("El número de tarjeta no es válido")
        self.numero_tarjeta = numero_tarjeta

    def procesar_pago(self, total):
        total = round(float(total), 2)
        comision = round(total * self.COMISION, 2)
        return {
            "metodo": self.nombre,
            "total": round(total + comision, 2),
            "subtotal": total,
            "comision": comision,
            "aprobado": True,
            "ultimos_digitos": self.numero_tarjeta[-4:],
        }
