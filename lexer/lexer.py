from .token_instance import Token, TokenType


class Lexer:
    def __init__(self):
        self.keywords = {
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
        self.symbols = {
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

    def scan(self, program: str) -> tuple[list[Token], list[dict], bool]:
        self.program = program
        self.tokens: list[Token] = []
        self.current = 0
        self.line = 1
        self.pos = 1
        while self.current < len(self.program):
            token = self._scanNextToken()
            if token is not None:
                self.tokens.append(token)
        self.tokens.append(self._createToken(TokenType.END, "\n"))
        return self.tokens

    def _createToken(self, type: TokenType, lexeme: str) -> Token:
        return Token(type, lexeme, self.line, self.pos - len(lexeme))

    def _forward(self, n: int = 1) -> None:
        for _ in range(n):
            self.current += 1
            self.pos += 1

    def _scanNextToken(self) -> Token:
        while self.current < len(self.program):
            match char := self.program[self.current]:
                case " ":
                    self._forward()
                case "\n":
                    self._forward()
                    self.line += 1
                    self.pos = 1
                case char if char.isalpha():
                    return self._matchAlpha()
                case char if char.isnumeric():
                    return self._matchNum()
                case "+" | "-" if self.program[self.current + 1].isnumeric():
                    self._forward()
                    return self._matchNum(char)
                case char if self.current < len(self.program) - 1 and (
                    symbol := char + self.program[self.current + 1]
                ) in self.symbols:
                    self._forward(2)
                    return self._createToken(self.symbols[symbol], symbol)
                case char if char in self.symbols:
                    self._forward()
                    return self._createToken(self.symbols[char], char)
                case _:
                    text = self.program.splitlines()[self.line - 1]
                    print(text[:self.pos - 1] + "\033[4;31m" + char + "\033[0m" + text[self.pos:])
                    print(f"\nLexical error at {self.line}:{self.pos}. Unrecognized symbol: {char}")
                    exit(1)

    def _matchAlpha(self) -> Token:
        lexeme = ""
        while (char := self.program[self.current]).isalnum():
            self._forward()
            lexeme += char
            if lexeme in self.keywords:
                return self._createToken(self.keywords[lexeme], lexeme)
        return self._createToken(TokenType.ID, lexeme)

    def _matchNum(self, signal: str = "") -> Token:
        lexeme = f"{signal}"
        while (char := self.program[self.current]).isnumeric():
            lexeme += char
            self._forward()
        return self._createToken(TokenType.NUM, lexeme)
