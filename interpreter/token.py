class Token:
    def __init__(self, type, literal):
        self.type = type
        self.literal = literal

    def __str__(self):
        return f"Type: {self.type} / Literal: {self.literal}"


ILLEGAL = "ILLEGAL"
EOF     = "EOF"

# Identifiers + literals
IDENT = "IDENT" # add, foobar, x, y
INT   = "INT"   # 12345

# Operators
ASSIGN   = "="
PLUS     = "+"
MINUS    = "-"
BANG     = "!"
ASTERISK = "*"
SLASH    = "/"

EQ     = "=="
NOT_EQ = "!="
LT = "<"
GT = ">"

# Delimiters
COMMA     = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"

# Keywords
FUNCTION = "FUNCTION"
LET      = "LET"
TRUE     = "TRUE"
FALSE    = "FALSE"
IF       = "IF"
ELSE     = "ELSE"
RETURN   = "RETURN"

keywords = {
    "fn":     FUNCTION,
	"let":    LET,
	"true":   TRUE,
	"false":  FALSE,
	"if":     IF,
	"else":   ELSE,
	"return": RETURN,
}

def lookup_ident(ident):
    return keywords.get(ident, IDENT)