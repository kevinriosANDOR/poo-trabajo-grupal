from metodo_pago import Metodo_Pago

class PagoEfectivo(Metodo_Pago):
    def __init__(self, monto_recibido):
        super().__init__("Efectivo")
        self.monto_recibido = monto_recibido
        
    def procesar_pago(self, monto):
        if self.monto_recibido < monto:
            return f"Pago rechazado: faltan {monto - self.monto_recibido:.2f} Bs."
        cambio = self.monto_recibido - monto
        return f"Pago en efectivo aceptado. Cambio {cambio:.2f} Bs."