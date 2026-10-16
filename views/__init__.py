"""
Paquete de Vistas del Prototipo Modular DistriGest.
Permite la importación limpia y centralizada hacia el controlador principal.
"""
from .clientes_view import ClientesView
from .bodega_view import BodegaView
from .facturacion_view import FacturacionView
from .proveedores_view import ProveedoresView
from .reportes_view import ReportesView

__all__ = [
    "ClientesView",
    "BodegaView",
    "FacturacionView",
    "ProveedoresView",
    "ReportesView"
]
