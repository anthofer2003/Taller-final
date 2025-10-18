class AjusteDetalleDto:
    def __init__(self, id_ajuste: int, id_item: int, cantidad: int, precio_unitario: float = 0.0, motivo: str = None):
        self.__id_ajuste = id_ajuste
        self.__id_item = id_item
        self.__cantidad = cantidad
        self.__precio_unitario = precio_unitario
        self.__motivo = motivo

    @property
    def id_ajuste(self) -> int:
        return self.__id_ajuste

    @id_ajuste.setter
    def id_ajuste(self, valor: int):
        self.__id_ajuste = valor

    @property
    def id_item(self) -> int:
        return self.__id_item

    @id_item.setter
    def id_item(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("id_item debe ser entero positivo")
        self.__id_item = valor

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        if not isinstance(valor, int):
            raise ValueError("cantidad debe ser entero")
        self.__cantidad = valor

    @property
    def precio_unitario(self) -> float:
        return self.__precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise ValueError("precio_unitario debe ser numérico")
        self.__precio_unitario = float(valor)

    @property
    def motivo(self) -> str:
        return self.__motivo

    @motivo.setter
    def motivo(self, valor: str):
        self.__motivo = valor
