from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class CreationLoggerMixin:
    """
    Миксин, который при создании объекта выводит в консоль информацию
    о том, от какого класса и с какими параметрами был создан объект.
    """

    def __init__(self, *args, **kwargs):
        # Получаем имя класса, от которого реально создаётся объект
        cls_name = self.__class__.__name__
        # Формируем представление аргументов для вывода
        args_repr = ", ".join(repr(a) for a in args)
        kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_repr, kwargs_repr]))
        print(f"{cls_name}({all_args})")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    Выделяет общую функциональность, которая должна быть у каждого продукта.
    """

    @abstractmethod
    def get_details(self) -> str:
        """Возвращает детали продукта, специфичные для подкласса."""
        pass

    @abstractmethod
    def get_type(self) -> str:
        """Возвращает тип продукта."""
        pass

    def get_total_cost(self) -> float:
        """Общая функциональность: итоговая стоимость всех единиц товара на складе."""
        return self.price * self.quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


class Product(BaseProduct, CreationLoggerMixin):
    """
    Базовый класс продукта. Теперь наследуется от BaseProduct и CreationLoggerMixin.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        # Вызов конструктора миксина и базового класса происходит через super()
        super().__init__()

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            if value < self.__price:
                response = input(
                    f"Цена понижается с {self.__price} до {value}. Подтвердить (y/n)? "
                )
                if response.lower() == "y":
                    self.__price = value
                else:
                    print("Изменение цены отменено")
            else:
                self.__price = value

    def get_details(self) -> str:
        return f"{self.name}: {self.description}"

    def get_type(self) -> str:
        return "Product"

    def __add__(self, other: "Product") -> float:
        if type(self) is not type(other):
            raise TypeError(
                f"Нельзя складывать товары разных классов: {type(self).__name__} и {type(other).__name__}"
            )
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(
        cls,
        product_data: Dict[str, Any],
        products_list: Optional[List["Product"]] = None,
    ) -> "Product":
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def get_details(self) -> str:
        return (
            f"{self.name} ({self.model}, {self.memory} ГБ, {self.color}) - "
            f"эффективность: {self.efficiency}"
        )

    def get_type(self) -> str:
        return "Smartphone"


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def get_details(self) -> str:
        return (
            f"{self.name} из {self.country}, период прорастания: {self.germination_period}, "
            f"цвет: {self.color}"
        )

    def get_type(self) -> str:
        return "LawnGrass"


# --- Дополнительное задание: Заказ и Категория ---

class BaseShopEntity(ABC):
    """
    Общий абстрактный класс для сущностей магазина (Заказ, Категория).
    Выделяем общие свойства: имя и описание.
    """

    @abstractmethod
    def summary(self) -> str:
        """Краткое описание сущности."""
        pass

    @abstractmethod
    def entity_type(self) -> str:
        """Тип сущности."""
        pass


class Order(BaseShopEntity, CreationLoggerMixin):
    """
    Класс «Заказ»: содержит ссылку на товар, количество и итоговую стоимость.
    В заказе может быть указан только один товар.
    """

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        super().__init__()

    @property
    def total_cost(self) -> float:
        return self.product.price * self.quantity

    def summary(self) -> str:
        return (
            f"Заказ: {self.product.name}, количество: {self.quantity}, "
            f"итого: {self.total_cost:.2f} руб."
        )

    def entity_type(self) -> str:
        return "Order"


class Category(BaseShopEntity, CreationLoggerMixin):
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)
        super().__init__()

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        if not self.__products:
            return ""
        result = [
            f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт." for p in self.__products
        ]
        return "\n".join(result)

    def summary(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"Категория: {self.name}, всего товаров: {len(self.__products)}, общее количество: {total_quantity} шт."

    def entity_type(self) -> str:
        return "Category"

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
