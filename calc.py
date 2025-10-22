from __future__ import annotations

from evaluator import eval_text
from formatter import format_rational_russian


def calc(text: str) -> str:
    q = eval_text(text)
    return format_rational_russian(q)


if __name__ == "__main__":
    examples = [
        ("двадцать пять плюс тринадцать", "тридцать восемь"),
        ("пять плюс два умножить на три минус один", "десять"),
        ("скобка открывается пять плюс два скобка закрывается умножить на три минус один", "двадцать"),
        ("девятнадцать и восемьдесят две сотых разделить на девяносто девять", None),
    ]
    for expr, expected in examples:
        try:
            res = calc(expr)
            print(expr, "->", res, ("(ok)" if expected is None or res == expected else f"(expected {expected})"))
        except Exception as e:
            print(expr, "-> error:", e)


