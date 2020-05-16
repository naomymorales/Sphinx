import sys
import math
import Sphinx_Lexer

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

#LEXER ANALYSIS


reserved = {
    'integral': 'INTEGRAL',
    'from': 'FROM',
    'to': 'TO',
    'derivation': 'DERIVATIVE',
    'limit': 'LIMIT',
    'when': 'WHEN',
    'of': 'OF',
    'oo': 'INFINITY',
    'summation': 'SUMMATION',
    'product': 'PRODUCT',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'varlist' : 'PRINTLIST',
}

# Tokens

tokens = [
    'VAR',
    'FLOAT',
    'INT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POWER',
    'EQUALS',
    'LPAREN',
    'RPAREN',
    'GOES',
    'X',
    ] + list(reserved.values())

# set Variables format
# Set tokens representation
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_POWER = r'\^'
t_EQUALS = r'\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_GOES = r'\->'
t_X = r'[x]'
t_ignore = " \t"


def t_VAR(t):
    r'[a-wyzA-WYZ][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VAR')    # Check for reserved words
    return t


# Set floating point structure
#   number '.' number                   -> example. 12.34
#   number '.' number 'e' '+/-' number  -> example. 12.34e+56 or 12.34E-56
#   number 'e' '+/-' number             -> example. 12E+34 or 12e-34
def t_FLOAT(t):
    r'([0-9]+)?([.][0-9]+)([eE][+-]?[0-9]+)?'
    t.value = float(t.value)
    return t


# Set integer structure
def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded


def t_error(t):
    print ("ERROR: Line %d: LEXER: Illegal character '%s' " % (t.lexer.lineno, t.value[0]))
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules and precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER'),
    ('right', 'UMINUS'),
)

# dictionary to store the variable name and value
names = {}

def p_print_var_list(p):
    '''statement : PRINTLIST '''
    if len(names) is not 0:
        for k, v in names.items():
            print(k, "=", v)
    else:
        print("No variables are in the system.")



def p_statement_assign(p):
    '''statement : VAR EQUALS expression
                 | VAR EQUALS equation
                 | VAR EQUALS result'''
    if p[3] is None:
        pass
    else:
        names[p[1]] = p[3]


def p_statement_expr(p):
    '''statement : expression
                 | equation
                 | result'''
    if p[1] is None:
        pass
    else:
        print(p[1])


