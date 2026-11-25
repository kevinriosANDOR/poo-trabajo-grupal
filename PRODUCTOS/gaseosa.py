import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelo.productos import Gaseosa

gaseosa = Gaseosa

__all__ = ["Gaseosa", "gaseosa"]
