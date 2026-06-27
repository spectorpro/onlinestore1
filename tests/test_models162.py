import pytest

from src.models import (BaseProduct, Category, LawnGrass, Order, Product,
                        Smartphone)


def test_base_product_abstract():
    with pytest.raises(TypeError):
        BaseProduct()  # type: ignore


def test_product_creation():
    p = Product("Test", "Desc", 100.0, 5)
    assert p.name == "Test"
    assert p.price == 100.0
    assert p.quantity == 5


def test_product_total_cost():
    p = Product("Test", "Desc", 100.0, 5)
    assert p.get_total_cost() == 500.0


def test_smartphone_inheritance():
    s = Smartphone("Phone", "Desc", 500.0, 2, 0.9, "ModelX", 256, "Black")
    assert isinstance(s, Product)
    assert s.get_type() == "Smartphone"


def test_lawn_grass_inheritance():
    g = LawnGrass("Grass", "Desc", 20.0, 10, "RU", "7 дней", "Green")
    assert isinstance(g, Product)
    assert g.get_type() == "LawnGrass"


def test_category_creation_and_counts():
    Category.category_count = 0
    Category.product_count = 0
    p1 = Product("A", "B", 10.0, 1)
    p2 = Product("C", "D", 20.0, 2)
    cat = Category("TestCat", "Desc", [p1, p2])
    assert cat.name == "TestCat"
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_order_creation_and_total():
    p = Product("Item", "Desc", 150.0, 10)
    o = Order(p, 3)
    assert o.product is p
    assert o.quantity == 3
    assert o.total_cost == 450.0
