import sys
import math
import Math_Functions_V2

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

# LEXER ANALYSIS


reserved = {
    'when': 'WHEN',
    'of': 'OF',
    'if': 'IF',
    'from': 'FROM',
    'to': 'TO',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'limit': 'LIMIT',
    'summation': 'SUMMATION',
    'product': 'PRODUCT',
    'integral': 'INTEGRAL',
    'derivation': 'DERIVATIVE',
    'inf': 'INFINITY',
    'varlist': 'PRINTLIST',
}

# Tokens

tokens = [
             'CHARACTER',
             'VAR',
             'FLOAT',
             'INT',
             'PLUS',
             'MINUS',
             'MULT',
             'DIV',
             'POWER',
             'RAD',
             'EQUALS',
             'LPAR',
             'RPAR',
             'COMMA',
             'GOES',
             'X',
         ] + list(reserved.values())

#Format For Variables and Token Representation
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_POWER = r'\^'
t_EQUALS = r'\='
t_LPAR = r'\('
t_RPAR = r'\)'
t_COMMA = r'\,'
t_GOES = r'\->'
t_X = r'[x]'
t_ignore = " \t"


def t_VAR(t):
    r'[a-wyzA-WYZ][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VAR')  # Check for reserved words
    return t


def t_CHARACTER(t):
    r'[a-z A-z_]'
    t.type = reserved.get(t.value, 'CHARACTER')
    return t

def t_FLOAT(t):
    r'([0-9]+)?([.][0-9]+)([eE][+-]?[0-9]+)?'
    t.value = float(t.value)
    return t


def t_RAD(t):
    r'r+a+d'
    t.value = reserved.get(t.value, 'RAD')
    return t



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
    print("ERROR: Line %d: LEXER: Illegal character '%s' " % (t.lexer.lineno, t.value[0]))
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()
# Parsing rules and precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
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


def p_polynomial(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression
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


def p_quadratic(p):
    '''expression : FLOAT CHARACTER POWER INT PLUS FLOAT CHARACTER PLUS FLOAT
                  | FLOAT CHARACTER POWER INT PLUS FLOAT CHARACTER MINUS FLOAT
                  | FLOAT CHARACTER POWER INT MINUS FLOAT CHARACTER PLUS FLOAT
                  | FLOAT CHARACTER POWER INT MINUS FLOAT CHARACTER MINUS FLOAT'''
    if p[4] == 2 and p[2] == p[7] and p[5] == '+' and p[8] == '+':
        p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5]) + str(p[6]) + str(p[7]) + str(p[8]) + str(p[9])
    elif p[4] == 2 and p[2] == p[7] and p[5] == '+' and p[8] == '-':
        p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5]) + str(p[6]) + str(p[7]) + str(p[8]) + str(p[9])
    elif p[4] == 2 and p[2] == p[7] and p[5] == '-' and p[8] == '+':
        p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5]) + str(p[6]) + str(p[7]) + str(p[8]) + str(p[9])
    elif p[4] == 2 and p[2] == p[7] and p[5] == '-' and p[8] == '-':
        p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5]) + str(p[6]) + str(p[7]) + str(p[8]) + str(p[9])
    else:
        pass


def p_coordinates_exp(p):
    '''expression : LPAR FLOAT COMMA FLOAT RPAR'''
    if p[2] is not None and p[4] is not None:
        p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5])
    else:
        pass


def p_result_quadratic(p):
    '''result : FLOAT CHARACTER POWER INT PLUS FLOAT CHARACTER PLUS FLOAT
                  | FLOAT CHARACTER POWER INT PLUS FLOAT CHARACTER MINUS FLOAT
                  | FLOAT CHARACTER POWER INT MINUS FLOAT CHARACTER PLUS FLOAT
                  | FLOAT CHARACTER POWER INT MINUS FLOAT CHARACTER MINUS FLOAT'''
    if p[2] == p[7] and p[4] == 2:
        a = str(p[1])
        b = str(p[6])
        c = str(p[9])
        eq = (str(Math_Functions_V2.Quadratic(a, b, c)))
        eq = Math_Functions_V2.reformateq(eq)
        p[0] = eq
    else:
        pass


def p_result_integral(p):
    '''result : INTEGRAL OF expression
                   | INTEGRAL OF equation'''

    if s.find('^') != -1:
        eq = Math_Functions_V2.formateq(p[3])
    else:
        eq = str(p[3])
    if p[3] is not None:
        eq = (str(Math_Functions_V2.newintegration(eq, Math_Functions_V2.symbols('x'))))
        eq = Math_Functions_V2.reformateq(eq)
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
        eq = Math_Functions_V2.formateq(eq1)
    else:
        eq = str(eq1)
    if lowerbound is not None and highbound is not None and p[7] is not None:
        eq = (str(Math_Functions_V2.newintegration(eq, (Math_Functions_V2.symbols('x'), lowerbound, highbound))))
        eq = Math_Functions_V2.reformateq(eq)
        p[0] = eq
    else:
        pass


