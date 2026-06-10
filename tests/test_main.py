import pytest
from src.main import Product, Category


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 5)

@pytest.fixture
def sample_products():
    return [
        Product("Product 1", "Description 1", 50.0, 3),
        Product("Product 2", "Description 2", 75.0, 2),
        Product("Product 3", "Description 3", 120.0, 8)
    ]

@pytest.fixture
def sample_category(sample_products):
    return Category("Test Category", "Test Category Description", sample_products)

def test_product_initialization(sample_product):
    assert sample_product.name == "Test Product"
    assert sample_product.description == "Test Description"
    assert sample_product.price == 100.0
    assert sample_product.quantity == 5

def test_category_initialization(sample_category, sample_products):
    assert sample_category.name == "Test Category"
    assert sample_category.description == "Test Category Description"
    assert sample_category.products == sample_products

def test_category_product_count(sample_category):
    assert len(sample_category.products) == 3

def test_category_count_increment():
    # Обнуляем счётчики для теста
    Category.category_count = 0
    Category.product_count = 0

    products1 = [Product("P1", "D1", 10.0, 1)]
    category1 = Category("C1", "Desc1", products1)
    assert Category.category_count == 1
    assert Category.product_count == 1

    products2 = [Product("P2", "D2", 20.0, 2), Product("P3", "D3", 30.0, 3)]
    category2 = Category("C2", "Desc2", products2)
    assert Category.category_count == 2
    assert Category.product_count == 3  # 1 + 2 = 3
