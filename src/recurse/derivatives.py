import re
from dataclasses import dataclass
from typing import Self

import pytest


class ParseError(ValueError):
    pass


@dataclass
class Polynomial:
    # In order of ascending exponents
    coefficients: list[float]

    def __str__(self) -> str:
        raise NotImplementedError

    @classmethod
    def parse(cls, s: str) -> Self:
        print(f"Parse input: {s}")
        # TODO: Support decimal coefficients
        term_pattern = "^([-0-9]*)?(x(\\^([0-9]+))?)?$"
        # TODO: Support multiple terms
        pattern = re.compile(term_pattern)
        match = re.match(pattern, s)
        if match is None:
            msg = f"failed to parse polynomial: {s}"
            raise ParseError(msg)

        for group_number in range(4):
            print(f"Group {group_number}: {match.group(group_number)}")

        coefficient = 1 if not match.group(1) else int(match.group(1))
        has_exponent = bool(match.group(4))
        has_variable = bool(match.group(2))
        exponent = (1 if has_variable else 0) if not has_exponent else int(match.group(4))

        print("coefficient: ", coefficient)
        print("exponent: ", exponent)

        coefficients = []
        for _ in range(exponent):
            coefficients.append(0)
        coefficients.append(coefficient)

        return cls(coefficients)


def derivative(polynomial: Polynomial) -> Polynomial:
    raise NotImplementedError


class TestPolynomial:
    def test_parse_constant(self) -> None:
        polynomial = Polynomial.parse("5")
        assert polynomial.coefficients == [5]

    def test_parse_simple_linear(self) -> None:
        polynomial = Polynomial.parse("5x")
        assert polynomial.coefficients == [0, 5]

    def test_parse_simple_quadratic(self) -> None:
        polynomial = Polynomial.parse("5x^2")
        assert polynomial.coefficients == [0, 0, 5]

    def test_parse_negative_coefficient(self) -> None:
        polynomial = Polynomial.parse("-5x")
        assert polynomial.coefficients == [0, -5]

    def test_parse_decimal_coefficient_raises(self) -> None:
        with pytest.raises(ParseError, match=re.escape("failed to parse polynomial: 0.5x")):
            Polynomial.parse("0.5x")

    def test_parse_negative_exponent_raises(self) -> None:
        with pytest.raises(ParseError, match=re.escape("failed to parse polynomial: x^-4")):
            Polynomial.parse("x^-4")
