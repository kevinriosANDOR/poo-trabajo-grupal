import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelo.pedidos import PedidoLlevar

Pedido_Llevar = PedidoLlevar

__all__ = ["PedidoLlevar", "Pedido_Llevar"]
