import unittest
from src.clexer import get_lexer

class TestIntegers(unittest.TestCase):
    def setUp(self):
        self.lexer = get_lexer()

    def test_basic_integers(self):
        self.lexer.input('034')
        token = self.lexer.token()
        self.assertEqual(token.type, 'INT')
        self.assertEqual(token.value, 0o34)

if __name__ == '__main__':
    unittest.main()