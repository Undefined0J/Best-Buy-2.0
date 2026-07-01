"""
Promotions module for Best Buy store.
Contains the abstract Promotion class and concrete discount strategies.
"""

from abc import ABC, abstractmethod
from typing import Any


class Promotion(ABC):
    """
    Abstract base class for all product promotions.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the promotion with a name.

        :param name: The name of the promotional campaign.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product: Any, quantity: int) -> float:
        """
        Calculate the discounted price for a given product and quantity.

        :param product: The product instance being purchased.
        :param quantity: The amount of the product being purchased.
        :return: The total price after applying the promotion.
        """
        pass


class PercentDiscount(Promotion):
    """
    Applies a percentage discount to the total price of the product.
    """

    def __init__(self, name: str, percent: float) -> None:
        """
        Initialize the percentage discount.

        :param name: The name of the promotional campaign.
        :param percent: The discount percentage (0-100).
        :raises ValueError: If percent is out of valid range.
        """
        super().__init__(name)
        if not isinstance(percent, (int, float)) or percent < 0 or percent > 100:
            raise ValueError("Discount percent must be between 0 and 100.")
        self.percent = float(percent)

    def apply_promotion(self, product: Any, quantity: int) -> float:
        """
        Apply the percentage discount.
        """
        return (product.price * quantity) * (1 - (self.percent / 100))


class SecondHalfPrice(Promotion):
    """
    Every second item purchased is sold at half price.
    """

    def apply_promotion(self, product: Any, quantity: int) -> float:
        """
        Apply the second-half-price logic.
        """
        pairs = quantity // 2
        remainder = quantity % 2
        return (pairs * product.price * 1.5) + (remainder * product.price)


class ThirdOneFree(Promotion):
    """
    Every third item purchased is free (Buy 2, Get 1 Free).
    """

    def apply_promotion(self, product: Any, quantity: int) -> float:
        """
        Apply the buy-two-get-one-free logic.
        """
        triplets = quantity // 3
        remainder = quantity % 3
        return (triplets * product.price * 2) + (remainder * product.price)
