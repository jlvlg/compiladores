# type: ignore
from enum import StrEnum, auto
from dataclasses import dataclass, field
from typing import Optional


class TokenType(StrEnum):
    BOOL = auto()
    NUM = "number"
    ID = auto()
    TYPE = auto()
    PROCEDURE = auto()
    FUNCTION = auto()
    POPEN = "("
    PCLOSE = ")"
    BOPEN = "{"
    BCLOSE = "}"
    COMMA = ","
    SEMICOLON = ";"
    ASSIGN = "="
    IF = auto()
    ELSE = auto()
    RETURN = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    WRITE = auto()
    AND = "&&"
    OR = "||"
    EQUAL = "=="
    NOTEQUAL = "!="
    GREATEREQUAL = ">="
    LESSEQUAL = "<="
    GREATER = ">"
    LESS = "<"
    SUM = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    READ = auto()
    END = auto()
    EMPTY = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    pos: int
    table_i: int | None = field(default=None, init=False)