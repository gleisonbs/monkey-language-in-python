from interpreter.token import Token
from typing import List, Optional
from abc import ABC, abstractmethod

class Program:
    def __init__(self):
        self.statements: List[Expression] = []

class Node(ABC):
    @abstractmethod
    def token_literal() -> str:
        ...
    
    @abstractmethod
    def string() -> str:
        ...

class Expression(Node):
    def expression_node():
        ...

class Statement(Node):
    def statement_node():
        ...

class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return f"{self.token}, Value: {self.value}"

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.value


class LetStatement(Statement):
    def __init__(self, token: Token, 
        identifier: Optional[Identifier] = None, 
        expression: Optional[Expression] = None):
        self.token = token
        self.name = identifier
        self.value = expression

    def __str__(self) -> str:
        return f"{self.token}, {self.identifier}, {self.value}"

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        ret = self.token_literal() + " "
        ret += self.name.string()
        ret += " = "
        if self.value:
            ret += self.value.string()
        ret += ";"
        return ret


class ReturnStatement(Statement):
    def __init__(self, token: Token, 
        return_value: Optional[Expression] = None):
        self.token = token
        self.return_value = return_value

    def __str__(self) -> str:
        return f"{self.token}, {self.identifier}, {self.return_value}"

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        ret = " "
        if self.return_value:
            ret += self.return_value.string()
        ret += ";"
        return ret