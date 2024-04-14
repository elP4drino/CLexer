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


if __name__ == '__main__':
    unittest.main()