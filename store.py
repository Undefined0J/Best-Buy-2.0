"""
Store module for Best Buy store.
Contains the Store class for managing a collection of products.
"""

from typing import List, Tuple
from products import Product, NonStockedProduct


class Store:
    """
    Represents a store containing multiple products.
    """

    def __init__(self, product_list: List[Product]) -> None:
        """
        Initialize the Store with a list of products.

        :param product_list: Initial list of products in the store.
        """
        self.products: List[Product] = []
        if isinstance(product_list, list):
            for product in product_list:
                self.add_product(product)

    def add_product(self, product: Product) -> None:
        """
        Add a product to the store.

        :param product: The product to add.
        """
        if isinstance(product, Product):
            self.products.append(product)

    def remove_product(self, product: Product) -> None:
        """
        Remove a product from the store.

        :param product: The product to remove.
        """
        if product in self.products:
            self.products.remove(product)

    def get_total_quantity(self) -> int:
        """
        Get the total quantity of all items in the store.

        :return: Total quantity of all items.
        """
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self) -> List[Product]:
        """
        Get all active products in the store.

        :return: List of active products.
        """
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: List[Tuple[Product, int]]) -> float:
        """
        Process an order for a list of products.
        Implements a dry-run check to prevent partial transactions on failure.

        :param shopping_list: List of tuples containing (Product, quantity).
        :return: Total cost of the order.
        :raises ValueError: If formatting is wrong, stock is insufficient, or a product is inactive.
        """
        total_price = 0.0

        # Dry Run: Validate the entire order before making any changes
        for product, quantity in shopping_list:
            if not isinstance(product, Product) or not isinstance(quantity, int):
                raise ValueError("Invalid shopping list item format.")
            if quantity < 0:
                raise ValueError("Order quantity cannot be negative.")
            if not product.is_active():
                raise ValueError(f"Product '{product.name}' is inactive.")

            # Skip stock check ONLY if it is not a non-stocked product
            if not isinstance(product, NonStockedProduct):
                if quantity > product.get_quantity():
                    raise ValueError(f"Not enough stock for '{product.name}'.")

        # Execution: Process purchases after validation
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)

        return total_price


def main() -> None:
    """
    Main execution function for testing the Store class.
    """
    try:
        product_list = [
            Product("MacBook Air M2", price=1450.0, quantity=100),
            Product("Bose QuietComfort Earbuds", price=250.0, quantity=500),
            Product("Google Pixel 7", price=500.0, quantity=250),
        ]

        best_buy = Store(product_list)
        products = best_buy.get_all_products()

        print(best_buy.get_total_quantity())
        print(best_buy.order([(products[0], 1), (products[1], 2)]))

    except ValueError as e:
        print(f"Transaction failed due to business logic or input error: {e}")


if __name__ == "__main__":
    main()
