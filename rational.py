from __future__ import annotations

from dataclasses import dataclass
from math import gcd


@dataclass(frozen=True)
class Rational:
    numerator: int
    denominator: int

    def __post_init__(self):
        if self.denominator == 0:
            raise ZeroDivisionError("denominator is zero")
        sign = -1 if (self.numerator < 0) ^ (self.denominator < 0) else 1
        a = abs(self.numerator)
        b = abs(self.denominator)
        g = gcd(a, b)
        object.__setattr__(self, "numerator", sign * (a // g))
        object.__setattr__(self, "denominator", b // g)

    def __add__(self, other: Rational) -> Rational:
        return Rational(self.numerator * other.denominator + other.numerator * self.denominator, self.denominator * other.denominator)

    def __sub__(self, other: Rational) -> Rational:
        return Rational(self.numerator * other.denominator - other.numerator * self.denominator, self.denominator * other.denominator)

    def __mul__(self, other: Rational) -> Rational:
        return Rational(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other: Rational) -> Rational:
        if other.numerator == 0:
            raise ZeroDivisionError("division by zero")
        return Rational(self.numerator * other.denominator, self.denominator * other.numerator)

    @staticmethod
    def from_num_den(num: int, den: int) -> Rational:
        return Rational(num, den)


