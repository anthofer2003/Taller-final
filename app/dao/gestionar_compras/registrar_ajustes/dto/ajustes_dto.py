from typing import List
from datetime import date
from app.dao.gestionar_compras.registrar_ajustes.dto.ajustes_detalle_dto import AjusteDetalleDto
from app.dao.referenciales.estado_ajustes.estado_ajustes_dto import EstadoAjuste

class AjusteDto:
    def __init__(self,
                 id_ajuste: int,
                 nro_ajuste: str,
                 id_empleado: int,
                 id_sucursal: int,
                 id_deposito: int,
                 empresa: str,
                 funcionario: str,
                 fecha: date,
                 tipo_ajuste: str,     # 'Positivo' o 'Negativo'
                 estado: EstadoAjuste,
                 motivo_general: str,
                 detalle_ajuste: List[AjusteDetalleDto]):

        self.__id_ajuste = id_ajuste
        self.__nro_ajuste = nro_ajuste
        self.__id_empleado = id_empleado
        self.__id_sucursal = id_sucursal
        self.__id_deposito = id_deposito
        self.__empresa = empresa
        self.__funcionario = funcionario
        self.__fecha = fecha
        self.__tipo_ajuste = tipo_ajuste
        self.__estado = estado
        self.__motivo_general = motivo_general
        self.__detalle_ajuste = detalle_ajuste or []

    @property
    def id_ajuste(self) -> int:
        return self.__id_ajuste

    @id_ajuste.setter
    def id_ajuste(self, valor: int):
        self.__id_ajuste = valor

    @property
    def nro_ajuste(self) -> str:
        return self.__nro_ajuste

    @nro_ajuste.setter
    def nro_ajuste(self, valor: str):
        self.__nro_ajuste = valor

    @property
    def id_empleado(self) -> int:
        return self.__id_empleado

    @id_empleado.setter
    def id_empleado(self, valor: int):
        if not valor:
            raise ValueError("id_empleado es obligatorio")
        self.__id_empleado = valor

    @property
    def id_sucursal(self) -> int:
        return self.__id_sucursal

    @id_sucursal.setter
    def id_sucursal(self, valor: int):
        if not valor:
            raise ValueError("id_sucursal es obligatorio")
        self.__id_sucursal = valor

    @property
    def id_deposito(self) -> int:
        return self.__id_deposito

    @id_deposito.setter
    def id_deposito(self, valor: int):
        if not valor:
            raise ValueError("id_deposito es obligatorio")
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
    def tipo_ajuste(self) -> str:
        return self.__tipo_ajuste

    @tipo_ajuste.setter
    def tipo_ajuste(self, valor: str):
        if valor not in ('Positivo','Negativo'):
            raise ValueError("tipo_ajuste debe ser 'Positivo' o 'Negativo'")
        self.__tipo_ajuste = valor

    @property
    def estado(self) -> EstadoAjuste:
        return self.__estado

    @estado.setter
    def estado(self, valor: EstadoAjuste):
        self.__estado = valor

    @property
    def motivo_general(self) -> str:
        return self.__motivo_general

    @motivo_general.setter
    def motivo_general(self, valor: str):
        self.__motivo_general = valor

    @property
    def detalle_ajuste(self) -> List[AjusteDetalleDto]:
        return self.__detalle_ajuste

    @detalle_ajuste.setter
    def detalle_ajuste(self, lista: List[AjusteDetalleDto]):
        if not isinstance(lista, list):
            raise ValueError("detalle_ajuste debe ser una lista")
        self.__detalle_ajuste = lista
