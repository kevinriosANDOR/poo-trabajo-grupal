import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelo.pagos import PagoTarjeta

__all__ = ["PagoTarjeta"]
