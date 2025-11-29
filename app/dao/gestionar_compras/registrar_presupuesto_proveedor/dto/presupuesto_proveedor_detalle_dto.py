# presupuesto_proveedor_detalle_dto.py

class PresupuestoProveedorDetalleDto:
    def __init__(self, id_presupuesto: int, id_producto: int, cantidad: int, precio_unitario: float):
        self.__id_presupuesto = id_presupuesto
        self.__id_producto = id_producto
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario

    @property
    def id_presupuesto(self) -> int:
        return self.__id_presupuesto

    @id_presupuesto.setter
    def id_presupuesto(self, valor: int):
        self.__id_presupuesto = valor

    @property
    def id_producto(self) -> int:
        return self.__id_producto

    @id_producto.setter
    def id_producto(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El id_producto debe ser un entero positivo")
        self.__id_producto = valor

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
        self.__cantidad = valor

    @property
    def precio_unitario(self) -> float:
        return self.__precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor: float):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El precio_unitario debe ser un número positivo")
        self.__precio_unitario = valor
