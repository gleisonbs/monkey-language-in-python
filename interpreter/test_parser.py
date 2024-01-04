import unittest
from interpreter.lexer import Lexer
from interpreter.parser import Parser
import interpreter.token as token
from interpreter.ast import LetStatement

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

        expected_identifiers = [
            "x", "y", "foobar",
        ]

        for i in range(len(program.statements)):
            self.assertEqual(isinstance(program.statements[i], LetStatement), True)
            self.assertEqual(program.statements[i].token.type, token.LET)
            self.assertEqual(program.statements[i].name.value, expected_identifiers[i])
            self.assertEqual(program.statements[i].name.token_literal(), expected_identifiers[i])
