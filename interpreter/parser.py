from enum import IntEnum
import interpreter.token as token
from interpreter.ast import (
    Boolean,
    ExpressionStatement,
    Identifier,
    InfixExpression,
    IntegerLiteral,
    LetStatement,
    PrefixExpression,
    Program,
    ReturnStatement,
)

class Precedence(IntEnum):
    LOWEST = 0
    EQUALS = 1
    LESSGREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CLASS = 6

PrecedenceMap = {
    token.EQ: Precedence.EQUALS,
    token.NOT_EQ: Precedence.EQUALS,
    token.LT: Precedence.LESSGREATER,
    token.GT: Precedence.LESSGREATER,
    token.PLUS: Precedence.SUM,
    token.MINUS: Precedence.SUM,
    token.SLASH: Precedence.PRODUCT,
    token.ASTERISK: Precedence.PRODUCT,
}


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
        self.register_prefix(token.INT, self.parse_integer_literal)
        self.register_prefix(token.BANG, self.parse_prefix_expression)
        self.register_prefix(token.MINUS, self.parse_prefix_expression)
        self.register_prefix(token.TRUE, self.parse_boolean)
        self.register_prefix(token.FALSE, self.parse_boolean)
        self.register_prefix(token.LPAREN, self.parse_grouped_expression)

        self.infix_parse_fns = dict()
        self.register_infix(token.PLUS, self.parse_infix_expression)
        self.register_infix(token.MINUS, self.parse_infix_expression)
        self.register_infix(token.SLASH, self.parse_infix_expression)
        self.register_infix(token.ASTERISK, self.parse_infix_expression)
        self.register_infix(token.EQ, self.parse_infix_expression)
        self.register_infix(token.NOT_EQ, self.parse_infix_expression)
        self.register_infix(token.LT, self.parse_infix_expression)
        self.register_infix(token.GT, self.parse_infix_expression)

    def register_prefix(self, token_type, prefix_parse_fn):
        self.prefix_parse_fns[token_type] = prefix_parse_fn

    def register_infix(self, token_type, infix_parse_fn):
        self.infix_parse_fns[token_type] = infix_parse_fn

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
        prefix = self.prefix_parse_fns.get(self.cur_token.type)
        if not prefix:
            self.no_prefix_parse_error(self.cur_token.type)
            return None
        
        leftExp = prefix()

        while not self.peek_token_is(token.SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.type)
            if not infix:
                return leftExp

            self.next_token()
            leftExp = infix(leftExp)

        return leftExp

    def parse_identifier(self):
        return Identifier(self.cur_token, self.cur_token.literal)

    def parse_integer_literal(self):
        integer_literal = IntegerLiteral(self.cur_token)
        integer_literal.value = int(self.cur_token.literal)
        return integer_literal

    def parse_prefix_expression(self):
        expression = PrefixExpression(
            self.cur_token, 
            self.cur_token.literal
        )

        self.next_token()

        expression.right = self.parse_expression(Precedence.PREFIX)

        return expression

    def parse_infix_expression(self, left):
        expression = InfixExpression(self.cur_token, left, self.cur_token.literal)

        precedence = self.cur_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)

        return expression

    def parse_boolean(self):
        return Boolean(self.cur_token, self.cur_token_is(token.TRUE))

    def parse_grouped_expression(self):
        self.next_token()
        expression = self.parse_expression(Precedence.LOWEST)
        if not self.expect_peek(token.RPAREN):
            return None
        return expression

    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        self.peek_error(token_type)
        return False

    def cur_token_is(self, token_type):
        return self.cur_token.type == token_type

    def peek_token_is(self, token_type):
        return self.peek_token.type == token_type

    def peek_precedence(self):
        if self.peek_token.type in PrecedenceMap:
            return PrecedenceMap[self.peek_token.type]
        return Precedence.LOWEST

    def cur_precedence(self):
        if self.cur_token.type in PrecedenceMap:
            return PrecedenceMap[self.cur_token.type]
        return Precedence.LOWEST

    def peek_error(self, token_type):
        self.errors.append(f"Expected next token to be {token_type}, " \
            f"got {self.peek_token.type} instead")

    def no_prefix_parse_error(self, token_type):
        self.errors.append(f"No prefix parse function for {token_type} found")


