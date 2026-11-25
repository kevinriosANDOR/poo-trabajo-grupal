# Sistema de Pedidos Sabor Valluno

Proyecto integrador de Programación Orientada a Objetos para un restaurante de comida típica de Cochabamba.

## Variante B

- Descuento de combos: 12 %.
- Envase para llevar: Bs 2,50 por plato, incluidos los platos dentro de combos.
- Delivery gratis desde Bs 120 en todas las zonas.
- Pedido mínimo de delivery: Bs 50.
- Los martes hay promoción 2 × 1 en vasos de refresco natural.
- El chicharrón está disponible solamente los domingos.

## Ejecución

Desde la carpeta principal del repositorio:

```powershell
py restaurante.py
```

El sistema muestra un menú de consola para registrar clientes, consultar el menú, crear pedidos, cobrar y consultar el reporte de ventas.

Para ejecutar las pruebas:

```powershell
py pruebas.py
```

Las carpetas `PRODUCTOS`, `PEDIDOS` y `METODO DE PAGO` funcionan como módulos adaptadores de la implementación de `modelo/`. El punto de entrada del sistema es `restaurante.py` y las pruebas están en `pruebas.py`.
