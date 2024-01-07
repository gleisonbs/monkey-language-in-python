import unittest
from interpreter.lexer import Lexer
from interpreter.parser import Parser
import interpreter.token as token
from interpreter.ast import (
    ExpressionStatement, 
    Identifier,
    IntegerLiteral
    LetStatement,
    PrefixExpression,
    ReturnStatement, 
)

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
        self.check_parser_errors(parser)


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
        self.check_parser_errors(parser)


        self.assertEqual(len(program.statements), 3)
        for i in range(len(program.statements)):
            self.assertEqual(isinstance(program.statements[i], ReturnStatement), True)
            self.assertEqual(program.statements[i].token.type, token.RETURN)
            self.assertEqual(program.statements[i].token_literal(), "return")

    def test_identifier_is_correctly_parsed(self):
        input = """
        foobar;
        """

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()
        self.check_parser_errors(parser)

        expected_identifiers = [
            "foobar",
        ]

        self.assertEqual(len(program.statements), len(expected_identifiers))
        for i in range(len(program.statements)):
            statement = program.statements[i]
            self.assertEqual(isinstance(statement, ExpressionStatement), True)
            self.assertEqual(isinstance(statement.expression, Identifier), True)

            identifier = statement.expression
            self.assertEqual(identifier.value, expected_identifiers[i])
            self.assertEqual(identifier.token_literal(), expected_identifiers[i])

    def test_integer_literal_is_correctly_parsed(self):
        input = """
        5;
        838383;
        """

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        self.check_parser_errors(parser)

        expected_identifiers = [
            "5",
            "838383"
        ]

        self.assertEqual(len(program.statements), len(expected_identifiers))
        for i in range(len(program.statements)):
            statement = program.statements[i]
            self.assertEqual(isinstance(statement, ExpressionStatement), True)
        
            literal = statement.expression
            self.assertEqual(isinstance(literal, IntegerLiteral), True)
            self.assertEqual(literal.value, expected_identifiers[i])
            self.assertEqual(literal.token_literal(), expected_identifiers[i])

    def test_prefix_expression_is_correctly_parsed(self):
        input = """
        !5;
        -15;
        !true;
        !false;
        """

        expected_prefixes = [
            ("!", '5'),
            ("-", '15'),
            ("!", 'true'),
            ("!", 'false'),
        ]

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()
        self.check_parser_errors(parser)

        self.assertEqual(len(program.statements), 4)
        for i in range(len(program.statements)):
            statement = program.statements[i]
            self.assertEqual(isinstance(statement, ExpressionStatement), True)

            prefix_expression = statement.expression
            self.assertEqual(isinstance(prefix_expression, PrefixExpression), True)
            self.assertEqual(prefix_expression.operator, expected_prefixes[i][0])
            self.assertEqual(prefix_expression.right.value, expected_prefixes[i][1])
                   
    def check_parser_errors(self, parser):
        errors = parser.errors

        if not errors:
            return

        for error in errors:
            self.fail(error)
