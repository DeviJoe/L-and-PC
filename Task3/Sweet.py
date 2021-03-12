class Sweet:

    __label: str
    __price: int

    def __init__(self, label: str, price: int) -> None:
        super().__init__()
        self.__label = label
        self.__price = price

    @property
    def label(self) -> str:
        return self.__label

    @property
    def price(self) -> int:
        return self.__price

    def __str__(self) -> str:
        out = "label - " + self.__label + ", price - " + str(self.__price)
        return out

