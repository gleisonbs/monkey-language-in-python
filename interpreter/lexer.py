import interpreter.token as token
from interpreter.token import Token


class Lexer:
    def __init__(self, input, position=0, readPostion=0, ch=''):
        self.input = input
        self.position = position
        self.readPostion = readPostion
        self.ch = ch
        self.read_char()


    def read_char(self):
        if self.readPostion >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.readPostion]
        self.position = self.readPostion
        self.readPostion += 1


    def next_token(self):
        self.skip_whitespace()

        tok = None
        if self.ch == '=':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = Token(token.EQ, ch + self.ch)
            else:
                tok = Token(token.ASSIGN, self.ch)
        elif self.ch == '+':
            tok = Token(token.PLUS, self.ch)
        elif self.ch == '-':
            tok = Token(token.MINUS, self.ch)
        elif self.ch == '!':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = Token(token.NOT_EQ, ch + self.ch)
            else:
                tok = Token(token.BANG, self.ch)
        elif self.ch == '/':
            tok = Token(token.SLASH, self.ch)
        elif self.ch == '*':
            tok = Token(token.ASTERISK, self.ch)
        elif self.ch == '<':
            tok = Token(token.LT, self.ch)
        elif self.ch == '>':
            tok = Token(token.GT, self.ch)
        elif self.ch == ';':
            tok = Token(token.SEMICOLON, self.ch)
        elif self.ch == '(':
            tok = Token(token.LPAREN, self.ch)
        elif self.ch == ')':
            tok = Token(token.RPAREN, self.ch)
        elif self.ch == ',':
            tok = Token(token.COMMA, self.ch)
        elif self.ch == '{':
            tok = Token(token.LBRACE, self.ch)
        elif self.ch == '}':
            tok = Token(token.RBRACE, self.ch)
        elif self.ch == 0:
            tok = Token(token.EOF, '')
        else:
            if self.is_letter():
                literal = self.read_identifier()
                type = token.lookup_ident(literal)
                return Token(type, literal)
            elif self.is_digit():
                literal = self.read_number()
                type = token.INT
                return Token(type, literal)
            else:
                tok = Token(token.ILLEGAL, self.ch)
        
        self.read_char()
        return tok


    def read_identifier(self):
        ident_start = self.position
        while self.is_letter():
            self.read_char()
        return self.input[ident_start:self.position]


    def read_number(self):
        ident_start = self.position
        while self.is_digit():
            self.read_char()
        return self.input[ident_start:self.position]

     
    def skip_whitespace(self):
        while self.ch in [' ', '\t', '\n', '\r']:
            self.read_char()


    def peek_char(self):
        if self.readPostion > len(self.input):
            return 0
        return self.input[self.readPostion]
    

    def is_letter(self):
        return self.ch.isalpha()


    def is_digit(self):
        return self.ch.isnumeric()
