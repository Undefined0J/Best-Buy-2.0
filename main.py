"""
Main execution module for the Best Buy store application.
Handles the user interface and application loop.
"""

import sys
import promotions
from products import Product, NonStockedProduct, LimitedProduct
from store import Store


def _display_menu() -> None:
    """
    Print the store menu options to the console.
    """
    print("\n   Store Menu")
    print("   ----------")
    print("1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit")


def _handle_list_products(store_obj: Store) -> None:
    """
    Display all active products available in the store.

    :param store_obj: The active store instance.
    """
    products = store_obj.get_all_products()
    if not products:
        print("\n------")
        print("No active products available in the store.")
        print("------")
        return

    print("------")
    for index, product in enumerate(products, start=1):
        # Dynamically use the polymorphic show() method of each product type
        print(f"{index}. {product.show()}")
    print("------")


def _handle_total_amount(store_obj: Store) -> None:
    """
    Display the total item count currently in stock.

    :param store_obj: The active store instance.
    """
    total_quantity = store_obj.get_total_quantity()
    print(f"Total of {total_quantity} items in store")


def _handle_make_order(store_obj: Store) -> None:
    """
    Guide the user through the process of making an order.

    :param store_obj: The active store instance.
    """
    products = store_obj.get_all_products()
    if not products:
        print("No products available to order.")
        return

    _handle_list_products(store_obj)
    print("When you want to finish order, enter empty text.")

    shopping_list = []
    while True:
        product_num_input = input("Which product # do you want? ").strip()
        # Exit ordering loop if input is empty
        if not product_num_input:
            break

        amount_input = input("What amount do you want? ").strip()
        if not amount_input:
            break

        try:
            product_index = int(product_num_input) - 1
            quantity = int(amount_input)

            # Validate list boundaries
            if product_index < 0 or product_index >= len(products):
                print("Invalid product number. Please select from the list.\n")
                continue

            selected_product = products[product_index]
            shopping_list.append((selected_product, quantity))
            print("Product added to list!\n")

        except ValueError:
            print("Invalid input format. Please enter numerical values.\n")

    if not shopping_list:
        print("No items ordered.")
        return

    try:
        # Process total order transaction
        total_payment = store_obj.order(shopping_list)
        print("********")
        print(f"Order made! Total payment: ${total_payment:.0f}")
    except ValueError as error:
        print(f"Order failed: {error}")


def start(store_obj: Store) -> None:
    """
    Start the interactive store engine loop.

    :param store_obj: The initialized store instance.
    """
    while True:
        _display_menu()
        user_choice = input("Please choose a number: ").strip()

        if user_choice == "1":
            _handle_list_products(store_obj)
        elif user_choice == "2":
            _handle_total_amount(store_obj)
        elif user_choice == "3":
            _handle_make_order(store_obj)
        elif user_choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def main() -> None:
    """
    Main entry point of the application. Initialises inventory and starts the UI.
    """
    product_list = [
        Product("MacBook Air M2", price=1450.0, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250.0, quantity=500),
        Product("Google Pixel 7", price=500.0, quantity=250),
        NonStockedProduct("Windows License", price=125.0),
        LimitedProduct("Shipping", price=10.0, quantity=250, maximum=1)
    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
