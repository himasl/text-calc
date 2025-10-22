from __future__ import annotations

from typing import Dict, Tuple


_UNITS: Dict[str, int] = {
    "ноль": 0,
    "один": 1,
    "одна": 1,
    "два": 2,
    "две": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
}


_TENS: Dict[str, int] = {
    "двадцать": 20,
    "тридцать": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "шестьдесят": 60,
    "семьдесят": 70,
    "восемьдесят": 80,
    "девяносто": 90,
}


_DENOM_WORDS = {
    1: ("десятая", "десятых"),
    2: ("сотая", "сотых"),
    3: ("тысячная", "тысячных"),
    4: ("десятитысячная", "десятитысячных"),
    5: ("стотысячная", "стотысячных"),
    6: ("миллионная", "миллионных"),
}


def normalize(token: str) -> str:
    return token.strip().lower()


def parse_0_99(words: Tuple[str, ...]) -> Tuple[int, int]:
    value = 0
    consumed = 0
    if consumed < len(words):
        w0 = normalize(words[0])
        if w0 in _UNITS and _UNITS[w0] < 20:

            v = _UNITS[w0]
            value = v
            consumed = 1
        if w0 in _TENS:
            value = _TENS[w0]
            consumed = 1
            if consumed < len(words):
                w1 = normalize(words[consumed])
                if w1 in _UNITS and _UNITS[w1] < 10:
                    value += _UNITS[w1]
                    consumed += 1
        elif w0 in _UNITS and _UNITS[w0] >= 10:

            value = _UNITS[w0]
            consumed = 1
    return value, consumed


def parse_fractional(words: Tuple[str, ...]) -> Tuple[int, int, int]:

    num, n_words = parse_0_99(words)
    if n_words == 0:
        return 0, 0, 0
    if n_words >= len(words):
        return 0, 0, 0
    denom_word = normalize(words[n_words])
    power = None
    for p, forms in _DENOM_WORDS.items():
        if denom_word.startswith(forms[0][:5]) or denom_word.startswith(forms[1][:5]):
            power = p
            break
    if power is None:
        return 0, 0, 0
    return num, power, n_words + 1


def parse_number(words: Tuple[str, ...]) -> Tuple[int, int, int]:

    integer, c = parse_0_99(words)
    if c == 0 and len(words) > 0 and normalize(words[0]) == "ноль":
        integer = 0
        c = 1

    if c < len(words) and normalize(words[c]) == "и":
        num, pow10, c2 = parse_fractional(words[c + 1 :])
        if c2 > 0:
            denom = 10**pow10
            return integer * denom + num, denom, c + 1 + c2
    return integer, 1, c


def int_to_words_0_99(n: int) -> str:
    if n < 0 or n >= 100:
        raise ValueError("n out of range 0..99")
    for k, v in _UNITS.items():
        if v == n and n < 20:
            return k
    if n < 20:

        return {
            0: "ноль",
            10: "десять",
            11: "одиннадцать",
            12: "двенадцать",
            13: "тринадцать",
            14: "четырнадцать",
            15: "пятнадцать",
            16: "шестнадцать",
            17: "семнадцать",
            18: "восемнадцать",
            19: "девятнадцать",
        }[n]
    tens = (n // 10) * 10
    units = n % 10
    tens_word = None
    for k, v in _TENS.items():
        if v == tens:
            tens_word = k
            break
    if units == 0:
        return tens_word
    unit_word = None
    for k, v in _UNITS.items():
        if v == units and v < 10:
            unit_word = k
            break

    if unit_word in ("одна",):
        unit_word = "один"
    if unit_word == "две":
        unit_word = "два"
    return f"{tens_word} {unit_word}"


def denom_power_to_word(power: int) -> str:
    return _DENOM_WORDS[power][1]


