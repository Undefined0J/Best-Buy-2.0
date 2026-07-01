"""
Unit tests for the Product class using pytest.
"""

import pytest
from products import Product


def test_create_normal_product() -> None:
    """
    Test that creating a normal product works and attributes are set correctly.
    """
    product = Product("MacBook Air M2", price=1450.0, quantity=100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450.0
    assert product.quantity == 100
    assert product.is_active() is True


def test_create_product_invalid_details() -> None:
    """
    Test that creating a product with invalid details raises a ValueError.
    """
    # Test empty name
    with pytest.raises(ValueError):
        Product("", price=1450.0, quantity=100)

    # Test negative price
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10.0, quantity=100)

    # Test negative quantity (extra safety)
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=1450.0, quantity=-5)


def test_product_becomes_inactive() -> None:
    """
    Test that a product becomes inactive when its quantity reaches 0.
    """
    product = Product("MacBook Air M2", price=1450.0, quantity=1)
    product.buy(1)

    assert product.get_quantity() == 0
    assert product.is_active() is False


def test_product_purchase_modifies_quantity_and_returns_correct_price() -> None:
    """
    Test that purchasing modifies the quantity and returns the correct total price.
    """
    product = Product("MacBook Air M2", price=1450.0, quantity=100)
    total_price = product.buy(2)

    assert total_price == 2900.0
    assert product.get_quantity() == 98


def test_buy_too_much_raises_exception() -> None:
    """
    Test that buying a larger quantity than available raises a ValueError.
    """
    product = Product("MacBook Air M2", price=1450.0, quantity=10)

    with pytest.raises(ValueError):
        product.buy(11)
