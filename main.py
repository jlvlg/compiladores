from lexer import Lexer
from parser import Parser

with open('test') as f:
    tokens = Lexer().scan(f.read())
    Parser().parse(tokens, True)
