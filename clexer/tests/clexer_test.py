import unittest
from src.clexer import CLexer


class TestIntegers(unittest.TestCase):
    def setUp(self):
        self.c_lexer = CLexer()
        self.c_lexer.build()

    def test_basic_integers(self):
        self.c_lexer.lexer.input('90000000000004')
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, 'INT')
        self.assertEqual(token.value, 90000000000004)

    def test_basic_integers_2(self):
        self.c_lexer.lexer.input('5')
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, 'INT')
        self.assertEqual(token.value, 5)


class TestFloats(unittest.TestCase):
    def setUp(self):
        self.c_lexer = CLexer()
        self.c_lexer.build()

    def test_basic_floats2(self):
        self.c_lexer.lexer.input('15.75 1. .54')
        for value in [15.75, 1.0, 0.54]:
            token = self.c_lexer.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)
    
    def test_exponent_floats(self):
        self.c_lexer.lexer.input('15.75 1.575E1 1575e-2 2.5e-3 25E-4')
        for value in [15.75, 15.75, 15.75, 0.0025, 0.0025]:
            token = self.c_lexer.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)
            
    def test_edge_cases_floats(self):
        self.c_lexer.lexer.input('.0075e2 0.075e1 .075e1 75e-2')
        for value in [0.75, 0.75, 0.75, 0.75]:
            token = self.c_lexer.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)
            
    def test_basic_floats(self):
        self.c_lexer.lexer.input('15.75 1. .54')
        for value in [15.75, 1.0, 0.54]:
            token = self.c_lexer.lexer.token()
            self.assertEqual(token.type, 'FLOAT')
            self.assertEqual(token.value, value)

class TestStrings(unittest.TestCase):
    def setUp(self):
        self.c_lexer = CLexer()
        self.c_lexer.build()

    def test_basic_strings(self):
        self.c_lexer.lexer.input('"hello, world"')
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, 'STRING')
        self.assertEqual(token.value, '"hello, world"')
    
    def test_escaped_quotes_strings(self):
        self.c_lexer.lexer.input('"hello \\"world\\""')
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, 'STRING')
        self.assertEqual(token.value, '"hello \\"world\\""')

    def test_escaped_quotes_and_backslashes_strings(self):
        self.c_lexer.lexer.input('"escaped \\"quotes\\" and \\\\ backslashes \\\\"')
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, 'STRING')
        self.assertEqual(token.value, '"escaped \\"quotes\\" and \\\\ backslashes \\\\"')
class IdentifierTests(unittest.TestCase):
    def setUp(self):
        self.c_lexer = CLexer()
        self.c_lexer.build()

    def test_identifiers(self):
        self.c_lexer.lexer.input('LastNum')
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, 'IDENTIFIER')
        self.assertEqual(token.value, "LastNum")

class TestLiterals(unittest.TestCase):
    def setUp(self):
        self.c_lexer = CLexer()
        self.c_lexer.build()

    def test_basic_literals(self):
        literal = '*'
        self.c_lexer.lexer.input(literal)
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, '*')
        self.assertEqual(token.value, literal)


class KeywordsTest(unittest.TestCase):
    def setUp(self):
        self.c_lexer = CLexer()
        self.c_lexer.build()

    def test_keywords(self):
        literal = 'auto'
        self.c_lexer.lexer.input(literal)
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, 'AUTO')
        self.assertEqual(token.value, literal)

class FullTester(unittest.TestCase):
    def setUp(self):
        self.c_lexer = CLexer()
        self.c_lexer.build()
        
    def test_text(self):
        self.c_lexer.lexer.input('void swap(int* xp, int* yp){int temp = *xp; *xp = *yp; *yp = temp;}')
        token = self.c_lexer.lexer.token()
        self.assertEqual(token.type, 'VOID')

if __name__ == '__main__':
    unittest.main()