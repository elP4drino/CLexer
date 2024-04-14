import unittest
from src.clexer import get_lexer


class TestIntegers(unittest.TestCase):
    def setUp(self):
        self.lexer = get_lexer()

    def test_basic_integers(self):
        self.lexer.input('90000000000004')
        token = self.lexer.token()
        self.assertEqual(token.type, 'INT')
        self.assertEqual(token.value, 90000000000004)


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
class IdentifierTests(unittest.TestCase):
    def setUp(self):
        self.lexer = get_lexer()

    def test_identifiers(self):
        self.lexer.input('LastNum')
        token = self.lexer.token()
        self.assertEqual(token.type, 'IDENTIFIER')
        self.assertEqual(token.value, "LastNum")


if __name__ == '__main__':
    unittest.main()