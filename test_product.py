"""
Unit tests for the Product class.

This module tests all functionality of the Product class including
normal operations and error handling.
"""

import pytest

from products import Product  # Import the Product class for testing


def test_create_product_with_valid_data():
    """
    Tests that creating a product with valid data works.
    """
    # Creates a product with valid data
    product = Product("MacBook Air M2", price=1450, quantity=100)
    # Checks all attributes were set correctly
    assert product.get_name() == "MacBook Air M2"
    assert product.get_price() == 1450
    assert product.get_quantity() == 100
    assert product.is_active() is True  # Should be active with quantity > 0


def test_create_product_with_empty_name_raises_exception():
    """
    Tests that empty product name raises ValueError.
    """
    # Should raise a ValueError
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)


def test_create_product_with_negative_price_raises_exception():
    """
    Tests that negative price raises ValueError.
    """
    # Should raise a ValueError
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_create_product_with_negative_quantity_raises_exception():
    """
    Tests that negative quantity raises ValueError.
    """
    # Should raise a ValueError
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=1450, quantity=-5)


def test_product_becomes_inactive_at_zero_quantity():
    """
    Tests that when a product reaches 0 quantity, it becomes inactive.
    """
    # Creates a product with a specified quantity
    product = Product("iPhone 14", price=999, quantity=1)
    assert product.is_active() is True  # Verifies product is active initially
    product.set_quantity(0)  # Sets quantity to 0
    assert product.is_active() is False  # Checks product is inactive
    assert product.get_quantity() == 0  # Checks product is inactive


def test_product_purchase_modifies_quantity_and_returns_correct_price():
    """
    Tests that product purchase modifies the quantity and returns the correct
    output.
    """
    product = Product(
        "Bose QuietComfort Earbuds",
        price=250,
        quantity=500
        )
    total_price = product.buy(50)  # Buy 50 units
    assert total_price == 12500.0  # Checks total price is correct (50 * 250)
    assert product.get_quantity() == 450  # Checks quantity was reduced
    assert product.is_active() is True  # Product should still be active


def test_buying_exact_quantity_deactivates_product():
    """
    Tests that buying all available quantity deactivates the product.
    """
    # Creates a product with limited quantity
    product = Product("Google Pixel 7", price=500, quantity=5)
    # Buy all 5 units
    total_price = product.buy(5)
    # Checks price and deactivation
    assert total_price == 2500.0
    assert product.get_quantity() == 0
    assert product.is_active() is False


def test_buying_larger_quantity_than_available_raises_exception():
    """
    Tests that buying a larger quantity than exists invokes exception.
    """
    # Creates a product with limited stock
    product = Product("Laptop Stand", price=50, quantity=3)
    # Try to buy more than available
    with pytest.raises(ValueError):
        product.buy(10)  # Only 3 available!
    # Verify quantity didn't change
    assert product.get_quantity() == 3


def test_buying_from_inactive_product_raises_exception():
    """
    Tests that buying from an inactive product raises ValueError.
    """
    # Creates and deactivates a product
    product = Product("Old Stock Item", price=10, quantity=0)
    assert product.is_active() is False  # Verify product is inactive
    with pytest.raises(ValueError):  # Try to buy from inactive product
        product.buy(1)


def test_buying_zero_or_negative_quantity_raises_exception():
    """
    Tests that buying zero or negative quantity raises ValueError.
    """
    product = Product("USB Cable", price=15, quantity=100)
    with pytest.raises(ValueError):  # Test buying 0 items
        product.buy(0)
    with pytest.raises(ValueError):  # Test buying negative quantity
        product.buy(-5)
