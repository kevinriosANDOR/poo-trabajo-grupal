import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelo.pedidos import PedidoDelivery

Pedido_Delivery = PedidoDelivery

__all__ = ["PedidoDelivery", "Pedido_Delivery"]
