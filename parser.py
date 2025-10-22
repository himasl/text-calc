from __future__ import annotations

from typing import List

from tokenizer import Token


PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}


def to_rpn(tokens: List[Token]) -> List[Token]:
    output: List[Token] = []
    ops: List[Token] = []
    for tok in tokens:
        if tok.kind == "NUM":
            output.append(tok)
        elif tok.kind == "OP":
            while ops and ops[-1].kind == "OP" and PRECEDENCE[ops[-1].value] >= PRECEDENCE[tok.value]:
                output.append(ops.pop())
            ops.append(tok)
        elif tok.kind == "LPAREN":
            ops.append(tok)
        elif tok.kind == "RPAREN":
            while ops and ops[-1].kind != "LPAREN":
                output.append(ops.pop())
            if not ops or ops[-1].kind != "LPAREN":
                raise ValueError("Несогласованные скобки")
            ops.pop()
        else:
            raise ValueError(f"Неизвестный токен: {tok}")
    while ops:
        if ops[-1].kind in ("LPAREN", "RPAREN"):
            raise ValueError("Несогласованные скобки")
        output.append(ops.pop())
    return output


