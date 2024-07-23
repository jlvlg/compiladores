from tkinter import Tk
from tkinter.filedialog import askopenfilename
from token_instance import TokenType
from lexer import Lexer

keywords = {
    "true": TokenType.BOOL,
    "false": TokenType.BOOL,
    "int": TokenType.TYPE,
    "bool": TokenType.TYPE,
    "procedure": TokenType.PROCEDURE,
    "function": TokenType.FUNCTION,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "return": TokenType.RETURN,
    "while": TokenType.WHILE,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "write": TokenType.WRITE,
    "read": TokenType.READ,
}

symbols = {
    "(": TokenType.POPEN,
    ")": TokenType.PCLOSE,
    "{": TokenType.BOPEN,
    "}": TokenType.BCLOSE,
    ",": TokenType.COMMA,
    ";": TokenType.SEMICOLON,
    "=": TokenType.ASSIGN,
    "&&": TokenType.AND,
    "||": TokenType.OR,
    "==": TokenType.EQUAL,
    "!=": TokenType.NOTEQUAL,
    ">=": TokenType.GREATEREQUAL,
    "<=": TokenType.LESSEQUAL,
    ">": TokenType.GREATER,
    "<": TokenType.LESS,
    "+": TokenType.SUM,
    "-": TokenType.SUB,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
}

Tk().withdraw()
filename = askopenfilename()

with open(filename) as f:
    tokens = Lexer(keywords, symbols).scan(f.read())
    [print(token) for token in tokens]
