import ply.lex as lex
from ply.lex import TOKEN

# Tokens definition
tokens = (
    'INT',
    'FLOAT',
    'STRING',
    'KEYWORD',
)

states = (
    ('string', 'exclusive'),
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

#--------- [KEYWORDS RULES] ----------
keywords_1 = r'auto|break|case|char|const|continue|default|do|double|else|enum'
keywords_2 = r'extern|float|for|goto|if|inline|int|long|register|restrict|return'
keywords_3 = r'short|signed|sizeof|static|struct|switch|typedef|typeof|typeof_unqual|union|unsigned|void|volatile'
keywords_4 = r'while|_Alignas|_Alignof|_Atomic|_Bool|_Complex|_Generic|_Noreturn|_Static_assert|_Thread_local'

keywordsMicro_1 = r'__asm|__based|__cdecl|__declspec|__except|__fastcall|__finally'
keywordsMicro_2 = r'__inline|__int16|__int32|__int64|__int8|__leave|__restrict'
keywordsMicro_3 = r'__stdcall|__try|__typeof__|__typeof_unqual__|dllexport|dllimport|naked|static_assert|thread'
KeyWords = rf'({keywords_1}|{keywords_2}|{keywords_3}|{keywords_4}|{keywordsMicro_1}|{keywordsMicro_2}|{keywordsMicro_3})'


@TOKEN(floating_point_constant)
def t_FLOAT(t):
    t.value = float(t.value)
    return t

@TOKEN(int_regex)
def t_INT(t):
    t.value = int(t.value)
    return t

@TOKEN(KeyWords)
def t_KEYWORD(t):
    
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