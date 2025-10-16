from typing import List
from datetime import date
from app.dao.gestionar_compras.registrar_presupuesto_compras.dto.presupuesto_compra_detalle_dto import PresupuestoDeComprasDetalleDto
from app.dao.referenciales.estado_presupuesto_compra.estado_presupuesto_compra_dto import EstadoPresupuestoCompra

class PresupuestoDeComprasDto:

    def __init__(self, id_presupuesto: int, nro_presupuesto: str, id_empleado: int,
                 id_proveedor: int, id_sucursal: int, id_deposito: int,
                 empresa: str, funcionario: str, fecha: date,
                 estado: EstadoPresupuestoCompra,
                 detalle_presupuesto: List[PresupuestoDeComprasDetalleDto]):

        self.__id_presupuesto = id_presupuesto
        self.__nro_presupuesto = nro_presupuesto
        self.__id_empleado = id_empleado
        self.__id_proveedor = id_proveedor
        self.__id_sucursal = id_sucursal
        self.__id_deposito = id_deposito
        self.__empresa = empresa
        self.__funcionario = funcionario
        self.__fecha = fecha
        self.__estado = estado
        self.__detalle_presupuesto = detalle_presupuesto

    # --- Propiedades ---
    @property
    def id_presupuesto(self) -> int:
        return self.__id_presupuesto

    @id_presupuesto.setter
    def id_presupuesto(self, valor: int):
        self.__id_presupuesto = valor

    @property
    def nro_presupuesto(self) -> str:
        return self.__nro_presupuesto

    @nro_presupuesto.setter
    def nro_presupuesto(self, valor: str):
        if not valor:
            raise ValueError("El número de presupuesto no puede estar vacío")
        self.__nro_presupuesto = valor

    @property
    def id_empleado(self) -> int:
        return self.__id_empleado

    @id_empleado.setter
    def id_empleado(self, valor: int):
        if not valor:
            raise ValueError("El atributo id_empleado no puede estar vacío")
        self.__id_empleado = valor

    @property
    def id_proveedor(self) -> int:
        return self.__id_proveedor

    @id_proveedor.setter
    def id_proveedor(self, valor: int):
        if not valor:
            raise ValueError("Debe indicar el proveedor")
        self.__id_proveedor = valor

    @property
    def id_sucursal(self) -> int:
        return self.__id_sucursal

    @id_sucursal.setter
    def id_sucursal(self, valor: int):
        if not valor:
            raise ValueError("Debe indicar la sucursal")
        self.__id_sucursal = valor

    @property
    def id_deposito(self) -> int:
        return self.__id_deposito

    @id_deposito.setter
    def id_deposito(self, valor: int):
        if not valor:
            raise ValueError("Debe indicar el depósito")
        self.__id_deposito = valor

    @property
    def empresa(self) -> str:
        return self.__empresa

    @empresa.setter
    def empresa(self, valor: str):
        self.__empresa = valor

    @property
    def funcionario(self) -> str:
        return self.__funcionario

    @funcionario.setter
    def funcionario(self, valor: str):
        self.__funcionario = valor

    @property
    def fecha(self) -> date:
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: date):
        self.__fecha = valor

    @property
    def estado(self) -> EstadoPresupuestoCompra:
        return self.__estado

    @estado.setter
    def estado(self, valor: EstadoPresupuestoCompra):
        self.__estado = valor

    @property
    def detalle_presupuesto(self) -> List[PresupuestoDeComprasDetalleDto]:
        return self.__detalle_presupuesto

    @detalle_presupuesto.setter
    def detalle_presupuesto(self, lista: List[PresupuestoDeComprasDetalleDto]):
        if not isinstance(lista, list):
            raise ValueError("El detalle debe ser una lista de PresupuestoDeComprasDetalleDto")
        self.__detalle_presupuesto = lista
