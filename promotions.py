"""
Promotions module for Best Buy store management system.

This module contains the abstract Promotion class and concrete promotion
implementations for different discount strategies.
"""

from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    Abstract base class for all promotions.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes promotion with a name.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """
        Abstract method that must be implemented by all promotions.
        Calculates discounted price for given product and quantity.
        
        'pass' statement is unnecessary when you have a docstring in the 
        method body. The docstring itself serves as the method body.
        """


class PercentDiscount(Promotion):
    """
    Applies a percentage discount to the total price.
    For example: 30% off means customer pays 70% of original price.
    """

    def __init__(self, name: str, percent: float) -> None:
        """
        Creates a percentage discount promotion.
        """
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculates price after percentage discount.
        """
        # Calculate normal total price
        total_price = product.price * quantity
        # Apply discount (e.g., 30% off = pay 70%)
        discount_multiplier = (100 - self.percent) / 100
        discounted_price = total_price * discount_multiplier
        return discounted_price


class SecondHalfPrice(Promotion):
    """
    Every second item is 50% off.
    For example: Buy 2 items, pay full price for 1st, half for 2nd.
    """

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculates price where every second item is half price.
        """
        # Calculate quantity of full- and half-price items
        full_price_items = (quantity + 1) // 2  # Integer division
        half_price_items = quantity // 2

        # Calculate total
        total_price = (
                (full_price_items * product.price) + (
                half_price_items * product.price * 0.5)
        )
        return total_price


class ThirdOneFree(Promotion):
    """
    For every 3 items, customer only pays for 2.
    For example: Buy 3, pay for 2. Buy 6, pay for 4.
    """

    def apply_promotion(self, product, quantity: int) -> float:
        """
        Calculates price where every third item is free.
        """
        # For every 3 items, pay for only 2
        paid_items = (quantity // 3) * 2 + (quantity % 3)
        # Calculate total
        total_price = paid_items * product.price
        return total_price


if __name__ == "__main__":
    # Test the promotion calculations
    print("Testing Promotions:")
    print("=" * 40)


    # Create a mock product for testing
    class MockProduct:
        """Mock product class for testing promotions."""

        def __init__(self, price):
            self.price = price


    test_product = MockProduct(100)

    # Test PercentDiscount
    print("Testing 30% off:")
    percent_promo = PercentDiscount("30% off", percent=30)
    print(
        f"5 items at $100 each with 30% off: "
        f"${percent_promo.apply_promotion(test_product, 5)}"
        )
    # Should print $350 (500 * 0.7)

    # Test SecondHalfPrice
    print("\nTesting Second Half Price:")
    second_promo = SecondHalfPrice("Second Half Price")
    for qty in range(1, 6):
        promo_price = second_promo.apply_promotion(test_product, qty)
        print(f"{qty} items: ${promo_price}")
    # Should show: 1=$100, 2=$150, 3=$250, 4=$300, 5=$400

    # Test ThirdOneFree
    print("\nTesting Buy 2 Get 1 Free:")
    third_promo = ThirdOneFree("Buy 2 Get 1")
    for qty in range(1, 10):
        promo_price = third_promo.apply_promotion(test_product, qty)
        print(f"{qty} items: ${promo_price}")
    # Should show: 1=$100, 2=$200, 3=$200, 4=$300, 5=$400, 6=$400...
