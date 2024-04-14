import ply.lex as lex
from ply.lex import TOKEN

# Tokens definition
tokens = (
    'INT',
)

# Tokens rules
int_regex = r'\d+'

@TOKEN(int_regex)
def t_INT(t):
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def get_lexer():
    return lex.lex()