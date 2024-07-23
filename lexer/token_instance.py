# type: ignore
from enum import StrEnum, auto
from dataclasses import dataclass


class TokenType(StrEnum):
    BOOL = auto()
    NUM = auto()
    ID = auto()
    TYPE = auto()
    PROCEDURE = auto()
    FUNCTION = auto()
    POPEN = auto()
    PCLOSE = auto()
    BOPEN = auto()
    BCLOSE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    ASSIGN = auto()
    IF = auto()
    ELSE = auto()
    RETURN = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    WRITE = auto()
    AND = auto()
    OR = auto()
    EQUAL = auto()
    NOTEQUAL = auto()
    GREATEREQUAL = auto()
    LESSEQUAL = auto()
    GREATER = auto()
    LESS = auto()
    SUM = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    READ = auto()
    END = auto()


@dataclass
class LexerToken:
    type: TokenType
    lexeme: str
    line: int
    start: int
    end: int
