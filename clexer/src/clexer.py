import ply.lex as lex
from ply.lex import TOKEN

# Tokens definition
tokens = ['INT', 'FLOAT', 'STRING', 'ALIGNMENT', 'SIZE']

literals = ['*', '+', '-', '%', '/', '&', '!', '~', '|', '^', '=', ',', '(', ')', '{', '}']

states = (
    ('string', 'exclusive'),
)

# Tokens rules
# ---------- [OPERATOR RULES] ----------
t_ALIGNMENT = r'_Alignof'
t_SIZE = r'sizeof'

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

# Conditional lexing
# ---------- [STRING RULE] ----------
s_char = rf'((\\\"|\\\\)|[^"\n\\])'
s_char_sequence = rf'{s_char}+'

def t_string(t):
    r'\"'
    t.lexer.str_start = t.lexer.lexpos - 1
    t.lexer.begin('string')

def t_string_ending_quote(t):
    r'\"'
    t.value = t.lexer.lexdata[t.lexer.str_start:t.lexer.lexpos + 1]
    t.type = "STRING"
    t.lexer.begin('INITIAL')
    return t

@TOKEN(s_char)
def t_string_s_char(t):
    pass

@TOKEN(s_char_sequence)
def t_string_s_char_sequence(t):
    pass

t_string_ignore = ' \t'

def t_string_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def get_lexer():
    return lex.lex()