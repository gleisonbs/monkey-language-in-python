import unittest
from interpreter.lexer import Lexer
from interpreter.parser import Parser
import interpreter.token as token
from interpreter.ast import LetStatement, ReturnStatement

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

        self.assertEqual(len(program.statements), 3)
        for i in range(len(program.statements)):
            self.assertEqual(isinstance(program.statements[i], LetStatement), True)
            self.assertEqual(program.statements[i].token.type, token.LET)
            self.assertEqual(program.statements[i].name.value, expected_identifiers[i])
            self.assertEqual(program.statements[i].name.token_literal(), expected_identifiers[i])

    def test_return_statement_is_correctly_parsed(self):
        input = """
        return 5;
        return 10;
        return 993322;
        """

        lexer = Lexer(input)
        parser = Parser(lexer)

        program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)
        for i in range(len(program.statements)):
            self.assertEqual(isinstance(program.statements[i], ReturnStatement), True)
            self.assertEqual(program.statements[i].token.type, token.RETURN)
            self.assertEqual(program.statements[i].token_literal(), "return")