import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelo.productos import Bebida

TamanoBebida = Bebida
tamano_bebida = Bebida

__all__ = ["TamanoBebida", "tamano_bebida"]
