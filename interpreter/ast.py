from interpreter.token import Token

class Program:
    def __init__(self):
        self.statements = []

class Expression:
    def __init__(self):
        ...

class Identifier:
    def __init__(self, token, value):
        self.token = token
        self.value = value

class LetStatement:
    def __init__(self, token, identifier=None, expression=None):
        self.token = token
        self.name = identifier
        self.value = expression