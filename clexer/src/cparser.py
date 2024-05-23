import ply.yacc as yacc
from src.clexer import CLexer
from src.ir import Literal, BinaryOp, RelationalOp, WhileStatement, Declaration, Assignment, Program, IfStatement, IfElseStatement, ForStatement

class CParser:
    def __init__(self):
        self.parser = None

    c_lexer = CLexer()
    c_lexer.build()

    tokens = c_lexer.tokens

    def p_program(self, p):
        """
        PROGRAM : INT_KEYWORD IDENTIFIER '(' ')' '{' DECLARATIONS STATEMENTS '}'
        """
        if len(p) > 2:
            p[0] = Program(p[6], p[7])
        else:
            p[0] = Program(p[6], [])


    def p_declarations(self, p):
        """
        DECLARATIONS : DECLARATION DECLARATIONS 
                     | EMPTY
        """
        if len(p) > 2:
            if p[2]:
                p[0] = [p[1]] + p[2]
            else:
                p[0] = [p[1]]
        else:
            p[0] = p[1]


    def p_declaration(self, p):
        """
        DECLARATION : TYPE IDENTIFIER '=' EQUALITY ';'
                    | TYPE IDENTIFIER ';'
        """

        if len(p) > 4:
            print(list(p))
            p[0] = Declaration(p[1], p[2], p[4])
        else:
            print('none', list(p))
            p[0] = Declaration(p[1], p[2], None)


    def p_type(self, p):
        """
        TYPE : INT_KEYWORD 
             | FLOAT_KEYWORD
        """
        p[0] = p[1]


    def p_statements(sefl, p):
        """
        STATEMENTS : STATEMENT STATEMENTS 
                   | EMPTY
        """
        if len(p) > 2:
            if p[2]:
                p[0] = [p[1]] + p[2]
            else:
                p[0] = [p[1]]
        else:
            p[0] = p[1]


    def p_statement(self, p):
        """
        STATEMENT : ASSIGNMENT
                  | DECLARATION
                  | IF_STATEMENT
                  | IF_ELSE_STATEMENT
                  | FOR_STATEMENT
                  | WHILE_STATEMENT
                  | BLOCK
                  | ';'
        """
        p[0] = p[1]


    def p_block(self, p):
        """
        BLOCK : '{' STATEMENTS '}'
        """
        p[0] = p[2]


    def p_for_assingment(self, p):
        """
        FOR_ASSIGNMENT : IDENTIFIER '=' EQUALITY
        """
        p[0] = Assignment(p[1], p[3])


    def p_assignment(self, p):
        """
        ASSIGNMENT : IDENTIFIER '=' EQUALITY ';'
        """
        p[0] = Assignment(p[1], p[3])


    def p_if_else_statement(self, p):
        """
        IF_ELSE_STATEMENT : IF '(' EXPRESSION ')' STATEMENTS ELSE STATEMENTS
        """
        p[0] = IfElseStatement(p[3], p[5], p[7])


    def p_if_statement(self, p):
        """
        IF_STATEMENT : IF '(' EXPRESSION ')' STATEMENTS
        """
        p[0] = IfStatement(p[3], p[5])


    def p_for_statement(self, p):
        """
        FOR_STATEMENT : FOR '(' DECLARATION EXPRESSION ';' FOR_ASSIGNMENT ')' STATEMENTS
        """
        print('reaching for')
        p[0] = ForStatement(p[3], p[4], [6], p[8])


    def p_while_statement(self, p):
        """
        WHILE_STATEMENT : WHILE '(' EXPRESSION ')' STATEMENTS
        """
        p[0] = WhileStatement(p[3], p[5])


    def p_expression(self, p):
        """
        EXPRESSION : EXPRESSION OR CONJUNCTION 
                   | CONJUNCTION
        """
        p[0] = p[1]


    def p_conjunction(self, p):
        """
        CONJUNCTION : CONJUNCTION AND EQUALITY 
                    | EQUALITY
        """
        p[0] = p[1]


    def p_equality(self, p):
        """
        EQUALITY : RELATION EQU_OP RELATION 
                 | RELATION
        """
        if len(p) > 2:
            p[0] = RelationalOp(p[2], p[1], p[3])
        else:
            p[0] = p[1]


    def p_equ_op(self, p):
        """
        EQU_OP : EQUAL
               | DIFFERENT
        """
        p[0] = p[1]


    def p_relation(self, p):
        """
        RELATION : ADDITION REL_OP ADDITION 
                 | ADDITION
        """
        if len(p) > 2:
            p[0] = RelationalOp(p[2], p[1], p[3])
        else:
            p[0] = p[1]


    def p_rel_op(self, p):
        """
        REL_OP : '<' 
               | LTE
               | '>' 
               | MTE
        """
        p[0] = p[1]


    def p_addition(self, p):
        """
        ADDITION : ADDITION ADD_OP TERM 
                 | TERM
        """
        if len(p) > 2:
            p[0] = BinaryOp(p[2], p[1], p[3])
        else:
            p[0] = p[1]


    def p_add_op(self, p):
        """
        ADD_OP : '+' 
               | '-'
        """
        p[0] = p[1]


    def p_term(self, p):
        """
        TERM : TERM MUL_OP FACTOR 
             | FACTOR
        """
        if len(p) > 2:
            p[0] = BinaryOp(p[2], p[1], p[3])
        else:
            p[0] = p[1]


    def p_mul_op(self, p):
        """
        MUL_OP : '*' 
               | '/' 
               | '%'
        """
        p[0] = p[1]


    def p_factor(self, p):
        """
        FACTOR : PRIMARY
        """
        p[0] = p[1]


    def p_primary(self, p):
        """
        PRIMARY : INT
                | FLOAT
                | IDENTIFIER
        """
        if isinstance(p[1], int):
            p[0] = Literal(p[1], 'INT')
        elif isinstance(p[1], float):
            p[0] = Literal(p[1], 'FLOAT')
        else:
            p[0] = Literal(p[1], 'ID')


    def p_empty(self, p):
        """
        EMPTY :
        """
        pass


    def p_error(self, p):
        print(f"¡Error de sintaxis en la entrada! {p}")


    def build(self):
        self.parser = yacc.yacc(module=self)


    def parse(self, t_string):
        if not self.parser:
            raise Exception('Analizador no construido')

        self.c_lexer.lexer.input(t_string)
        return self.parser.parse(t_string)