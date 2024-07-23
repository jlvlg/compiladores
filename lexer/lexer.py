from token_instance import LexerToken, TokenType


class Lexer:
    def __init__(self, keywords: dict[str, TokenType], symbols: dict[str, TokenType]):
        self.keywords = keywords
        self.symbols = symbols

    def scan(self, program: str) -> list[LexerToken]:
        self.program = program
        self.tokens: list[LexerToken] = []
        self.line = 1
        self.length = len(program)
        self.current = 0
        self.line = 1
        self.pos = 1
        while self.current < self.length:
            token = self._scanNextToken()
            if token is not None:
                self.tokens.append(token)
        self.tokens.append(self._createToken(TokenType.END, "\n"))
        return self.tokens

    def _createToken(self, type: TokenType, lexeme: str) -> LexerToken:
        return LexerToken(type, lexeme, self.line, self.pos - len(lexeme), self.pos - 1)

    def _forward(self, n: int = 1) -> None:
        for _ in range(n):
            self.current += 1
            self.pos += 1

    def _scanNextToken(self) -> LexerToken:
        while self.current < self.length:
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
                case char if self.current < self.length - 1 and (
                    symbol := char + self.program[self.current + 1]
                ) in self.symbols:
                    self._forward(2)
                    return self._createToken(self.symbols[symbol], symbol)
                case char if char in self.symbols:
                    self._forward()
                    return self._createToken(self.symbols[char], char)
                case _:
                    print(f"Unrecognized character at {self.line}:{self.pos} ")
                    exit(1)

    def _matchAlpha(self) -> LexerToken:
        lexeme = ""
        type = TokenType.ID
        while (char := self.program[self.current]).isalnum():
            lexeme += char
            if lexeme in self.keywords:
                type = self.keywords[lexeme]
            self._forward()
        return self._createToken(type, lexeme)

    def _matchNum(self, signal: str = "") -> LexerToken:
        lexeme = f"{signal}"
        while (char := self.program[self.current]).isnumeric():
            lexeme += char
            self._forward()
        return self._createToken(TokenType.NUM, lexeme)
