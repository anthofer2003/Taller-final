class PresupuestoDeComprasDetalleDto:

    def __init__(self, id_presupuesto: int, id_item: int, cantidad: int, precio_iva: float):
        self.__id_presupuesto = id_presupuesto
        self.__id_item = id_item
        self.__cantidad = cantidad
        self.__precio_iva = precio_iva

    # Getters y setters
    @property
    def id_presupuesto(self) -> int:
        return self.__id_presupuesto

    @id_presupuesto.setter
    def id_presupuesto(self, valor: int):
        self.__id_presupuesto = valor

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
    def precio_iva(self) -> float:
        return self.__precio_iva

    @precio_iva.setter
    def precio_iva(self, valor: float):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("El precio debe ser un número mayor o igual a cero")
        self.__precio_iva = valor
