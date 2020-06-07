from enum import Enum


class Currencies(Enum):
    CAD = 1
    USD = 1.5
    EUR = 2

    def convert_to_cad(self, amount: float):
        return amount * self.value
