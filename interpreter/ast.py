from interpreter.token import Token
from typing import List, Optional


class Program:
    def __init__(self):
        self.statements: List[Expression] = []

class Expression:
    def __init__(self):
        ...

class Identifier:
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return f"{self.token}, Value: {self.value}"

    def token_literal(self) -> str:
        return self.token.literal

class LetStatement:
    def __init__(self, token: Token, 
        identifier: Optional[Identifier] = None, 
        expression: Optional[Expression] = None):
        self.token = token
        self.name = identifier
        self.value = expression

    def __str__(self) -> str:
        return f"{self.token}, {self.identifier}, {self.value}"
