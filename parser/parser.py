from lexer.token_instance import Token, TokenType
from itertools import chain

class Parser:
    def __init__(self) -> None:
        self.syntaxtable = {
            "program": {
                "cmd": ["cmd_block", "program"],
                TokenType.PROCEDURE: [self._procedure, self._id, TokenType.POPEN, self._params, TokenType.PCLOSE, "block", "program"],
                TokenType.FUNCTION: [self._function, self._type, self._id, TokenType.POPEN, self._params, TokenType.PCLOSE, "block", "program"],
                TokenType.END: [],
            },
            "var_def": {
                TokenType.TYPE: [self._type, self._id],
            },
            "params": {
                "var_def": [self._var_def, "params_separator"],
                TokenType.EMPTY: []
            },
            "params_separator": {
                TokenType.COMMA: [TokenType.COMMA, self._var_def, "params_separator"],
                TokenType.EMPTY: [],
            },
            "block": {
                TokenType.BOPEN: [TokenType.BOPEN, "cmd_block", self._bclose]
            },
            "cmd_block": {
                "cmd": ["cmd", "cmd_block"],
                TokenType.EMPTY: []
            },
            "cmd": {
                TokenType.ID: {
                    TokenType.ASSIGN: [self._id, TokenType.ASSIGN, "expr", TokenType.SEMICOLON],
                    TokenType.POPEN: [self._id, TokenType.POPEN, "args", TokenType.PCLOSE, TokenType.SEMICOLON],
                },
                TokenType.IF: [self._if, "expr", "block", "else"],
                TokenType.WHILE: [self._while, "expr", "block"],
                TokenType.BREAK: [TokenType.BREAK, TokenType.SEMICOLON],
                TokenType.CONTINUE: [TokenType.CONTINUE, TokenType.SEMICOLON],
                "var_def": [self._var_def, TokenType.SEMICOLON],
                TokenType.WRITE: [TokenType.WRITE, TokenType.POPEN, "expr", TokenType.PCLOSE, TokenType.SEMICOLON],
                "read": ["read", TokenType.SEMICOLON],
                TokenType.RETURN: [TokenType.RETURN, "expr", TokenType.SEMICOLON],
            },
            "else": {
                TokenType.ELSE: [self._else, "block"],
                TokenType.EMPTY: [],
            },
            "log_op": {
                TokenType.AND: [TokenType.AND],
                TokenType.OR: [TokenType.OR],
            },
            "rel_op": {
                TokenType.EQUAL: [TokenType.EQUAL],
                TokenType.NOTEQUAL: [TokenType.NOTEQUAL],
                TokenType.GREATEREQUAL: [TokenType.GREATEREQUAL],
                TokenType.LESSEQUAL: [TokenType.LESSEQUAL],
                TokenType.GREATER: [TokenType.GREATER],
                TokenType.LESS: [TokenType.LESS],
            },
            "math_op": {
                TokenType.SUM: [TokenType.SUM],
                TokenType.SUB: [TokenType.SUB],
                TokenType.MUL: [TokenType.MUL],
                TokenType.DIV: [TokenType.DIV],
            },
            "expr": {
                TokenType.POPEN: [TokenType.POPEN, "expr", TokenType.PCLOSE, "expr_2"],
                TokenType.NUM: [TokenType.NUM, "expr_2"],
                TokenType.BOOL: [TokenType.BOOL, "expr_2"],
                TokenType.ID: {
                    TokenType.POPEN: [self._id, TokenType.POPEN, "args", TokenType.PCLOSE, "expr_2"],
                    TokenType.EMPTY: [self._id, "expr_2"],
                },
                "read": ["read", "expr_2"],
            },
            "expr_2": {
                "log_op": ["log_op", "expr"],
                "rel_op": ["rel_op", "expr"],
                "math_op": ["math_op", "expr"],
                TokenType.EMPTY: []
            },
            "read": {
                TokenType.READ: [TokenType.READ, TokenType.POPEN, TokenType.PCLOSE]
            },
            "args": {
                "expr": ["expr", "args_separator"],
                TokenType.EMPTY: []
            },
            "args_separator": {
                TokenType.COMMA: [TokenType.COMMA, "expr", "args_separator"],
                TokenType.EMPTY: [],
            },
        }

    def parse(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0
        self.table = []
        self.scopes = [[]]
        self.building = {}
        self.stack = ["program"]
        while len(self.stack) > 0:
            next = self.stack.pop()
            if isinstance(next, TokenType):
                self._consume(next)
            elif isinstance(next, str):
                self._extendStack(next)
            else:
                next()
        return self.tokens, self.table

    def _forward(self, n: int = 1):
        self.current += n

    def _token(self, n: int = 0):
        if self.current + n >= len(self.tokens):
            print("Could not fetch next symbol")
            exit(1)
        return self.tokens[self.current + n]

    def _getTable(self, prod: str, token: Token):
        table = self.syntaxtable[prod]
        while not all(isinstance(prod, TokenType) for prod in table):
            for prod in table:
                if not isinstance(prod, TokenType):
                    table = {x:table[x] for x in table if x != prod} | {y: table[prod] for y in self.syntaxtable[prod]}
        self._check(token, table)
        next = table.get(token.type, [])
        if isinstance(next, dict):
            lookahead = self._token(1)
            self._check(lookahead, next.keys())
            next = next.get(lookahead.type, next.get(TokenType.EMPTY))
        return next[::-1]

    def _check(self, token: Token, types: list[TokenType]):
        if token.type not in types and TokenType.EMPTY not in types:
            print(f"Syntax error at {token.line}:{token.start}. Expected {', '.join(types)}. Got {token.type}.")
            exit(1)
    
    def _consume(self, type: TokenType):
        self._check(self._token(), [type])
        self._forward()

    def _extendStack(self, prod: str):
        self.stack.extend(self._getTable(prod, self._token()))
    
    def _openScope(self):
        self.scopes.append([])
    
    def _closeScope(self):
        self.scopes.pop()

    def _procedure(self):
        self.building = {"what": "procedure"}
        self._consume(TokenType.PROCEDURE)

    def _function(self):
        self.building = {"what": "function"}
        self._consume(TokenType.FUNCTION)

    def _params(self):
        self._openScope()
        self._extendStack("params")

    def _var_def(self):
        self.building = {"what": "variable"}
        self._extendStack("var_def")

    def _if(self):
        self._openScope()
        self._consume(TokenType.IF)

    def _else(self):
        self._openScope()
        self._consume(TokenType.ELSE)
    
    def _while(self):
        self._openScope()
        self._consume(TokenType.WHILE)
    
    def _id(self):
        token = self._token()
        self._check(token, [TokenType.ID])
        if self.building:
            self.building["id"] = token.lexeme
            self.table.append(self.building)
            token.table_i = len(self.table) - 1
            self.building["token"] = token
            if self.building["id"] in chain.from_iterable(self.scopes):
                print(f"{self.building["id"]} already defined")
                exit(1)
            self.scopes[-1].append(self.building["id"])
        else:
            if token.lexeme in chain.from_iterable(self.scopes):
                token.table_i = [x["id"] for x in self.table].index(token.lexeme)
            else:
                print(f"Accessing undefined object {token.lexeme} at line {token.line} pos {token.start}:{token.end}")
                exit(1)

        self.building = {}
        self._forward()
    
    def _type(self):
        self.building["type"] = self._token().lexeme
        self._consume(TokenType.TYPE)

    def _bclose(self):
        self._closeScope()
        self._consume(TokenType.BCLOSE)
