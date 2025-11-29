# presupuesto_proveedor_dto.py

from datetime import date
from typing import List
from app.dao.gestionar_compras.registrar_presupuesto_proveedor.dto.presupuesto_proveedor_detalle_dto import PresupuestoProveedorDetalleDto
from app.dao.referenciales.estado_presupuesto_proveedor.estado_presupuesto_proveedor_dto import EstadoPresupuesto

class PresupuestoProveedorDto:
    def __init__(self, id_presupuesto: int, id_proveedor: int, id_empleado: int, id_sucursal: int,
                 estado: EstadoPresupuesto, fecha_presupuesto: date,
                 detalle_presupuesto: List[PresupuestoProveedorDetalleDto]):
        self.__id_presupuesto = id_presupuesto
        self.__id_proveedor = id_proveedor
        self.__id_empleado = id_empleado
        self.__id_sucursal = id_sucursal
        self.__estado = estado
        self.__fecha_presupuesto = fecha_presupuesto
        self.__detalle_presupuesto = detalle_presupuesto

    @property
    def id_presupuesto(self): return self.__id_presupuesto

    @id_presupuesto.setter
    def id_presupuesto(self, val): self.__id_presupuesto = val

    @property
    def id_proveedor(self): return self.__id_proveedor

    @id_proveedor.setter
    def id_proveedor(self, val): self.__id_proveedor = val

    @property
    def id_empleado(self): return self.__id_empleado

    @id_empleado.setter
    def id_empleado(self, val): self.__id_empleado = val

    @property
    def id_sucursal(self): return self.__id_sucursal

    @id_sucursal.setter
    def id_sucursal(self, val): self.__id_sucursal = val

    @property
    def estado(self): return self.__estado

    @estado.setter
    def estado(self, val):
        if not isinstance(val, EstadoPresupuesto):
            raise ValueError("Estado debe ser tipo EstadoPresupuesto")
        self.__estado = val

    @property
    def fecha_presupuesto(self): return self.__fecha_presupuesto

    @fecha_presupuesto.setter
    def fecha_presupuesto(self, val):
        self.__fecha_presupuesto = val

    @property
    def detalle_presupuesto(self): return self.__detalle_presupuesto

    @detalle_presupuesto.setter
    def detalle_presupuesto(self, val):
        if not isinstance(val, list):
            raise ValueError("Detalle debe ser una lista de PresupuestoProveedorDetalleDto")
        self.__detalle_presupuesto = val
