import ply.lex as lex
from ply.lex import TOKEN

# Tokens definition
tokens = (
    'INT',
    'FLOAT',
)

# Tokens rules
# ---------- [FLOAT RULE] ----------
floating_suffix = r'[flFL]'
digit_sequence = r'(\d+)'
sign = r'[\+\-]'
exponent_part = rf'([eE]{sign}?{digit_sequence})'

fractional_constant_1 = rf'{digit_sequence}?\.{digit_sequence}'
fractional_constant_2 = rf'{digit_sequence}\.'
fractional_constant = rf'(({fractional_constant_1})|({fractional_constant_2}))'

floating_point_constant_1 = rf'{fractional_constant}{exponent_part}?{floating_suffix}?'
floating_point_constant_2 = rf'{digit_sequence}{exponent_part}{floating_suffix}?'
floating_point_constant = rf'(({floating_point_constant_1})|({floating_point_constant_2}))'

int_regex = r'\d+'

@TOKEN(floating_point_constant)
def t_FLOAT(t):
    t.value = float(t.value)
    return t

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