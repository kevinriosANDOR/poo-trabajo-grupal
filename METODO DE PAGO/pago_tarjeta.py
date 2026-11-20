from metodo_pago import Metodo_Pago

class PagoTarjeta(Metodo_Pago):
    def __init__(self, numero_tarjeta):
        super().__init__("Tarjeta")
        self.numero_tarjeta = numero_tarjeta
        
    def procesar_pago(self, monto):
        ultimos = self.numero_tarjeta[-4:]
        return f"Pago con tarjeta ****{ultimos} de Bs. {monto:.2f} aceptado"