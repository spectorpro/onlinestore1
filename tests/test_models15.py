import pytest
from src.models import Product, Category

def test_product_str():
    product = Product("Test Product", "Description", 100.0, 5)
    assert str(product) == "Test Product, 100.0 руб. Остаток: 5 шт."

def test_category_str():
    product1 = Product("Product 1", "Desc", 100.0, 3)
    product2 = Product("Product 2", "Desc", 200.0, 7)
    category = Category("Test Category", "Desc", [product1, product2])
    assert str(category) == "Test Category, количество продуктов: 10 шт."

def test_product_addition():
    product1 = Product("Product 1", "Desc", 100.0, 10)
    product2 = Product("Product 2", "Desc", 200.0, 2)
    result = product1 + product2
    assert result == 1400.0


if __name__ == '__main__':
    pytest.main()