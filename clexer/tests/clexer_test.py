import unittest
from src.clexer import get_lexer


class TestIntegers(unittest.TestCase):
    def setUp(self):
        self.lexer = get_lexer()
    
    def test_basic_integers(self):
        self.lexer.input('1934')
        token = self.lexer.token()
        self.assertEqual(token.type, 'INT')
        self.assertEqual(token.value, 1934)


class TestFloats(unittest.TestCase):
    def setUp(self):
        self.lexer = get_lexer()

    def test_basic_floats(self):
        self.lexer.input('15.75 1. .54')
        for value in [15.75, 1.0, 0.54]:
            token = self.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)
    
    def test_exponent_floats(self):
        self.lexer.input('15.75 1.575E1 1575e-2 2.5e-3 25E-4')
        for value in [15.75, 15.75, 15.75, 0.0025, 0.0025]:
            token = self.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)
            
    def test_edge_cases_floats(self):
        self.lexer.input('.0075e2 0.075e1 .075e1 75e-2')
        for value in [0.75, 0.75, 0.75, 0.75]:
            token = self.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)

class TestStrings(unittest.TestCase):
    def setUp(self):
        self.lexer = get_lexer()

    def test_basic_strings(self):
        self.lexer.input('"hello, world"')
        token = self.lexer.token()
        self.assertEqual(token.type, 'STRING')
        self.assertEqual(token.value, '"hello, world"')
    
    def test_escaped_quotes_strings(self):
        self.lexer.input('"hello \\"world\\""')
        token = self.lexer.token()
        self.assertEqual(token.type, 'STRING')
        self.assertEqual(token.value, '"hello \\"world\\""')

    def test_escaped_quotes_and_backslashes_strings(self):
        self.lexer.input('"escaped \\"quotes\\" and \\\\ backslashes \\\\"')
        token = self.lexer.token()
        self.assertEqual(token.type, 'STRING')
        self.assertEqual(token.value, '"escaped \\"quotes\\" and \\\\ backslashes \\\\"')

class TestOperators(unittest.TestCase):
    def setUp(self):
        self.lexer = get_lexer()

    def test_operator_tokens(self):
        test_input = r'+ - * / % & ! ~ _Alignof sizeof ++ -- | ^ >> << < > <= >= == != && || ,'
        expected_tokens = [
            'PLUS', 'MINUS', 'TIMES', 'DIVISION', 'MODULO',
            'AMPERSAND', 'EXCLAMATION_OPERATOR', 'COMPLEMENT_OPERATOR',
            'ALIGNMENT_OPERATOR', 'SIZE_OPERATOR',
            'INCREMENT', 'DECREMENT',
            'BITWISE_OR', 'BITWISE_XOR', 'RIGHT_SHIFT', 'LEFT_SHIFT',
            'LESS_THAN', 'BIGGER_THAN', 'LESS_THAN_OR_EQUAL', 'BIGGER_THAN_OR_EQUAL',
            'EQUAL_TO', 'DIFFERENCE',
            'LOGIC_AND', 'LOGIC_OR',
            'SEQUENTIAL_OPERATOR'
        ]
        self.lexer.input(test_input)
        for token_type in expected_tokens:
            token = self.lexer.token()
            self.assertEqual(token.type, token_type)


if __name__ == '__main__':
    unittest.main()