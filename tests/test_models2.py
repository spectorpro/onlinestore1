import unittest

from src.models import Category, Product


class TestProductAndCategory(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
        self.product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        self.category1 = Category("Смартфоны", "Описание категории", [self.product1, self.product2])

    def test_private_attributes(self):
        """Тест приватных атрибутов"""
        with self.assertRaises(AttributeError):
            _ = self.category1.__products

    def test_add_product(self):
        """Тест метода add_product"""
        product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
        initial_count = Category.product_count
        self.category1.add_product(product3)
        self.assertIn(product3, self.category1._Category__products)
        self.assertEqual(Category.product_count, initial_count + 1)

    def test_products_getter(self):
        """Тест геттера products"""
        products_str = self.category1.products
        self.assertIn("Samsung Galaxy S23 Ultra", products_str)
        self.assertIn("180000.0 руб.", products_str)
        self.assertIn("5 шт.", products_str)

    def test_new_product_classmethod(self):
        """Тест класс-метода new_product"""
        product_data = {
            "name": "55\" QLED 4K",
            "description": "Фоновая подсветка",
            "price": 123000.0,
            "quantity": 7
        }
        new_product = Product.new_product(product_data)
        self.assertIsInstance(new_product, Product)
        self.assertEqual(new_product.name, "55\" QLED 4K")

    def test_duplicate_product_handling(self):
        """Тест обработки дубликатов в new_product"""
        existing_products = [
            Product("Duplicate Phone", "Test", 1000.0, 5)
        ]
        duplicate_data = {
            "name": "Duplicate Phone",
            "description": "Updated",
            "price": 1500.0,  # выше старой цены
            "quantity": 3
        }
        updated_product = Product.new_product(duplicate_data, existing_products)
        self.assertEqual(updated_product.quantity, 8)  # 5 + 3
        self.assertEqual(updated_product.price, 1500.0)  # более высокая цена
