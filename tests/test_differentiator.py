import re

import pytest

from recurse.differentiator import ParseError, Polynomial, derivative


class TestDerivative:
    def test_derivative(self) -> None:
        polynomial = Polynomial.parse("5x^2 - 4x + 2")
        assert derivative(polynomial).coefficients == [-4, 10]


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

    def test_parse_negative_one_coefficient(self) -> None:
        polynomial = Polynomial.parse("-x")
        assert polynomial.coefficients == [0, -1]

    def test_parse_decimal_coefficient_raises(self) -> None:
        with pytest.raises(ParseError, match=re.escape("failed to parse polynomial term: 0.5x")):
            Polynomial.parse("0.5x")

    def test_parse_multi_term_quadratic(self) -> None:
        polynomial = Polynomial.parse("5x^2 - 4x + 2")
        assert polynomial.coefficients == [2, -4, 5]

    def test_parse_multi_term_quadratic_with_hole(self) -> None:
        polynomial = Polynomial.parse("5x^3 - 2")
        assert polynomial.coefficients == [-2, 0, 0, 5]

    def test_parse_no_coefficient(self) -> None:
        polynomial = Polynomial.parse("x")
        assert polynomial.coefficients == [0, 1]

    def test_parse_backwards_terms(self) -> None:
        polynomial = Polynomial.parse("1 + x^2")
        assert polynomial.coefficients == [1, 0, 1]
