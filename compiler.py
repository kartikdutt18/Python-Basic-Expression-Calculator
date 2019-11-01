import ply.lex as lex
import ply.yacc as yacc
import sys

# LIST OF ALL TOKENS
tokens = [

    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS',
    'POWER',
    'AND',
    'OR',

]

# REGEX FOR EACH TOKEN
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_POWER=r'\^'
t_AND=r'\&'
t_OR=r'\|'

#IGNORE SPACES AND BRACKETS [PRIORITY DEFINED SO NO NEED]
t_ignore = r' ( ) {}'

#FLOAT NOS CONTAIN DECIMAL POINT AND THEN AGAIN NOS
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

#SIMPLY AN INTEGER.
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# The first character in Variable NAME must be in the ranges a-z A-Z.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.
def t_NAME(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

# SKIP ILLEGAL CHARACTERS
def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1)

# BUILD THE LEXER
lexer = lex.lex()

#DEFINE AST PRECEDENCE
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right','POWER')
)

# DEFINE THE LOGIC
def p_calc(p):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    # BUILD TREE
    p[0] = ('=', p[1], p[3])

# Expressions are recursive.
def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression POWER expression
               | expression AND expression
               | expression OR expression

    '''
    # BUILD TREE
    p[0] = (p[2], p[1], p[3])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

#OUTPUT INCASE OF ERROR
def p_error(p):
    print("Syntax error found!")

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# BUILD THE PARSER
parser = yacc.yacc()
# ENVIORNMENT TO STORE VARIABLES {DICTIONARY}
env = {}
# TRAVERSE TREE
def run(p):
    global env
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '^':
            return run(p[1]) ** run(p[2])
        elif p[0] == '&':
            return run(p[1]) & run(p[2])
        elif p[0] == '|':
            return run(p[1]) | run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
            return ''
        
        elif p[0] == 'var':
            if p[1] not in env:
                return 'Undeclared variable found!'
            else:
                return env[p[1]]
    else:
        return p

# INTERFACE OF TREE
print('BASIC_LANG 1.0.0')
while True:
    try:
        s = input('>>> ')
        s=s.replace('int',' ')
        s=s.replace('float',' ')
        s=s.replace('double',' ')
        s=s.replace('long',' ')
    except EOFError:
        break
    parser.parse(s)
