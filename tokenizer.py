from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from ru_numbers import parse_number, normalize


@dataclass(frozen=True)
class Token:
    kind: str
    value: str | None = None


OPERATORS = {
    "плюс": "+",
    "минус": "-",
    "умножить": "*",
    "разделить": "/",
}


def tokenize(text: str) -> List[Token]:
    words = [normalize(w) for w in text.split()]
    i = 0
    tokens: List[Token] = []
    while i < len(words):
        w = words[i]

        if w == "скобка" and i + 1 < len(words):
            if words[i + 1].startswith("открыва"):
                tokens.append(Token("LPAREN"))
                i += 2
                continue
            if words[i + 1].startswith("закрыва"):
                tokens.append(Token("RPAREN"))
                i += 2
                continue

        if w in OPERATORS:
            tokens.append(Token("OP", OPERATORS[w]))

            if w in ("умножить", "разделить") and i + 1 < len(words) and words[i + 1] == "на":
                i += 2
            else:
                i += 1
            continue

        num, den, consumed = parse_number(tuple(words[i:]))
        if consumed > 0:
            tokens.append(Token("NUM", f"{num}/{den}"))
            i += consumed
            continue
        if w in ("и", "на"):
            i += 1
            continue
        raise ValueError(f"Неожиданное слово: {w}")
    return tokens


