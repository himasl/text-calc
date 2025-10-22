from __future__ import annotations

from typing import List, Tuple

from parser import to_rpn
from rational import Rational
from tokenizer import Token, tokenize


def eval_tokens(tokens: List[Token]) -> Rational:
    rpn = to_rpn(tokens)
    stack: List[Rational] = []
    for tok in rpn:
        if tok.kind == "NUM":
            num_str, den_str = tok.value.split("/")
            stack.append(Rational.from_num_den(int(num_str), int(den_str)))
        elif tok.kind == "OP":
            b = stack.pop()
            a = stack.pop()
            if tok.value == "+":
                stack.append(a + b)
            elif tok.value == "-":
                stack.append(a - b)
            elif tok.value == "*":
                stack.append(a * b)
            elif tok.value == "/":
                stack.append(a / b)
        else:
            raise ValueError("Unsupported token in RPN")
    if len(stack) != 1:
        raise ValueError("Некорректное выражение")
    return stack[0]


def eval_text(expr: str) -> Rational:
    return eval_tokens(tokenize(expr))


def decimal_representation(q: Rational, max_period_len: int = 4) -> Tuple[int, str, str]:

    n, d = q.numerator, q.denominator
    sign = -1 if n < 0 else 1
    n = abs(n)
    integer = n // d
    rem = n % d

    d_abs = d
    e2 = 0
    while d_abs % 2 == 0:
        d_abs //= 2
        e2 += 1
    e5 = 0
    while d_abs % 5 == 0:
        d_abs //= 5
        e5 += 1
    finite_len = max(e2, e5)
    if finite_len > 6:
        finite_len = 6

    finite_digits: list[str] = []
    r = rem
    for _ in range(finite_len):
        r *= 10
        finite_digits.append(str(r // d))
        r %= d

    period_digits: list[str] = []
    seen = {}
    count = 0
    while r != 0 and count < max_period_len:
        if r in seen:
            break
        seen[r] = len(period_digits)
        r *= 10
        period_digits.append(str(r // d))
        r %= d
        count += 1
    finite = "".join(finite_digits)
    period = "".join(period_digits)
    if sign < 0 and (integer > 0 or finite or period):
        integer = -integer
    return integer, finite, period


