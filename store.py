"""
Store module for Best Buy store management system.

This module contains the Store class which manages a collection of products.
The store can add/remove products, track total inventory, and process orders
for multiple products at once.
"""

import products  # Imports 'Product' class from 'products.py'


class Store:
    """
    Represents a store that manages multiple products.
    """

    def __init__(self, products_list: list) -> None:
        """
        Creates a new store with an initial list of products.
        """
        self.products = products_list

    def add_product(self, product) -> None:
        """
        Adds a product to the store inventory.
        """
        self.products.append(product)

    def remove_product(self, product) -> None:
        """
        Removes a product from store.
        """
        # Checks if product exists in the list
        if product in self.products:
            self.products.remove(product)

    def get_total_quantity(self) -> int:
        """
        Returns how many items are in the store in total.
        """
        total = 0  # Counter variable
        for product in self.products:
            total += product.get_quantity()
        return total

    def get_all_products(self) -> list:
        """
        Returns all products in the store that are active.
        """
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products

    def order(self, shopping_list: list) -> float:
        """
        Gets a list of tuples where each tuple has 2 items:
         - Product (Product class)
         - Quantity (int).
        Buys the products and returns the total price of the order.
        """
        total_price = 0.0  # Counter variable

        # Process each item in the shopping list
        for item in shopping_list:
            # Extract product and quantity from tuple
            product = item[0]
            quantity = item[1]

            # Try to buy the product
            try:
                # Buy returns the price for this purchase
                item_price = product.buy(quantity)
                total_price += item_price
            except ValueError as e:
                # If there's an error, print it and continue
                print(f"Error ordering {product.get_name()}: {e}")

        return total_price


def main():
    """
    Test function for the Store class as specified in the assignment.
    """
    # Create test products as specified
    product_list = [
        products.Product(
            "MacBook Air M2",
            price=1450,
            quantity=100
            ),
        products.Product(
            "Bose QuietComfort Earbuds",
            price=250,
            quantity=500
            ),
        products.Product(
            "Google Pixel 7",
            price=500,
            quantity=250
            ),
        ]

    # Create store instance
    best_buy = Store(product_list)

    # Get all products
    products_in_store = best_buy.get_all_products()

    # Test and print total quantity
    print(best_buy.get_total_quantity())

    # Creates a shopping list with 'MacBook' and 'Bose earbuds':
    shopping_list = [
        (products_in_store[0], 1),  # 'MacBook Air M2'
        (products_in_store[1], 2)  # 'Bose QuietComfort Earbuds'
        ]

    # Process the order using the shopping list
    order_total = best_buy.order(shopping_list)
    print(order_total)


# Only runs main() if this file is executed directly
if __name__ == "__main__":
    main()
