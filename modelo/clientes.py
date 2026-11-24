import re


class Cliente:
    def __init__(self, nombre, telefono):
        self._nombre = str(nombre).strip()
        if not self._nombre:
            raise ValueError("El nombre del cliente no puede estar vacío")
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor)
        if not re.fullmatch(r"[67]\d{7}", valor):
            raise ValueError("El teléfono debe tener 8 dígitos y empezar en 6 o 7")
        self._telefono = valor

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"
