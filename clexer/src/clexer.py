import ply.lex as lex
from ply.lex import TOKEN

# Tokens definition
tokens = (
    'INT',
)

# ---------- [INT RULE] ----------
digit = rf'[0-9]+'
bit_integer_suffix_64 = rf'(i64|I64)'
long_long_suffix = rf'(ll|LL)'
long_suffix = rf'(l|L)'
unsigned_suffix = rf'(u|U)'

# Integer-suffix options
integer_suffix_1 = rf'{unsigned_suffix}({long_suffix}?)'
integer_suffix_2 = rf'{unsigned_suffix}{long_long_suffix}'
integer_suffix_3 = rf'{unsigned_suffix}{bit_integer_suffix_64}'
integer_suffix_4 = rf'{long_suffix}({unsigned_suffix}?)'
integer_suffix_5 = rf'{long_long_suffix}({unsigned_suffix}?)'
integer_suffix_6 = rf'{bit_integer_suffix_64}'
integer_suffix = rf'(({integer_suffix_1})|({integer_suffix_2})|({integer_suffix_3})|({integer_suffix_4})|({integer_suffix_5})|({integer_suffix_6}))'

hexadecimal_digit =  rf'[0-9a-fA-F]'
octal_digit = rf'[0-7]'
nonzero_digit = rf'[1-9]'
hexadecimal_prefix = rf'(0x|0X)'

hexadecimal_constant = rf'({hexadecimal_prefix}{hexadecimal_digit}+)'

octal_constant = rf'(0{octal_digit}+)'

decimal_constant = rf'({nonzero_digit}{digit}+)'

integer_constant_1 = rf'{decimal_constant}({integer_suffix}?)'
integer_constant_2 = rf'{octal_constant}({integer_suffix}?)'
integer_constant_3 = rf'{hexadecimal_constant}({integer_suffix}?)'
integer_constant = rf'(({integer_constant_1})|({integer_constant_2})|({integer_constant_3}))'

@TOKEN(integer_constant)
def t_INT(t):
    if len(t.value) > 1 and t.value[0] == '0':
        if t.value[1] in ('x', 'X'):
            t.value = int(t.value, 16)
        else:
            t.value = int(t.value, 8)
    else:
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