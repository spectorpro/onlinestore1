

class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price  # приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для атрибута цены"""
        return self._price

    @price.setter
    def price(self, value: float):
        """Сеттер для атрибута цены с проверкой"""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            # Дополнительное задание: подтверждение понижения цены
            if value < self._price:
                response = input(f"Цена понижается с {self._price} до {value}. Подтвердить (y/n)? ")
                if response.lower() == 'y':
                    self._price = value
                else:
                    print("Изменение цены отменено")
            else:
                self._price = value

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        """
        Класс-метод для создания нового продукта

        Args:
            product_data: словарь с данными продукта
            products_list: список существующих продуктов для проверки дубликатов

        Returns:
            Экземпляр класса Product
        """
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        # Дополнительное задание: проверка на дубликаты
        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    # Складываем количество
                    existing_product.quantity += quantity
                    # Выбираем более высокую цену
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products  # приватный атрибут списка товаров

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product):
        """Метод для добавления продукта в категорию"""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для приватного атрибута products"""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result
