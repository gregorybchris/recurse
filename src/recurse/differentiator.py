import re
from dataclasses import dataclass
from typing import Optional, Self


class ParseError(ValueError):
    pass


@dataclass
class Polynomial:
    # In order of ascending exponents
    coefficients: list[int]

    def __str__(self) -> str:
        raise NotImplementedError

    @classmethod
    def parse_coefficient(cls, coefficient: Optional[str]) -> int:
        if coefficient is None:
            return 1
        if coefficient == "":
            return 1
        if coefficient == "+":
            return 1
        if coefficient == "-":
            return -1
        return int(coefficient)

    @classmethod
    def parse_exponent(cls, variable: str, exponent: str) -> int:
        if variable is None or variable == "":
            return 0
        if not exponent:
            return 1
        return int(exponent)

    @classmethod
    def parse(cls, s: str) -> Self:
        # Split into terms
        # TODO: Support negative exponents
        s = s.replace(" ", "").replace("+", " +").replace("-", " -").strip()
        terms = [x.replace(" ", "") for x in s.split(" ")]

        exponent_map = {}
        max_exponent = 0
        for term in terms:
            # TODO: Support decimal coefficients
            pattern = re.compile("^([-+]?[0-9]*)?(x(\\^([0-9]+))?)?$")
            match = re.match(pattern, term)
            if match is None:
                msg = f"failed to parse polynomial term: {term}"
                raise ParseError(msg)

            coefficient = cls.parse_coefficient(match.group(1))
            exponent = cls.parse_exponent(match.group(2), match.group(4))
            exponent_map[exponent] = coefficient
            max_exponent = max(max_exponent, exponent)

        coefficients = []
        for exponent in range(max_exponent + 1):
            if exponent in exponent_map:
                coefficients.append(exponent_map[exponent])
            else:
                coefficients.append(0)

        return cls(coefficients)


def derivative(polynomial: Polynomial) -> Polynomial:
    new_terms = []
    for exponent, coefficient in enumerate(polynomial.coefficients):
        if exponent == 0:
            continue
        new_terms.append(coefficient * exponent)

    return Polynomial(new_terms)