def p_result_derivative(p):
    '''result : DERIVATIVE OF expression
              | DERIVATIVE OF equation'''

    if s.find('^') != -1:
        eq = Math_Functions_V2.formateq(p[3])
    else:
        eq = str(p[3])
    if p[3] is not None:
        eq = (str(Math_Functions_V2.newderivative(eq, Math_Functions_V2.symbols('x'))))
        eq = Math_Functions_V2.reformateq(eq)
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
        eq = Math_Functions_V2.formateq(eq1)
    else:
        eq = str(eq1)
    if limitOf is not None and tendsTo is not None and p[7] is not None:
        eq = (str(Math_Functions_V2.limits(eq, Math_Functions_V2.symbols('x'), tendsTo)))
        eq = Math_Functions_V2.reformateq(eq)
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
        eq = Math_Functions_V2.formateq(eq1)
    else:
        eq = str(eq1)
    if lowerBound is not None and highBound is not None and p[7] is not None:
        p[0] = Math_Functions_V2.summation(eq, lowerBound, highBound, Math_Functions_V2.symbols('x'))
    else:
        pass


def p_result_factorial(p):
    '''result : INT'''
    if p[1] is not None:
        n = p[1]
        p[0] = Math_Functions_V2.Factorial(n)
    else:
        pass

# def p_result_CartToPolar(p):
#     '''result : LPAREN FLOAT COMMMA FLOAT RPAREN'''
#     if p[2] is not None and p[4] is not None:
#         x = p[2]
#         y = p[4]
#         p[0] = Sphinx_Lexer.Cartersian_To_Polar(x, y)
#     else:
#         pass


def p_result_PolarToCart(p):
    '''result : LPAR FLOAT COMMA FLOAT RPAR'''
    if p[2] is not None and p[4] is not None:
        x = p[2]
        y = p[4]
        if Sphinx_Lexer.Cartersian_To_Polar():
            p[0] = Sphinx_Lexer.Cartersian_To_Polar(x,y)
        elif Sphinx_Lexer.Polar_To_Cartersian():
            p[0] = Sphinx_Lexer.Polar_To_Cartersian(x,y)
    else:
        pass


def p_result_DegToRads(p):
    '''result : FLOAT'''
    if p[1] is not None:
        x = p[1]
        if Sphinx_Lexer.Degrees_To_Radians():
            p[0] = Sphinx_Lexer.Degrees_To_Radians(x)
        elif Sphinx_Lexer.Radians_To_Degrees():
            p[0] = Sphinx_Lexer.Radians_To_Degrees(x)
    else:
        pass


# def p_result_RadsToDeg(p):
#     '''result : FLOAT'''
#     if p[1] is not None:
#         rad = p[1]
#         p[0] = Sphinx_Lexer.Degrees_To_Radians(rad)
#     else:
#         pass


def p_result_magnitude(p):
    '''result : FLOAT FLOAT'''
    if p[1] is not None and p[2] is not None:
        x = p[1]
        y = p[2]
        p[0] = Sphinx_Lexer.Magnitude(x, y)
    else:
        pass


def p_result_MagnitudeOfThree(p):
    '''result : FLOAT FLOAT FLOAT'''
    if p[1] is not None and p[2] is not None and p[3] is not None:
        x = p[1]
        y = p[2]
        z = p[3]
        p[0] = Sphinx_Lexer.Magnitude(x, y, z)
    else:
        pass


def p_result_DistanceBetweenTwo(p):
    '''result : FLOAT FLOAT FLOAT FLOAT'''
    if p[1] is not None and p[2] is not None and p[3] is not None and p[4] is not None:
        x1 = p[1]
        y1 = p[2]
        x2 = p[3]
        y2 = p[4]
        p[0] = Sphinx_Lexer.Distance_Between_Two_Points(x1, y1, x2, y2)
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
                  | equation MULT equation
                  | equation DIV equation
                  | equation POWER equation
                  | equation PLUS expression
                  | equation MINUS expression
                  | equation MULT expression
                  | equation DIV expression
                  | equation POWER expression
                  | expression PLUS equation
                  | expression MINUS equation
                  | expression MULT equation
                  | expression DIV equation
                  | expression POWER equation'''
    if p[1] is None or p[3] is None:
        pass
    else:
        p[0] = str(p[1]) + str(p[2]) + str(p[3])


def p_equation_complex(p):
    'equation : X'
    p[0] = str(p[1])


def p_equation_trigonometry(p):
    '''equation : SIN LPAR expression RPAR
                | SIN LPAR equation RPAR
                | COS LPAR expression RPAR
                | COS LPAR equation RPAR
                | TAN LPAR expression RPAR
                | TAN LPAR equation RPAR'''
    p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4])


def p_equation_group(p):
    'equation : LPAR equation RPAR'
    print(p[1], p[2], p[3])
    p[0] = str(p[1]) + str(p[2]) + str(p[3])


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_negative(p):
    "equation : MINUS equation %prec UMINUS"
    p[0] = str('-') + str(p[2])


def p_expression_group(p):
    "expression : LPAR expression RPAR"
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

#Parser Run
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