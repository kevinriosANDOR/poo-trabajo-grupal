from metodo_pago import Metodo_Pago

class PagoQR(Metodo_Pago):
    def __init__(self, codigo_qr):
        super().__init__("QR")
        self.codigo_qr = codigo_qr
        
    def procesar_pago(self, monto):
        return f"Pago por QR ({self.codigo_qr}) de Bs. {monto:.2f} aceptado"