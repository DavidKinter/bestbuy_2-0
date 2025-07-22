"""
Best Buy Store Management System - Main Interface

This module provides a menu system for managing the Best Buy store. Users
can view products, check inventory totals, make orders, and quit the program.
"""

import products
import store


def display_menu() -> None:
    """
    Displays the main menu options to the user.
    """
    print("\n" + "=" * 40)
    print("Best Buy Store Menu".center(40))
    print("=" * 40)
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit")
    print("=" * 40)


def get_menu_choice() -> str:
    """
    Gets the user's menu choice and validates it.
    """
    valid_choices = ["1", "2", "3", "4"]  # User input choices
    choice = input("Please choose an option (1-4): ").strip()
    # Validate the choice
    while choice not in valid_choices:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        choice = input("Please choose an option (1-4): ").strip()
    return choice


def get_active_products(store_obj: store.Store) -> list:
    """
    Gets active products from store and handles empty case.
    """
    active_products = store_obj.get_all_products()
    if not active_products:
        print("No products currently available.")
    return active_products


def display_numbered_products(products_list: list, format_func=None) -> None:
    """
    Displays a numbered list of products using specified format.
    """
    product_number = 1  # Counter variable
    for product in products_list:
        if format_func:
            print(f"{product_number}. {format_func(product)}")
        else:
            print(f"{product_number}. {product.show()}")
        product_number += 1


def format_price(product) -> str:
    """
    Formats product with name and price.
    """
    return f"{product.get_name()}, ${product.get_price():,.2f}"


def format_quantity(product) -> str:
    """
    Formats product with name and quantity.
    """
    return f"{product.get_name()}: {product.get_quantity()} items"


def print_section_header(title: str) -> None:
    """
    Prints a formatted section header.
    """
    print(f"\n--- {title} ---")


def list_all_products(store_obj: store.Store) -> None:
    """
    Lists all active products in the store.
    """
    print_section_header("Products Available in Store")
    active_products = get_active_products(store_obj)
    if active_products:
        display_numbered_products(active_products, format_price)


def show_total_quantity(store_obj: store.Store) -> None:
    """
    Displays the quantity of all active items in the store.
    """
    print_section_header("Product Quantities in Store")
    active_products = get_active_products(store_obj)
    if active_products:
        # Shows quantity of individual products
        display_numbered_products(active_products, format_quantity)
        # Shows total quantity
        total_quantity = store_obj.get_total_quantity()
        print(f"\nTotal items in store: {total_quantity}")


def validate_num_input(input_str: str, input_type: str) -> int:
    """
    Validates that input is a positive integer.
    """
    if not input_str.isdigit():
        print(f"Please enter a valid {input_type}.")
        return None
    num_input = int(input_str)
    if num_input <= 0:
        print(f"{input_type.capitalize()} must be greater than 0.")
        return None
    return num_input


def get_product_selection(max_products: int) -> int:
    """
    Gets and validates product selection.
    """
    product_choice = input(
        "\nEnter product number (or press Enter to finish):"
        ).strip()
    # Checks if user wants to finish
    if not product_choice:
        return -1  # Breaks loop in build_cart 'if product_index == -1:'

    # Validate input is a number
    if not product_choice.isdigit():
        print("Please enter a valid number.")
        return None

    product_index = int(product_choice) - 1  # Convert to 0-based indexing
    # Check if index is valid --> cannot be "<1" or "> # active products"
    if not 0 <= product_index < max_products:
        print(f"Please enter a number between 1 and {max_products}.")
        return None
    return product_index


def get_quantity_from_user() -> int:
    """
    Gets and validates quantity from user input.
    """
    quantity_str = input("Enter quantity: ").strip()
    return validate_num_input(quantity_str, "quantity")


def check_availability(product, requested_qty: int, cart_qty: int) -> bool:
    """
    Checks if requested quantity is available based on shopping cart.
    """
    available_qty = product.get_quantity()
    remaining_qty = available_qty - cart_qty
    if requested_qty > remaining_qty:
        if cart_qty > 0:
            print(
                f"Error: Only {remaining_qty} items available "
                f"({cart_qty} already in cart)."
                )
        else:
            print(f"Error: Only {available_qty} items available.")
        return False
    return True


def build_cart(active_products: list) -> list:
    """
    Builds cart through user interaction.
    """
    cart = []
    cart_quantities = {}  # Track quantities in cart

    while True:
        # Get product selection for cart
        product_index = get_product_selection(len(active_products))
        if product_index == -1:  # User wants to finish
            break
        if product_index is None:  # Invalid input
            continue
        # Get quantity
        quantity = get_quantity_from_user()
        if quantity is None:  # Invalid input
            continue
        # Check availability
        selected_product = active_products[product_index]
        already_in_cart = cart_quantities.get(product_index, 0)
        if not check_availability(selected_product, quantity, already_in_cart):
            continue
        # Add to cart and update quantities
        cart.append((selected_product, quantity))
        cart_quantities[product_index] = already_in_cart + quantity
        print(f"Added {quantity} x {selected_product.show()}")

    return cart


def process_order(store_obj: store.Store, cart: list) -> None:
    """
    Processes the order and displays result.
    """
    if not cart:
        print("No items in order.")
        return
    try:
        total_price = store_obj.order(cart)
        print(f"\nOrder complete! Total cost: ${total_price:,.2f}")
    except ValueError as e:
        print(f"Error processing order: {e}")
    except AttributeError as e:
        # In case of programming errors with objects
        print(f"System error: {e}")


def make_order(store_obj: store.Store) -> None:
    """
    Handles the order process, allowing users to select products and
    quantities.
    """
    print_section_header("Make an Order")
    # Get and display available products
    active_products = get_active_products(store_obj)
    if not active_products:
        return
    print("\nAvailable products:")
    display_numbered_products(active_products)

    # Build and process order
    cart = build_cart(active_products)
    process_order(store_obj, cart)


def quit_program(store_obj: store.Store) -> None:
    """
    Displays exit message and quits program. The 'store_obj' parameter is
    required for proper functioning when called in 'call_menu_action'.
    Would otherwise raise TypeError.
    """
    print("\nThank you for using Best Buy Store Management System!")
    print("Goodbye!")


def call_menu_action(store_obj: store.Store, choice: str) -> None:
    """
    Calls the appropriate menu action based on user choice.
    """
    menu_actions = {
        "1": list_all_products,
        "2": show_total_quantity,
        "3": make_order,
        "4": quit_program
        }
    action = menu_actions.get(choice)
    if action:
        action(store_obj)
    else:
        print("Invalid choice. Please try again.")


def start(store_obj: store.Store) -> None:
    """
    Runs menu execution.
    """
    print("Welcome to Best Buy Store Management System!")
    while True:
        display_menu()
        choice = get_menu_choice()
        call_menu_action(store_obj, choice)
        if choice == "4":  # Exit if user chose quit
            break
        # Pause before showing menu again
        input("\nPress Enter to continue...")


def main() -> None:
    """
    Main program entry point. Sets up the store and starts the menu.
    """
    # Creates initial inventory
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
            )
        ]
    # Creates store
    best_buy = store.Store(product_list)
    # Starts the menu
    start(best_buy)


if __name__ == "__main__":
    main()
