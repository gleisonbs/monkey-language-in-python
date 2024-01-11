import interpreter.token as token
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
        return f"{self.token}, Name: {self.name}, Value: {self.value}"

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
        return f"{self.token}, Return Value: {self.return_value}"

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        ret = " "
        if self.return_value:
            ret += self.return_value.string()
        ret += ";"
        return ret


class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Optional[Expression] = None):
        self.token = token
        self.expression = expression

    def __str__(self) -> str:
        return f"{self.token}, Expression: {self.expression}"

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        if self.expression:
            return self.expression.string()
        return ""


class  IntegerLiteral(Expression):
    def __init__(self, token: Token, value: Optional[int] = None):
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return f"{self.token}, Value: {self.value}"

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Optional[Expression] = None):
        self.token = token
        self.operator = operator
        self.right = right

    def token_literal(self):
        return self.token.literal

    def string(self):
        return f"({self.operator}{self.right.string()})"

class InfixExpression(Expression):
    def __init__(self, 
        token: Token, 
        left: Expression, 
        operator: str, 
        right: Optional[Expression] = None):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def token_literal(self):
        return self.token.literal

    def string(self):
        return f"({self.left.string()} {self.operator} {self.right.string()})"


class Boolean(Expression):
    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.literal

    def string(self):
        return self.token.literal