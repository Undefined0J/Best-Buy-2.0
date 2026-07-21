"""
Product module for Best Buy store.
Contains the Product class for managing inventory items.
"""

from typing import Optional
from promotions import Promotion


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
        self.promotion: Optional[Promotion] = None

    def get_quantity(self) -> int:
        """
        Get the current quantity of the product.

        :return: The current quantity as an integer.
        """
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """
        Set a new quantity for the product.
        Deactivates the product if quantity reaches 0.

        :param quantity: The new stock quantity.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """
        Check if the product is active.

        :return: True if the product is active, False otherwise.
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

    def get_promotion(self) -> Optional[Promotion]:
        """
        Get the current promotion of the product.

        :return: The active Promotion instance or None.
        """
        return self.promotion

    def set_promotion(self, promotion: Optional[Promotion]) -> None:
        """
        Set a new promotion for the product.

        :param promotion: The Promotion instance to apply.
        """
        self.promotion = promotion

    def show(self) -> str:
        """
        Return a string representation of the product, including promotion if active.

        :return: Formatted string detailing the product's attributes.
        """
        promo_text = self.promotion.name if self.promotion else "None"
        return (f"{self.name}, Price: ${self.price:.0f}, Quantity: "
                f"{self.quantity}, Promotion: {promo_text}")

    def check_purchase(self, quantity: int) -> None:
        """
        Validate if the given quantity can be purchased.
        Raises ValueError if rules are violated.

        :param quantity: The desired purchase amount.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to buy must be a positive integer.")
        if not self.is_active():
            raise ValueError("Product is currently inactive and cannot be bought.")
        if quantity > self.quantity:
            raise ValueError(f"Not enough stock available for '{self.name}'.")

    def buy(self, quantity: int) -> float:
        """
        Buy a specific quantity of the product.
        Delegates rule validation to check_purchase().

        :param quantity: The amount to buy.
        :return: The total price of the purchase.
        """
        self.check_purchase(quantity)

        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity

        self.set_quantity(self.quantity - quantity)

        return total_price


class NonStockedProduct(Product):
    """
    Represents a digital or non-physical product with unlimited quantity.
    """

    def __init__(self, name: str, price: float) -> None:
        """
        Initialize a new NonStockedProduct instance with 0 quantity.

        :param name: The name of the product.
        :param price: The price of the product.
        """
        super().__init__(name, price, quantity=0)

    def show(self) -> str:
        """
        Return a string representation specifying unlimited quantity.

        :return: Formatted string detailing the product's attributes.
        """
        promo_text = self.promotion.name if self.promotion else "None"
        return (f"{self.name}, Price: ${self.price:.0f}, "
                f"Quantity: Unlimited, Promotion: {promo_text}")

    def check_purchase(self, quantity: int) -> None:
        """
        Validates purchase without checking stock limitations.

        :param quantity: The desired purchase amount.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity to buy must be a positive integer.")
        if not self.is_active():
            raise ValueError("Product is currently inactive and cannot be bought.")

    def buy(self, quantity: int) -> float:
        """
        Buy a specific quantity of the non-stocked product.

        :param quantity: The amount to buy.
        :return: The total price of the purchase.
        """
        self.check_purchase(quantity)
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity


class LimitedProduct(Product):
    """
    Represents a product that has a restriction on the maximum quantity per order.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int) -> None:
        """
        Initialize a new LimitedProduct instance.

        :param name: The name of the product.
        :param price: The price of the product.
        :param quantity: The available quantity in the store.
        :param maximum: The maximum allowed quantity per order.
        """
        super().__init__(name, price, quantity)
        if not isinstance(maximum, int) or maximum <= 0:
            raise ValueError("Maximum order limit must be a positive integer.")
        self._maximum = maximum

    def show(self) -> str:
        """
        Return a string representation specifying the order limit restriction.

        :return: Formatted string detailing the product's attributes.
        """
        promo_text = self.promotion.name if self.promotion else "None"
        return (f"{self.name}, Price: ${self.price:.0f}, Quantity: {self.quantity}, "
                f"Limited to {self._maximum} per order!, Promotion: {promo_text}")

    def check_purchase(self, quantity: int) -> None:
        """
        Validates purchase including the maximum limit per order.

        :param quantity: The desired purchase amount.
        """
        if isinstance(quantity, int) and quantity > self._maximum:
            raise ValueError(f"Processing failed: Maximum allowed quantity "
                             f"for this item is {self._maximum} per order.")
        super().check_purchase(quantity)
