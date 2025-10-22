from __future__ import annotations

from typing import Tuple

from evaluator import decimal_representation
from rational import Rational
from ru_numbers import int_to_words_0_99, denom_power_to_word


def format_number_russian(integer: int, finite: str, period: str) -> str:
    negative = integer < 0
    iabs = abs(integer)
    if iabs >= 100:

        iwords = " ".join(int_to_words_0_99(int(d)) for d in str(iabs))
    else:
        iwords = int_to_words_0_99(iabs)
    if not finite and not period:
        return ("минус " + iwords) if negative and iabs != 0 else iwords

    if len(finite) > 6:
        finite = finite[:6]
    denom_power = len(finite)
    if denom_power == 0 and period:

        denom_power = 1
        finite = "0"
    frac_parts = []
    if denom_power > 0:
        finite_val = int(finite) if finite else 0
        if finite_val >= 100:
            finite_words = " ".join(int_to_words_0_99(int(d)) for d in finite)
        else:
            finite_words = int_to_words_0_99(finite_val)
        frac_parts.append(f"{finite_words} {denom_power_to_word(denom_power)}")
    if period:

        period_spaced = " ".join([int_to_words_0_99(int(d)) for d in period])
        if frac_parts:
            frac_parts.append(f"и {period_spaced} в периоде")
        else:
            frac_parts.append(f"{period_spaced} в периоде")
    head = ("минус " if negative and iabs != 0 else "") + iwords
    return head + " и " + " и ".join(frac_parts)


def format_rational_russian(q: Rational) -> str:
    integer, finite, period = decimal_representation(q)
    return format_number_russian(integer, finite, period)


