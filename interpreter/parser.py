from enum import IntEnum
import interpreter.token as token
from interpreter.ast import Program, LetStatement, ReturnStatement, ExpressionStatement, Identifier

class Parser:
    def __init__(self, lexer):
        self.errors = []
        self.cur_token = None
        self.peek_token = None
        self.lexer = lexer

        self.next_token()
        self.next_token()

        self.prefix_parse_fns = dict()
        self.register_prefix(token.IDENT, self.parse_identifier)

    def register_prefix(self, token_type, prefix_parse_fn):
        self.prefix_parse_fns[token_type] = prefix_parse_fn

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        program = Program()
        while self.cur_token.type != token.EOF:
            statement = self.parse_statement()
            if statement is not None:
                program.statements.append(statement)
            self.next_token()
        return program

    def parse_statement(self):
        if self.cur_token.type == token.LET:
            return self.parse_let_statement()
        elif self.cur_token.type == token.RETURN:
            return self.parse_return_statement()
        return self.parse_expression_statement()

    def parse_let_statement(self):
        statement = LetStatement(self.cur_token)

        if not self.expect_peek(token.IDENT):
            return None

        statement.name = Identifier(self.cur_token, self.cur_token.literal)

        if not self.expect_peek(token.ASSIGN):
            self.next_token()
        
        while not self.cur_token_is(token.SEMICOLON) and not self.cur_token_is(token.EOF):
            self.next_token()
        
        return statement

    def parse_return_statement(self):
        statement = ReturnStatement(self.cur_token)

        self.next_token()

        if not self.cur_token_is(token.SEMICOLON):
            self.next_token()

        return statement

    def parse_expression_statement(self):
        statement = ExpressionStatement(self.cur_token)
        statement.expression = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(token.SEMICOLON):
            self.next_token()

        return statement

    def parse_expression(self, precedence):
        prefix = self.prefix_parse_fns[self.cur_token.type]
        if not prefix:
            return None
        
        leftExp = prefix()

        return leftExp

    def parse_identifier(self):
        return Identifier(self.cur_token, self.cur_token.literal)

    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        return False

    def cur_token_is(self, token_type):
        return self.cur_token.type == token_type

    def peek_token_is(self, token_type):
        return self.peek_token.type == token_type

    def peek_error(self, token_type):
        self.errors.append(f"Expected next token to be {token_type}, " \
            f"got {self.peek_token.type} instead")

class Precedence(IntEnum):
    LOWEST = 0
    EQUALS = 1
    LESSGREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CLASS = 6