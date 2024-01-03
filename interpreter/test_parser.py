import unittest
from interpreter.lexer import Lexer
from interpreter.parser import Parser
import interpreter.token as token

class ParserTest(unittest.TestCase):
    def test_let_statement_is_correctly_parsed(self):
        input = """
        let x = 5;
        let y = 10;
        let foobar = 838383;
        """

        lexer = Lexer(input)
        parser = Parser(lexer)

        program = parser.parse_program()

        for statement in program.statements:
            self.assertEqual(statement.token.type, token.LET)