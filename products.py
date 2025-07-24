"""
Product module for Best Buy store management system.

This module contains the Product class and subclasses which
represent different types of items available in the store. Each product type
has specific behavior for inventory management and purchasing.
"""


class Product:
    """
    Represents a product available in the Best Buy store.
    """

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """
        Creates a new product with validation. Raises ValueError if name is
        empty. Raises ValueError if price or quantity are negative.
        """
        # Validate name is not empty
        if not name:
            raise ValueError("Product name cannot be empty")

        # Validate price is not negative
        if price < 0:
            raise ValueError("Product price cannot be negative")

        # Validate quantity is not negative
        if quantity < 0:
            raise ValueError("Product quantity cannot be negative")

        # If all validations pass, create the product
        self.name = name
        self.price = price
        self.quantity = quantity
        if quantity > 0:  # Set active status based on quantity
            self.active = True
        else:
            self.active = False

        # Initialize promotion as None
        self.promotion = None

    def get_quantity(self) -> int:
        """
        Returns the current quantity of the product.
        """
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """
        Updates the product quantity and deactivates if it reaches 0.
        """
        self.quantity = quantity

        # If quantity reaches 0, deactivates the product
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """
        Returns True if the product is active, False otherwise.
        """
        return self.active

    def activate(self) -> None:
        """
        Activates the product so it can be sold.
        """
        self.active = True

    def deactivate(self) -> None:
        """
        Deactivates the product so it cannot be sold.
        """
        self.active = False

    def get_promotion(self):
        """
        Returns the current promotion for this product.
        """
        return self.promotion

    def set_promotion(self, promotion) -> None:
        """
        Sets or removes a promotion for this product.
        """
        self.promotion = promotion

    def show(self) -> str:
        """
        Returns a string representation of the product.
        """
        product_info = (f"{self.name}, "
                        f"Price: {self.price}, "
                        f"Quantity: {self.quantity}")
        # Add promotion info if exists
        if self.promotion:
            product_info += f", Promotion: {self.promotion.name}"
        return product_info

    def get_name(self) -> str:
        """
        Returns the product name.
        """
        return self.name

    def get_price(self) -> float:
        """
        Returns the product price.
        """
        return self.price

    def buy(self, quantity: int) -> float:
        """
        Buys a specified quantity of Product. Returns the total price of the
        purchase. Updates the product quantity. Raises ValueError if there
        are any logical issues.
        """
        # Checks if quantity is valid (not negative or zero)
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than 0")

        # Checks if product is active
        if not self.active:
            raise ValueError("Product is not active")

        # Checks if there is enough quantity in stock
        if quantity > self.quantity:
            raise ValueError(f"Only {self.quantity} items available")

        # Calculate price with promotion if exists
        if self.promotion:
            # Use promotion to calculate price
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            # No promotion - use regular price
            total_price = self.price * quantity

        # Updates the quantity
        new_quantity = self.quantity - quantity
        self.set_quantity(new_quantity)

        # Return the total price
        return total_price


class NonStockedProduct(Product):
    """
    Represents a product that doesn't require stock tracking (like software 
    licenses). Quantity is always 0 but the product remains active.
    """

    def __init__(self, name: str, price: float) -> None:
        """
        Creates a non-stocked product. Note: no quantity parameter needed.
        """
        # Call parent's __init__ with quantity always set to 0
        super().__init__(name, price, quantity=0)
        self.active = True  # Overrides status: non-stock is always 'active'

    def set_quantity(self, quantity: int) -> None:
        """
        Override to prevent quantity changes. Non-stocked products
        always have quantity 0.
        """
        pass  # Do nothing - quantity stays '0'

    def show(self) -> str:
        """
        Shows product information with indication it's non-stocked.
        """
        # Overrides parent's show method, adding the 'special characteristics'
        return f"{super().show()} (Non-Stocked)"

    def buy(self, quantity: int) -> float:
        """
        Allows purchase of any quantity --> stock is unlimited.
        """
        if quantity <= 0:  # Validates quantity is positive
            raise ValueError("Purchase quantity must be greater than 0")
        # Calculate price with promotion if exists
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity
        # Note: Quantity not updated as product is 'non-stock'
        return total_price


class LimitedProduct(Product):
    """
    Represents a product that can only be purchased in limited quantities
    per order (e.g., shipping fees that can only be added once).
    """

    def __init__(
            self,
            name: str,
            price: float,
            quantity: int,
            maximum: int
            ) -> None:
        """
        Creates a limited product with a maximum purchase quantity per order.
        """
        # Call parent's __init__ first
        super().__init__(name, price, quantity)
        # Add the new maximum attribute
        self.maximum = maximum

    def show(self) -> str:
        """
        Shows product information including purchase limit.
        """
        # Get parent's show output and add limit info
        return f"{super().show()} (Limited to {self.maximum} per order)"

    def buy(self, quantity: int) -> float:
        """
        Processes purchase with 'maximum quantity' enforcement.
        """
        if quantity > self.maximum:  # Check if quantity > limited maximum
            raise ValueError(
                f"Cannot purchase more than {self.maximum} "
                f"of '{self.name}' per order"
                )
        return super().buy(quantity)  # If in limit, use parent's buy method


if __name__ == "__main__":  # Test code
    # Test the new product types

    # Test NonStockedProduct
    print("Testing NonStockedProduct:")
    windows = NonStockedProduct("Windows License", price=125)
    print(windows.show())  # Should show (Non-Stocked)
    print(f"Active: {windows.is_active()}")  # Should be True
    print(f"Quantity: {windows.get_quantity()}")  # Should be 0

    # Try to buy licenses
    total = windows.buy(3)
    print(f"Bought 3 licenses for ${total}")  # Should be $375
    print(f"Quantity after purchase: {windows.get_quantity()}")  # Still 0
    print(f"\n{'=' * 40}\n")

    # Test LimitedProduct
    print("Testing LimitedProduct:")
    shipping = LimitedProduct(
        "Shipping",
        price=10,
        quantity=250,
        maximum=1
        )
    print(shipping.show())  # Should show (Limited to 1 per order)

    # Try to buy within limit
    total = shipping.buy(1)
    print(f"Bought 1 shipping for ${total}")  # Should output $10

    # Try to buy more than limit
    try:
        shipping.buy(2)  # Should raise error
    except ValueError as e:
        print(f"Error: {e}")  # Should print limit error
