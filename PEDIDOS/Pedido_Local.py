import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelo.pedidos import PedidoLocal

Pedido_Local = PedidoLocal

__all__ = ["PedidoLocal", "Pedido_Local"]
