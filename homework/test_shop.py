"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart

@pytest.fixture
def product_milk() -> Product:
    return Product("milk", 98, "This is a milk", 998)

@pytest.fixture
def product_bread() -> Product:
    return Product("bread", 998, "This is a bread", 98)

@pytest.fixture
def cart() -> Cart:
    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity_equal(self, product_milk):
        # Напишите проверки на метод check_quantity
        assert product_milk.check_quantity(product_milk.quantity)

    def test_product_check_quantity_more(self, product_milk):
        # Напишите проверки на метод check_quantity
        assert not product_milk.check_quantity(product_milk.quantity + 1)

    def test_product_buy(self, product_milk):
        # Напишите проверки на метод buy
        quantity_before = product_milk.quantity
        buy_amount = 444
        product_milk.buy(buy_amount)
        assert product_milk.quantity == quantity_before - buy_amount

    def test_product_buy_more_than_available(self, product_milk):
        #  Напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError, match='Недостаточно товара в наличии'):
            product_milk.buy(product_milk.quantity + 1)


class TestCart:
    """
        Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_add_product_once(self, product_milk, cart):
        buy_count = 39
        cart.add_product(product_milk, buy_count)
        assert cart.products[product_milk] == buy_count

    def test_cart_add_product_twice(self, product_milk, cart):
        buy_count_1 = 47
        buy_count_2 = 33
        cart.add_product(product_milk, buy_count_1)
        assert cart.products[product_milk] == buy_count_1
        cart.add_product(product_milk, buy_count_2)
        assert cart.products[product_milk] == buy_count_1 + buy_count_2

    def test_cart_add_zero_product_(self, product_milk, cart):
        buy_count = 0
        cart.add_product(product_milk, buy_count)
        assert not cart.products

    def test_cart_add_two_products(self, product_milk, product_bread, cart):
        buy_count_milk = 12
        buy_count_bread = 34
        cart.add_product(product_milk, buy_count_milk)
        cart.add_product(product_bread, buy_count_bread)
        assert cart.products[product_milk] == buy_count_milk
        assert cart.products[product_bread] == buy_count_bread

    def test_cart_remove_product_with_remove_count_less(self, product_milk, cart):
        buy_count = 55
        remove_count = buy_count - 1
        cart.add_product(product_milk, buy_count)
        cart.remove_product(product_milk, remove_count)
        assert cart.products[product_milk] == buy_count - remove_count

    def test_cart_remove_product_without_remove_count(self, product_milk, cart):
        buy_count = 51
        cart.add_product(product_milk, buy_count)
        cart.remove_product(product_milk)
        assert not cart.products

    def test_cart_remove_product_with_remove_count_over(self, product_milk, cart):
        buy_count = 52
        cart.add_product(product_milk, buy_count)
        cart.remove_product(product_milk, buy_count + 1)
        assert not cart.products

    def test_cart_remove_one_of_two_products(self, product_milk, product_bread, cart):
        buy_count = 53
        cart.add_product(product_milk, buy_count)
        cart.add_product(product_bread, buy_count)
        cart.remove_product(product_milk)
        assert product_milk not in cart.products
        assert cart.products[product_bread] == buy_count

    def test_cart_remove_absent_product(self, product_milk, product_bread, cart):
        buy_count = 54
        cart.add_product(product_bread, buy_count)
        cart.remove_product(product_milk)
        assert product_milk not in cart.products
        assert cart.products[product_bread] == buy_count

    def test_cart_remove_product_from_empty_card(self, product_milk, cart):
        cart.remove_product(product_milk)
        assert not cart.products

    def test_cart_clear(self, product_milk, cart):
        buy_count = 55
        cart.add_product(product_milk, buy_count)
        cart.clear()
        assert not cart.products

    def test_cart_empty_clear(self, product_milk, cart):
        cart.clear()
        assert not cart.products

    def test_cart_get_total_price_one_product(self, product_milk, cart):
        buy_count = 56
        cart.add_product(product_milk, buy_count)
        assert cart.get_total_price() == product_milk.price * buy_count

    def test_cart_get_total_price_two_products(self, product_milk, product_bread, cart):
        buy_count_milk = 57
        buy_count_bread = 58
        cart.add_product(product_milk, buy_count_milk)
        cart.add_product(product_bread, buy_count_bread)
        assert (cart.get_total_price() == product_milk.price *
                                          buy_count_milk +
                                          product_bread.price *
                                          buy_count_bread)

    def test_cart_get_total_price_empty(self, cart):
        assert cart.get_total_price() == 0

    def test_cart_buy(self, product_milk, cart):
        buy_count = 59
        quantity_before = product_milk.quantity
        cart.add_product(product_milk, buy_count)
        cart.buy()
        assert product_milk.quantity == quantity_before - buy_count
        assert not cart.products

    def test_cart_buy_two_products(self, product_milk, product_bread, cart):
        buy_count = 60
        quantity_before_milk = product_milk.quantity
        quantity_before_bread = product_bread.quantity
        cart.add_product(product_milk, buy_count)
        cart.add_product(product_bread, buy_count)
        cart.buy()
        assert product_milk.quantity == quantity_before_milk - buy_count
        assert product_bread.quantity == quantity_before_bread - buy_count
        assert not cart.products

    def test_cart_buy_more_than_available(self, product_milk, cart):
        buy_count = product_milk.quantity + 1
        quantity_before = product_milk.quantity
        cart.add_product(product_milk, buy_count)
        with pytest.raises(ValueError):
            cart.buy()
        assert product_milk.quantity == quantity_before
        assert cart.products[product_milk] == buy_count

    def test_cart_buy_more_than_available_one_of_two_products(self, product_milk,
        product_bread, cart):
        buy_count_bread = product_bread.quantity + 1
        quantity_before_bread = product_bread.quantity
        quantity_before_milk = product_milk.quantity
        buy_count_milk = 5
        cart.add_product(product_milk, buy_count_milk)
        cart.add_product(product_bread, buy_count_bread)
        with pytest.raises(ValueError):
            cart.buy()
        assert product_bread.quantity == quantity_before_bread
        assert product_milk.quantity == quantity_before_milk
        assert cart.products[product_bread] == buy_count_bread
        assert cart.products[product_milk] == buy_count_milk

    def test_cart_buy_empty(self, cart):
        with pytest.raises(ValueError, match='Ваша корзина пустая'):
            cart.buy()