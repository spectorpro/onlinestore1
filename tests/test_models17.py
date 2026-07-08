import pytest

from src.models import Category, Product


def test_product_raises_value_error_on_zero_quantity():
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Test", "Desc", 100.0, 0)


def test_category_average_price_with_products():
    p1 = Product("A", "Desc A", 100.0, 5)
    p2 = Product("B", "Desc B", 200.0, 3)
    category = Category("Test", "Test category", [p1, p2])
    assert category.middle_price() == 150.0


def test_category_average_price_empty():
    category = Category("Empty", "Empty category", [])
    assert category.middle_price() == 0.0
