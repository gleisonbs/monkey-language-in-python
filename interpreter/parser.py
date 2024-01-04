import interpreter.token as token
from interpreter.ast import Program, LetStatement, Identifier

class Parser:
    def __init__(self, lexer):
        self.errors = []
        self.cur_token = None
        self.peek_token = None
        self.lexer = lexer

        self.next_token()
        self.next_token()

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

    def parse_let_statement(self):
        letStatement = LetStatement(self.cur_token)

        if not self.expect_peek(token.IDENT):
            return None

        letStatement.name = Identifier(self.cur_token, self.cur_token.literal)

        if not self.expect_peek(token.ASSIGN):
            self.next_token()
        
        while not self.cur_token_is(token.SEMICOLON) and not self.cur_token_is(token.EOF):
            self.next_token()
        
        return letStatement

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