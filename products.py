"""
Product module for Best Buy store.
Contains the Product class for managing inventory items.
"""


class Product:
    """
    Represents a specific product available in the store.
    """

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """
        Initialize a new Product instance.

        :param name: The name of the product.
        :param price: The price of the product.
        :param quantity: The available quantity in the store.
        :raises ValueError: If name is empty, price is negative, or quantity is negative.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Product price cannot be negative.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Product quantity cannot be negative.")

        self.name = name.strip()
        self.price = float(price)
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> int:
        """
        Get the current quantity of the product.

        :return: The current quantity.
        """
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """
        Set a new quantity for the product.
        Deactivates the product if quantity reaches 0.

        :param quantity: The new quantity to set.
        :raises ValueError: If the new quantity is negative.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """
        Check if the product is active.

        :return: True if active, False otherwise.
        """
        return self.active

    def activate(self) -> None:
        """
        Activate the product.
        """
        self.active = True

    def deactivate(self) -> None:
        """
        Deactivate the product.
        """
        self.active = False

    def show(self) -> str:
        """
        Return a string representation of the product.

        :return: Formatted string representing the product details.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        Buy a specific quantity of the product.

        :param quantity: The amount to buy.
        :return: The total price of the purchase.
        :raises ValueError: If quantity is invalid, exceeds stock, or product is inactive.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to buy must be a positive integer.")
        if not self.is_active():
            raise ValueError("Product is currently inactive and cannot be bought.")
        if quantity > self.quantity:
            raise ValueError("Not enough stock available.")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)

        return total_price


def main() -> None:
    """
    Main execution function for testing the Product class.
    """
    bose = Product("Bose QuietComfort Earbuds", price=250.0, quantity=500)
    mac = Product("MacBook Air M2", price=1450.0, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    print(bose.show())
    print(mac.show())

    bose.set_quantity(1000)
    print(bose.show())


if __name__ == "__main__":
    main()
