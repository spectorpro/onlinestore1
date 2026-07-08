import unittest

from src.models import Category, LawnGrass, Product, Smartphone


class TestProduct(unittest.TestCase):
    def test_product_creation(self):
        p = Product("Товар", "Описание", 100.0, 5)
        self.assertEqual(p.name, "Товар")
        self.assertEqual(p.price, 100.0)
        self.assertEqual(p.quantity, 5)

    def test_product_add_same_class(self):
        p1 = Product("Товар 1", "Описание 1", 100.0, 2)
        p2 = Product("Товар 2", "Описание 2", 200.0, 3)
        total = p1 + p2
        expected = 100 * 2 + 200 * 3
        self.assertEqual(total, expected)

    def test_product_add_different_class_raises(self):
        p = Product("Товар", "Описание", 100.0, 5)
        s = Smartphone("Смартфон", "Описание", 20000.0, 2, 95.0, "Model", 128, "Black")
        with self.assertRaises(TypeError):
            _ = p + s


class TestSmartphone(unittest.TestCase):
    def test_smartphone_creation_and_attributes(self):
        s = Smartphone(
            "Смартфон",
            "Описание",
            20000.0,
            2,
            95.0,
            "Model",
            128,
            "Black",
        )
        self.assertEqual(s.name, "Смартфон")
        self.assertEqual(s.efficiency, 95.0)
        self.assertEqual(s.model, "Model")
        self.assertEqual(s.memory, 128)
        self.assertEqual(s.color, "Black")

    def test_smartphone_add_smartphone(self):
        s1 = Smartphone(
            "S1", "Desc", 20000.0, 2, 95.0, "M1", 128, "Black"
        )
        s2 = Smartphone(
            "S2", "Desc", 30000.0, 1, 98.0, "M2", 256, "White"
        )
        total = s1 + s2
        expected = 20000 * 2 + 30000 * 1
        self.assertEqual(total, expected)

    def test_smartphone_add_other_class_raises(self):
        s = Smartphone(
            "S", "Desc", 20000.0, 2, 95.0, "M", 128, "Black"
        )
        g = LawnGrass(
            "Трава", "Desc", 500.0, 10, "RU", "7 дней", "Green"
        )
        with self.assertRaises(TypeError):
            _ = s + g


class TestLawnGrass(unittest.TestCase):
    def test_lawn_grass_creation_and_attributes(self):
        g = LawnGrass(
            "Трава",
            "Описание",
            500.0,
            10,
            "RU",
            "7 дней",
            "Green",
        )
        self.assertEqual(g.name, "Трава")
        self.assertEqual(g.country, "RU")
        self.assertEqual(g.germination_period, "7 дней")
        self.assertEqual(g.color, "Green")

    def test_lawn_grass_add_lawn_grass(self):
        g1 = LawnGrass(
            "G1", "Desc", 500.0, 10, "RU", "7 дней", "Green"
        )
        g2 = LawnGrass(
            "G2", "Desc", 600.0, 5, "US", "5 дней", "Dark Green"
        )
        total = g1 + g2
        expected = 500 * 10 + 600 * 5
        self.assertEqual(total, expected)


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.s1 = Smartphone(
            "S1", "Desc", 20000.0, 2, 95.0, "M1", 128, "Black"
        )
        self.g1 = LawnGrass(
            "G1", "Desc", 500.0, 10, "RU", "7 дней", "Green"
        )

    def test_category_creation_with_products(self):
        cat = Category("Смартфоны", "Описание категории", [self.s1])
        self.assertEqual(cat.name, "Смартфоны")
        self.assertIn(self.s1, cat._Category__products)  # доступ к приватному атрибуту для теста

    def test_add_product_valid(self):
        cat = Category("Смартфоны", "Описание", [])
        cat.add_product(self.s1)
        self.assertIn(self.s1, cat._Category__products)

    def test_add_product_invalid_type_raises(self):
        cat = Category("Смартфоны", "Описание", [])
        with self.assertRaises(TypeError):
            cat.add_product("not a product")  # type: ignore

    def test_category_product_count_increments(self):
        initial_count = Category.product_count
        cat = Category("Смартфоны", "Описание", [self.s1])
        self.assertEqual(Category.product_count, initial_count + 1)


if __name__ == "__main__":
    unittest.main()