def p_expression_math(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression'''
    p1 = str(p[1])
    p3 = str(p[3])
    if p[2] == '+' and p[1] is not None and p[3] is not None:
        if "x" in p1 or "x" in p3:
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[1] + p[3]
    elif p[2] == '-' and p[1] is not None and p[3] is not None:
        if "x" in p1 or "x" in p3:
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[1] - p[3]
    elif p[2] == '*' and p[1] is not None and p[3] is not None:
        if "x" in p1 or "x" in p3:
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[1] * p[3]
    elif p[2] == '/' and p[1] is not None and p[3] is not None:
        if "x" in p1 or "x" in p3:
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = p[1] / p[3]
    elif p[2] == '^' and p[1] is not None and p[3] is not None:
        if "x" in p1 or "x" in p3:
            p[0] = str(p[1]) + str(p[2]) + str(p[3])
        else:
            p[0] = math.pow(p[1], p[3])


def p_result_integral(p):
    '''result : INTEGRAL OF expression
                   | INTEGRAL OF equation'''

    if s.find('^') != -1:
        eq = Sphinx_Lexer.formateq(p[3])
    else:
        eq = str(p[3])
    if p[3] is not None:
        eq = (str(Sphinx_Lexer.newintegration(eq, Sphinx_Lexer.symbols('x'))))
        eq = Sphinx_Lexer.reformateq(eq)
        p[0] = eq
    else:
        pass


def p_result_definite_integral(p):
    '''result : INTEGRAL FROM expression TO expression OF expression
              | INTEGRAL FROM expression TO expression OF equation
              | INTEGRAL FROM expression TO INFINITY OF expression
              | INTEGRAL FROM expression TO INFINITY OF equation'''

    lowerbound = str(p[3])
    highbound = str(p[5])
    eq1 = str(p[7])
    if s.find('^') != -1:
        eq = Sphinx_Lexer.formateq(eq1)
    else:
        eq = str(eq1)
    if lowerbound is not None and highbound is not None and p[7] is not None:
        eq = (str(Sphinx_Lexer.newintegration(eq, (Sphinx_Lexer.symbols('x'), lowerbound, highbound))))
        eq = Sphinx_Lexer.reformateq(eq)
        p[0] = eq
    else:
        pass


def p_result_derivative(p):
    '''result : DERIVATIVE OF expression
              | DERIVATIVE OF equation'''

    if s.find('^') != -1:
        eq = Sphinx_Lexer.formateq(p[3])
    else:
        eq = str(p[3])
    if p[3] is not None:
        eq = (str(Sphinx_Lexer.newderivative(eq, Sphinx_Lexer.symbols('x'))))
        eq = Sphinx_Lexer.reformateq(eq)
        p[0] = eq
    else:
        pass


def p_result_limit(p):
    '''result : LIMIT WHEN X GOES expression OF expression
              | LIMIT WHEN X GOES INFINITY OF expression
              | LIMIT WHEN X GOES expression OF equation
              | LIMIT WHEN X GOES INFINITY OF equation'''

    limitOf = str(p[3])
    tendsTo = str(p[5])
    eq1 = str(p[7])

    if s.find('^') != -1:
        eq = Sphinx_Lexer.formateq(eq1)
    else:
        eq = str(eq1)
    if limitOf is not None and tendsTo is not None and p[7] is not None:
        eq = (str(Sphinx_Lexer.limits(eq, Sphinx_Lexer.symbols('x'), tendsTo)))
        eq = Sphinx_Lexer.reformateq(eq)
        p[0] = eq
    else:
        pass


def p_result_summation(p):
    '''result : SUMMATION FROM expression TO expression OF expression
              | SUMMATION FROM expression TO expression OF equation'''

    lowerBound = p[3]
    highBound = p[5]
    eq1 = str(p[7])
    if s.find('^') != -1:
        eq = Sphinx_Lexer.formateq(eq1)
    else:
        eq = str(eq1)
    if lowerBound is not None and highBound is not None and p[7] is not None:
        p[0] = Sphinx_Lexer.summation(eq, lowerBound, highBound, Sphinx_Lexer.symbols('x'))
    else:
        pass


def p_expression_product(p):
    '''result : PRODUCT FROM expression TO expression OF expression
              | PRODUCT FROM expression TO expression OF equation'''

    lowerBound = p[3]
    highBound = p[5]
    eq1 = str(p[7])
    if s.find('^') != -1:
        eq = Sphinx_Lexer.formateq(eq1)
    else:
        eq = str(eq1)
    if lowerBound is not None and highBound is not None and p[7] is not None:
        p[0] = Sphinx_Lexer.productnotation(eq, lowerBound, highBound, Sphinx_Lexer.symbols('x'))
    else:
        pass


def p_equation_more(p):
    '''equation : equation PLUS equation
                  | equation MINUS equation
                  | equation TIMES equation
                  | equation DIVIDE equation
                  | equation POWER equation
                  | equation PLUS expression
                  | equation MINUS expression
                  | equation TIMES expression
                  | equation DIVIDE expression
                  | equation POWER expression
                  | expression PLUS equation
                  | expression MINUS equation
                  | expression TIMES equation
                  | expression DIVIDE equation
                  | expression POWER equation'''
    if p[1] is None or p[3] is None:
        pass
    else:
        p[0] = str(p[1]) + str(p[2]) + str(p[3])


def p_equation_complex(p):
    'equation : X'
    p[0] = str(p[1])


def p_equation_trigonometry(p):
    '''equation : SIN LPAREN expression RPAREN
                | SIN LPAREN equation RPAREN
                | COS LPAREN expression RPAREN
                | COS LPAREN equation RPAREN
                | TAN LPAREN expression RPAREN
                | TAN LPAREN equation RPAREN'''
    p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4])


def p_equation_group(p):
    'equation : LPAREN equation RPAREN'
    print(p[1], p[2], p[3])
    p[0] = str(p[1]) + str(p[2]) + str(p[3])


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_negative(p):
    "equation : MINUS equation %prec UMINUS"
    p[0] = str('-') + str(p[2])


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_basic(p):
    'expression : term'
    p[0] = p[1]


def p_term_number(p):
    '''term : FLOAT
            | INT'''
    p[0] = p[1]


def p_expression_name(p):
    'expression : VAR'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined variable '%s'" % p[1])


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('CASOLUS > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s + '\n')