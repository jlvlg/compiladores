from lexer import Lexer
from parser import Parser
from pprint import pprint

with open('test') as f:
    tokens = Lexer().scan(f.read())
    pprint(Parser().parse(tokens, True))
