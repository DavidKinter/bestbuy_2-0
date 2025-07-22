"""
Product module for Best Buy store management system.

This module contains the Product class which represents items available
in the store. Each product has a name, price, quantity, and active status.
Products can be purchased, activated/deactivated, and displayed (shown).
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

    def show(self) -> str:
        """
        Returns a string representation of the product.
        """
        product_info = (f"{self.name}, "
                        f"Price: {self.price}, "
                        f"Quantity: {self.quantity}")
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

        # Calculates the total price
        total_price = self.price * quantity

        # Updates the quantity
        new_quantity = self.quantity - quantity
        self.set_quantity(new_quantity)

        # Return the total price
        return total_price


if __name__ == "__main__":  # Test code
    # Create test products
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    # Test buying products
    print(bose.buy(50))  # Should print 12500.0
    print(mac.buy(100))  # Should print 145000.0
    print(mac.is_active())  # Should print False (quantity is now 0)

    # Test show method
    print(bose.show())  # Should show updated quantity
    print(mac.show())  # Should show 0 quantity

    # Test set_quantity
    bose.set_quantity(1000)
    print(bose.show())  # Should show new quantity of 1000
