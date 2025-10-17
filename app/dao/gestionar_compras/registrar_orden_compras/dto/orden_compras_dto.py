from typing import List
from datetime import date
from app.dao.gestionar_compras.registrar_orden_compras.dto.orden_compra_detalle_dto import OrdenDeCompraDetalleDto
from app.dao.referenciales.estado_orden_compra.estado_orden_compra_dto import EstadoOrdenCompra

class OrdenDeCompraDto:
    def __init__(self,
                 id_orden_compra: int,
                 nro_orden: str,
                 id_empleado: int,
                 id_proveedor: int,
                 id_sucursal: int,
                 id_deposito: int,
                 empresa: str,
                 funcionario: str,
                 fecha: date,
                 fecha_vencimiento: date = None,
                 factura: str = None,
                 tipo_pago: str = None,  # 'Credito' | 'Debito'
                 nro_pedido: str = None,
                 estado: EstadoOrdenCompra = None,
                 detalle_orden: List[OrdenDeCompraDetalleDto] = None):

        self.__id_orden_compra = id_orden_compra
        self.__nro_orden = nro_orden
        self.__id_empleado = id_empleado
        self.__id_proveedor = id_proveedor
        self.__id_sucursal = id_sucursal
        self.__id_deposito = id_deposito
        self.__empresa = empresa
        self.__funcionario = funcionario
        self.__fecha = fecha
        self.__fecha_vencimiento = fecha_vencimiento
        self.__factura = factura
        self.__tipo_pago = tipo_pago
        self.__nro_pedido = nro_pedido
        self.__estado = estado
        self.__detalle_orden = detalle_orden or []

    @property
    def id_orden_compra(self) -> int:
        return self.__id_orden_compra

    @id_orden_compra.setter
    def id_orden_compra(self, valor: int):
        self.__id_orden_compra = valor

    @property
    def nro_orden(self) -> str:
        return self.__nro_orden

    @nro_orden.setter
    def nro_orden(self, valor: str):
        self.__nro_orden = valor

    @property
    def id_empleado(self) -> int:
        return self.__id_empleado

    @id_empleado.setter
    def id_empleado(self, valor: int):
        if not valor:
            raise ValueError("id_empleado es obligatorio")
        self.__id_empleado = valor

    @property
    def id_proveedor(self) -> int:
        return self.__id_proveedor

    @id_proveedor.setter
    def id_proveedor(self, valor: int):
        if not valor:
            raise ValueError("id_proveedor es obligatorio")
        self.__id_proveedor = valor

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
    def fecha_vencimiento(self) -> date:
        return self.__fecha_vencimiento

    @fecha_vencimiento.setter
    def fecha_vencimiento(self, valor: date):
        self.__fecha_vencimiento = valor

    @property
    def factura(self) -> str:
        return self.__factura

    @factura.setter
    def factura(self, valor: str):
        self.__factura = valor

    @property
    def tipo_pago(self) -> str:
        return self.__tipo_pago

    @tipo_pago.setter
    def tipo_pago(self, valor: str):
        self.__tipo_pago = valor

    @property
    def nro_pedido(self) -> str:
        return self.__nro_pedido

    @nro_pedido.setter
    def nro_pedido(self, valor: str):
        self.__nro_pedido = valor

    @property
    def estado(self) -> EstadoOrdenCompra:
        return self.__estado

    @estado.setter
    def estado(self, valor: EstadoOrdenCompra):
        self.__estado = valor

    @property
    def detalle_orden(self):
        return self.__detalle_orden

    @detalle_orden.setter
    def detalle_orden(self, lista):
        if not isinstance(lista, list):
            raise ValueError("detalle_orden debe ser una lista")
        self.__detalle_orden = lista
