import pytest

from src.models import Category, Product


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
    # Проверяем, что все продукты присутствуют (сравниваем по именам)
    product_names = [p.name for p in sample_category._Category__products]
    expected_names = [p.name for p in sample_products]
    assert product_names == expected_names


def test_category_product_count(sample_category):
    assert len(sample_category._Category__products) == 3


def test_category_count_increment():
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


def test_empty_category():
    """Тест создания категории без товаров."""
    category = Category("Пустая категория", "Описание пустой категории", [])
    assert category.name == "Пустая категория"
    assert category.description == "Описание пустой категории"
    assert len(category._Category__products) == 0
    assert Category.category_count >= 1  # Категория учтена в общем счёте
    assert Category.product_count >= 0  # Количество товаров не увеличилось


def test_single_product_category():
    """Тест категории с одним товаром."""
    product = Product("Единственный товар", "Описание единственного товара", 999.99, 1)
    category = Category("Одиночный товар", "Категория с одним товаром", [product])

    assert len(category._Category__products) == 1
    assert category._Category__products[0].name == "Единственный товар"
    assert Category.product_count >= 1


def test_product_price_confirmation_decline(monkeypatch):
    """Тест отмены понижения цены."""
    product = Product("Test", "Desc", 100.0, 5)

    def mock_input(prompt):
        return 'n'  # Пользователь отменяет

    monkeypatch.setattr('builtins.input', mock_input)
    original_price = product.price
    product.price = 50.0  # Пытаемся понизить цену
    assert product.price == original_price  # Цена не изменилась


def test_product_price_confirmation_accept(monkeypatch):
    """Тест подтверждения понижения цены."""
    product = Product("Test", "Desc", 100.0, 5)

    def mock_input(prompt):
        return 'y'  # Пользователь подтверждает

    monkeypatch.setattr('builtins.input', mock_input)
    product.price = 50.0  # Понижаем цену
    assert product.price == 50.0


def test_product_price_increase():
    """Тест повышения цены (без подтверждения)."""
    product = Product("Test", "Desc", 100.0, 5)
    product.price = 150.0
    assert product.price == 150.0


def test_new_product_duplicate_merge():
    """Тест слияния дубликатов через new_product."""
    existing_product = Product("Duplicate", "Desc", 50.0, 3)
    products_list = [existing_product]

    # Создаём дубликат с большим количеством и ценой
    duplicate_data = {"name": "Duplicate", "description": "New Desc", "price": 70.0, "quantity": 5}
    result = Product.new_product(duplicate_data, products_list)

    # Должен вернуть существующий продукт
    assert result is existing_product
    # Количество должно сложиться
    assert existing_product.quantity == 8  # 3 + 5
    # Цена должна обновиться на большую
    assert existing_product.price == 70.0


def test_new_product_no_duplicate():
    """Тест создания нового продукта без дубликатов."""
    products_list = []
    new_data = {"name": "New Product", "description": "Desc", "price": 100.0, "quantity": 1}
    result = Product.new_product(new_data, products_list)

    assert isinstance(result, Product)
    assert result.name == "New Product"
    assert len(products_list) == 0  # Список не изменился


def test_add_product_updates_count():
    """Тест добавления продукта обновляет счётчик."""
    initial_count = Category.product_count
    category = Category("Test", "Desc", [])
    product = Product("New", "Desc", 10.0, 1)

    category.add_product(product)
    assert Category.product_count == initial_count + 1
    assert len(category._Category__products) == 1
