import unittest
from interpreter.lexer import Lexer
from interpreter.parser import Parser
import interpreter.token as token
from interpreter.ast import (
    ExpressionStatement, 
    Identifier,
    InfixExpression,
    IntegerLiteral,
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
            5,
            838383
        ]

        self.assertEqual(len(program.statements), len(expected_identifiers))
        for i in range(len(program.statements)):
            statement = program.statements[i]
            self.assertEqual(isinstance(statement, ExpressionStatement), True)
        
            literal = statement.expression
            self.assertEqual(isinstance(literal, IntegerLiteral), True)
            self.assertEqual(literal.value, expected_identifiers[i])
            self.assertEqual(literal.token_literal(), f"{expected_identifiers[i]}")

    def test_prefix_expression_is_correctly_parsed(self):
        input = """
        !5;
        -15;
        !true;
        !false;
        """

        expected_prefixes = [
            ("!", 5),
            ("-", 15),
            ("!", True),
            ("!", False),
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
                   
    def test_infix_expression_is_correctly_parsed(self):
        infix_tests = [
            ("5 + 5", 5, "+", 5),
            ("5 - 5", 5, "-", 5),
            ("5 * 5", 5, "*", 5),
            ("5 / 5", 5, "/", 5),
            ("5 > 5", 5, ">", 5),
            ("5 < 5", 5, "<", 5),
            ("5 == 5", 5, "==", 5),
            ("5 != 5", 5, "!=", 5),
            ("true == true", True, "==", True),
            ("true != false", True, "!=", False),
            ("false == false", False, "==", False),
        ]

        for i in range(len(infix_tests)):
            input = infix_tests[i][0]

            lexer = Lexer(input)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.check_parser_errors(parser)

            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertEqual(isinstance(statement, ExpressionStatement), True)

            infix_expression = statement.expression
            self.assertEqual(isinstance(infix_expression, InfixExpression), True)

            self.check_literal_expression(infix_expression.left, infix_tests[i][1])

    def test_operator_precedence_is_correctly_parsed(self):
        precedence_tests = [
            ("-a * b", "((-a) * b)"),
            ( "!-a", "(!(-a))" ),
            ( "a + b + c", "((a + b) + c)" ),
            ( "a + b - c", "((a + b) - c)" ),
            ( "a * b * c", "((a * b) * c)" ),
            ( "a * b / c", "((a * b) / c)" ),
            ( "a + b / c", "(a + (b / c))" ),
            ( "a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)" ),
            ( "3 + 4; -5 * 5", "(3 + 4)((-5) * 5)" ),
            ( "5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))" ),
            ( "5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))" ),
            ( "3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))" ),
            ( "3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))" ),
            ( "true", "true" ),
            ( "false", "false" ),
            ( "3 > 5 == false", "((3 > 5) == false)" ),
            ( "3 < 5 == true", "((3 < 5) == true)" ),
            ( "1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)" ),
            ( "(5 + 5) * 2", "((5 + 5) * 2)" ),
            ( "2 / (5 + 5)", "(2 / (5 + 5))" ),
            ( "-(5 + 5)", "(-(5 + 5))" ),
            ( "!(true == true)", "(!(true == true))" ),
        ]

        for i in range(len(precedence_tests)):
            input = precedence_tests[i][0]
            lexer = Lexer(input)
            parser = Parser(lexer)
            program = parser.parse_program()
            self.check_parser_errors(parser)
            self.assertEqual(program.string(), precedence_tests[i][1])


    def check_literal_expression(self, expression, expected_value):
        if isinstance(expected_value, bool):
            return self.check_boolean_literal(expression, expected_value)
        elif isinstance(expected_value, int):
            return self.check_integer_literal(expression, expected_value)

    def check_integer_literal(self, integer_literal, value):
        self.assertEqual(integer_literal.value, value)
        self.assertEqual(integer_literal.token_literal(), f"{value}")

    def check_boolean_literal(self, boolean_literal, value):
        self.assertEqual(boolean_literal.value, value)

        literal = boolean_literal.token_literal()
        literal = literal[0].upper() + literal[1:]
        self.assertEqual(literal, f"{value}")

    def check_parser_errors(self, parser):
        errors = parser.errors

        if not errors:
            return

        for error in errors:
            self.fail(error)
