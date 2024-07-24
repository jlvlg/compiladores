from lexer.token_instance import Token, TokenType
from itertools import chain

class Parser:
    def __init__(self) -> None:
        self.syntaxtable = {
            "program": {
                TokenType.ID: ["program", "cmdblock"], 
                TokenType.IF: ["program", "cmdblock"],
                TokenType.WHILE: ["program", "cmdblock"],
                TokenType.BREAK: ["program", "cmdblock"],
                TokenType.CONTINUE: ["program", "cmdblock"],
                TokenType.WRITE: ["program", "cmdblock"],
                TokenType.READ: ["program", "cmdblock"],
                TokenType.TYPE: ["program", "cmdblock"],
                TokenType.PROCEDURE: ["program", self._procdef],
                TokenType.FUNCTION: ["program", self._fundef],
                TokenType.END: [],
            },
            "cmd": {
                TokenType.ID: {
                    TokenType.ASSIGN: ["cmd", TokenType.SEMICOLON, "assign"],
                    TokenType.POPEN: ["cmd", TokenType.SEMICOLON, "proccall"],
                },
                TokenType.TYPE: ["cmd", TokenType.SEMICOLON, self._vardef],
                TokenType.IF: ["cmd", "cond"],
                TokenType.WHILE: ["cmd", "loop"],
                TokenType.BREAK: ["cmd", TokenType.SEMICOLON, TokenType.BREAK],
                TokenType.CONTINUE: ["cmd", TokenType.SEMICOLON, TokenType.CONTINUE],
                TokenType.WRITE: ["cmd", TokenType.SEMICOLON, "write"],
                TokenType.READ: ["cmd", TokenType.SEMICOLON, "read"],
                TokenType.RETURN: ["cmd", "return"],
            },
            "cmdblock": {
                "cmd": ["cmdblock", "cmd"],
                TokenType.EMPTY: []
            },
            "procdef": {
                TokenType.PROCEDURE: ["block", TokenType.PCLOSE, "params", TokenType.POPEN, self._id, TokenType.PROCEDURE],
            },
            "fundef": {
                TokenType.FUNCTION: ["block", TokenType.PCLOSE, "params", TokenType.POPEN, self._id, self._type, TokenType.FUNCTION],
            },
            "params": {
                TokenType.TYPE: [self._paramsseparator, self._vardef],
                TokenType.EMPTY: [],
            },
            "vardef": {
                TokenType.TYPE: [self._id, self._type],
            },
            "paramsseparator": {
                TokenType.COMMA: [self._paramsseparator, self._vardef, TokenType.COMMA],
                TokenType.EMPTY: [],
            },
            "block": {
                TokenType.BOPEN: [TokenType.BCLOSE, "cmd", TokenType.BOPEN],
            },
            "assign": {
                TokenType.ID: ["expr", TokenType.ASSIGN, self._id]
            },
            "proccall": {
                TokenType.ID: [TokenType.PCLOSE, "args", TokenType.POPEN, self._id]
            },
            "args": {
                "expr": ["args_separator", "expr"],
                TokenType.EMPTY: [],
            },
            "args_separator": {
                TokenType.COMMA: ["args_separator", "expr", TokenType.COMMA],
                TokenType.EMPTY: [],
            },
            "cond": {
                TokenType.IF: ["elsecond", "block", TokenType.PCLOSE, "expr", TokenType.POPEN, self._if]
            },
            "elsecond": {
                TokenType.ELSE: ["block", self._else],
                TokenType.EMPTY: [],
            },
            "return": {
                TokenType.RETURN: [TokenType.SEMICOLON, "expr", TokenType.RETURN],
            },
            "expr": {
                TokenType.POPEN: ["expr_2", TokenType.PCLOSE, "expr", TokenType.POPEN],
                TokenType.NUM: ["expr_2", TokenType.NUM],
                TokenType.BOOL: ["expr_2", TokenType.BOOL],
                TokenType.READ: ["expr_2", "read"],
                TokenType.ID: {
                    TokenType.POPEN: ["expr_2", "funccall"],
                    TokenType.EMPTY: ["expr_2", self._id],
                }
            },
            "expr_2": {
                TokenType.AND: ["expr", TokenType.AND],
                TokenType.OR: ["expr", TokenType.OR],
                TokenType.EQUAL: ["expr", TokenType.EQUAL],
                TokenType.NOTEQUAL: ["expr", TokenType.NOTEQUAL],
                TokenType.GREATEREQUAL: ["expr", TokenType.GREATEREQUAL],
                TokenType.LESSEQUAL: ["expr", TokenType.LESSEQUAL],
                TokenType.GREATER: ["expr", TokenType.GREATER],
                TokenType.LESS: ["expr", TokenType.LESS],
                TokenType.SUM: ["expr", TokenType.SUM],
                TokenType.SUB: ["expr", TokenType.SUB],
                TokenType.MUL: ["expr", TokenType.MUL],
                TokenType.DIV: ["expr", TokenType.DIV],
                TokenType.EMPTY: []
            },
            "funccall": {
                TokenType.ID: [TokenType.PCLOSE, "args", TokenType.POPEN, self._id],
            },
            "read": {
                TokenType.READ: [TokenType.PCLOSE, TokenType.POPEN, TokenType.READ]
            },
            "write": {
                TokenType.WRITE: [TokenType.PCLOSE, "expr", TokenType.POPEN, TokenType.WRITE]
            },
            "loop": {
                TokenType.WHILE: ["block", TokenType.PCLOSE, "expr", TokenType.POPEN, self._while]
            }
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
        if self.current + n > len(self.tokens) - 1:
            print("Could not fetch lookahead")
            exit(1)
        return self.tokens[self.current + n]

    def _getTable(self, prod: str, token: Token):
        table = self.syntaxtable[prod]
        for x in table.keys():
            if not isinstance(x, TokenType):
                table = table | self.syntaxtable[x]
        self._check(token, self.syntaxtable[prod])
        next = self.syntaxtable[prod].get(token.type, [])
        if isinstance(next, dict):
            lookahead = self._token(1)
            self._check(lookahead, next.keys())
            next = next.get(lookahead.type, next.get(TokenType.EMPTY))
        return next

    def _check(self, token: Token, types: list[TokenType]):
        if token.type not in types and TokenType.EMPTY not in types:
            print(f"Syntax error at {token.line}:{token.start}. Expected {', '.join(types)}. Got {token.type}.")
            exit(1)
    
    def _consume(self, type: TokenType):
        self._check(self._token(), [type])
        self._forward()

    def _extendStack(self, prod):
        self.stack.extend(self._getTable(prod, self._token()))
    
    def _openScope(self):
        self.scopes.append([])
    
    def _closeScope(self):
        self.scopes.pop()

    def _procdef(self):
        self.building = {"what": "procedure"}
        self._extendStack("procdef")
        self._openScope()

    def _fundef(self):
        self.building = {"what": "function"}
        self._extendStack("fundef")
        self._openScope()

    def _vardef(self):
        self.building = {"what": "variable"}
        self._extendStack("vardef")

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
        self._check(self._token(), [TokenType.TYPE])
        self.building["type"] = self._token().lexeme
        self._forward()
    
    def _paramsseparator(self):
        self._extendStack("paramsseparator")