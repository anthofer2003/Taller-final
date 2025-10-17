class OrdenDeCompraDetalleDto:
    def __init__(self, id_orden_compra: int, id_item: int, cantidad: int, precio_unitario: float = 0.0):
        self.__id_orden_compra = id_orden_compra
        self.__id_item = id_item
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario

    @property
    def id_orden_compra(self) -> int:
        return self.__id_orden_compra

    @id_orden_compra.setter
    def id_orden_compra(self, valor: int):
        self.__id_orden_compra = valor

    @property
    def id_item(self) -> int:
        return self.__id_item

    @id_item.setter
    def id_item(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El atributo id_item debe ser un entero positivo")
        self.__id_item = valor

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
            raise ValueError("El precio_unitario debe ser >= 0")
        self.__precio_unitario = float(valor)
