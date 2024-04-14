import ply.lex as lex
import int_rules
import float_rules

tokens = (
    'INT',
)

# States for more complex regex
states = ()

# Ignored characters
t_ignore = ' \t'

lexer = lex.lex()

def get_lexer():
    return lexer