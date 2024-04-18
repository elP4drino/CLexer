import ply.lex as lex
from ply.lex import TOKEN

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

#---------- [IDENTIFIER RULES] ----------
digit = rf'[0-9]'
nondigit = rf'[_a-zA-Z]'
identifier = rf'({nondigit}+{digit}*)'

#--------- [KEYWORDS RULES] ----------
reserved = {
    'auto'     : 'AUTO',
    'break'    : 'BREAK',
    'case'     : 'CASE',
    'char'     : 'CHAR',
    'const'    : 'CONST',
    'continue' : 'CONTINUE',
    'default'  : 'DEFAULT',
    'do'       : 'DO',
    'double'   : 'DOUBLE',
    'else'     : 'ELSE',
    'enum'     : 'ENUM',
    'extern'   : 'EXTERN',
    'float'    : 'FLOAT_KEYWORD',
    'for'      : 'FOR',
    'goto'     : 'GOTO',
    'if'       : 'IF',
    'inline'   : 'INLINE',
    'int'      : 'INT_KEYWORD',
    'long'     : 'LONG',
    'register' : 'REGISTER',
    'restrict' : 'RESTRICT',
    'return'   : 'RETURN',
    'short'    : 'SHORT',
    'signed'   : 'SIGNED',
    'sizeof'   : 'SIZEOF',
    'static'   : 'STATIC',
    'struct'   : 'STRUCT',
    'switch'   : 'SWITCH',
    'typedef'  : 'TYPEDEF',
    'typeof'   : 'TYPEOF',
    'typeof_unqual' : 'TYPEOF_UNQUAL',
    'union'    : 'UNION',
    'unsigned' : 'UNSIGNED',
    'void'     : 'VOID',
    'volatile' : 'VOLATILE',
    'while'    : 'WHILE',
    '_Alignas'        : '_ALIGNAS',
    '_Alignof'        : '_ALIGNOF',
    '_Atomic'         : '_ATOMIC',
    '_Bool'           : '_BOOL',
    '_Complex'        : '_COMPLEX',
    '_Generic'        : '_GENERIC',
    '_Noreturn'       : '_NORETURN',
    '_Static_assert'  : '_STATIC_ASSERT',
    '_Thread_local'   : '_THREAD_LOCAL',
    '__asm'           : '__ASM',
    '__based'         : '__BASED',
    '__cdecl'         : '__CDECL',
    '__declspec'      : '__DECLSPEC',
    '__except'        : '__EXCEPT',
    '__fastcall'      : '__FASTCALL',
    '__finally'       : '__FINALLY',
    '__inline'        : '__INLINE',
    '__int16'         : '__INT16',
    '__int32'         : '__INT32',
    '__int64'         : '__INT64',
    '__int8'          : '__INT8',
    '__leave'         : '__LEAVE',
    '__restrict'      : '__RESTRICT',
    '__stdcall'       : '__STDCALL',
    '__try'           : '__TRY',
    '__typeof__'      : '__TYPEOF__',
    '__typeof_unqual__' : '__TYPEOF_UNQUAL__',
    'dllexport'       : 'DLLEXPORT',
    'dllimport'       : 'DLLIMPORT',
    'naked'           : 'NAKED',
    'static_assert'   : 'STATIC_ASSERT',
    'thread'          : 'THREAD'
}

# Tokens definition
tokens = ['INT', 'FLOAT', 'STRING', 'ALIGNMENT', 'SIZE', 'IDENTIFIER'] + list(reserved.values())

literals = ['*', '+', '-', '%', '/', '&', '!', '~', '|', '^', '=', ',', '(', ')', '{', '}']

def t_KEYWORD(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'KEYWORD')    # Check for reserved words
    return t


@TOKEN(identifier)
def  t_IDENTIFIER(t):
    return t


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