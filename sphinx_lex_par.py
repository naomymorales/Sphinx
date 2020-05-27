# @authors: Anel Martinez, Naomy Morales, Julibert Diaz, Angel Hernandez
# Sphinx Programming Language

import sys
import math
import Math_Functions_V2
import ply.lex as lex
import ply.yacc as yacc

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

# Lexer Analysis

# Reserved mathematical words
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
tokens = ['CHARACTER', 'VAR', 'FLOAT', 'INT', 'PLUS', 'MINUS', 'MULT', 'DIV',
          'POWER', 'EQUALS', 'LPAR', 'RPAR', 'COMMA', 'GOES', 'X',] + list(reserved.values())

# Format For Variables and Token Representation
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


# Variable
def t_VAR(t):
    r'[a-wyzA-WYZ][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VAR')  # Check for reserved words
    return t


# String characters
def t_CHARACTER(t):
    r'[a-z A-z_]'
    t.type = reserved.get(t.value, 'CHARACTER')
    return t


# Floating point
def t_FLOAT(t):
    r'([0-9]+)?([.][0-9]+)([eE][+-]?[0-9]+)?'
    t.value = float(t.value)
    return t


# Integer
def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


# When there is a new line
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Making comments
def t_COMMENT(t):
    r'\#.*'
    pass


# If an error occurs
def t_error(t):
    print("ERROR: Line %d: LEXER: Illegal character '%s'!! " % (t.lexer.lineno, t.value[0]))
    t.lexer.skip(1)


# LEXER BUILD
lex.lex()

# Parsing rules and precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('left', 'POWER'),
    ('right', 'SIGN'),
)

names = {}

#STATEMENTS
# Printing variables
def p_list(p):
    '''statement : PRINTLIST '''
    if len(names) is not 0:
        for keys, values in names.items():
            print(keys, "=", values)
    else:
        print("Names is 0 :(")


# Assigning variables
def p_assign_state(p):
    '''statement : VAR EQUALS expression
                 | VAR EQUALS equation
                 | VAR EQUALS result'''
    if p[3] is None:
        pass
    else:
        names[p[1]] = p[3]


# Defining Statement
def p_expr_statement(p):
    '''statement : expression
                 | equation
                 | result'''
    if p[1] is None:
        pass
    else:
        print(p[1])

#EXPRESSIONS
# An expression can be a variable
def p_expression_name(p):
    'expression : VAR'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined variable '%s'" % p[1])


# Defining polynomials
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


# Defining a quadratic function
def p_quadratic(p):
    '''expression : term CHARACTER POWER term PLUS term CHARACTER PLUS term
                  | term CHARACTER POWER term PLUS term CHARACTER MINUS term
                  | term CHARACTER POWER term MINUS term CHARACTER PLUS term
                  | term CHARACTER POWER term MINUS term CHARACTER MINUS term'''
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


# Expressing coordinates in the grammar rules
def p_coordinates_exp(p):
    '''expression : LPAR term COMMA term RPAR'''
    if p[2] is not None and p[4] is not None:
        p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5])
    else:
        pass


# Expression encased in parenthesis
def p_expression_group(p):
    "expression : LPAR expression RPAR"
    p[0] = p[2]


# reverses sign
def p_expression_sign(p):
    "expression : MINUS expression %prec SIGN"
    p[0] = -p[2]


# Simple expression
def p_expression_basic(p):
    'expression : term'
    p[0] = p[1]




#TERM
def p_term(p):
    '''term : FLOAT
            | INT'''
    p[0] = p[1]

#RESULTS
# Representing a quadratic result
def p_quadratic_result(p):
    '''result : term CHARACTER POWER term PLUS term CHARACTER PLUS term
                  | term CHARACTER POWER term PLUS term CHARACTER MINUS term
                  | term CHARACTER POWER term MINUS term CHARACTER PLUS term
                  | term CHARACTER POWER term MINUS term CHARACTER MINUS term'''
    if p[2] == p[7] and p[4] == 2:
        a = str(p[1])
        b = str(p[6])
        c = str(p[9])
        eq = (str(Math_Functions_V2.Quadratic(a, b, c)))
        eq = Math_Functions_V2.reformat(eq)
        p[0] = eq
    else:
        pass


#Volume
def p_volume_result_sphere(p):
    '''result : term MULT term MULT VAR POWER term DIV term'''
    if p[1] == 4 and p[3] == math.pi and p[6] == 3 and p[8] == 3:
        a = str(p[5])
        b = 0
        c = 0
        equation = (str(Math_Functions_V2.SurfaceArea("sphere", a, b, c)))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass


def p_volume_result_cone(p):
    '''result : term MULT VAR POWER VAR DIV term'''
    if p[1] == math.pi and p[4] == 2 and p[7] == 3:
        a = str(p[4])
        b = str(p[5])
        c = 0
        equation = (str(Math_Functions_V2.SurfaceArea("cone", a, b, c)))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass

def p_volume_result_cube(p):
    '''result : VAR POWER term'''
    if p[3] == 3:
        a = str(p[1])
        b = 0
        c = 0
        equation = (str(Math_Functions_V2.SurfaceArea("cube", a, b, c)))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass

def p_volume_result_cylinder(p):
    '''result : term VAR POWER term VAR'''
    if p[1] == math.pi and p[4] == 2:
        a = str(p[2])
        b = str(p[5])
        c = 0
        equation = (str(Math_Functions_V2.SurfaceArea("cylinder", a, b, c)))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass

def p_volume_result_spyramid(p):
    '''result : VAR POWER term VAR DIV term'''
    if p[3] == 2 and p[6] == 3:
        a = str(p[1])
        b = str(p[4])
        c = 0
        equation = (str(Math_Functions_V2.SurfaceArea("square pyramid", a, b, c)))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass

def p_volume_result_tube(p):
    '''result : term LPAR VAR POWER term MINUS VAR RPAR DIV term'''
    if p[1] == math.pi and p[5] == 2 and p[10] == 4:
        a = str(p[5])
        b = 0
        c = 0
        equation = (str(Math_Functions_V2.SurfaceArea("tube", a, b, c)))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass

def p_volume_result_capsule(p):
    '''result : term MULT term MULT VAR POWER term DIV term'''
    if p[1] == 4 and p[3] == math.pi and p[6] == 3 and p[8] == 3:
        a = str(p[5])
        b = 0
        c = 0
        equation = (str(Math_Functions_V2.SurfaceArea("sphere", a, b, c)))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass



# Integrals
def p_result_integral(p):
    '''result : INTEGRAL OF expression
                   | INTEGRAL OF equation'''

    if s.find('^') != -1:
        equation = Math_Functions_V2.format(p[3])
    else:
        equation = str(p[3])
    if p[3] is not None:
        equation = (str(Math_Functions_V2.integration(equation, Math_Functions_V2.symbols('x'))))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass


def p_result_integral_definida(p):
    '''result : INTEGRAL FROM expression TO expression OF expression
              | INTEGRAL FROM expression TO expression OF equation
              | INTEGRAL FROM expression TO INFINITY OF expression
              | INTEGRAL FROM expression TO INFINITY OF equation'''

    lowerLimit = str(p[3])
    upperLimit = str(p[5])
    firstEquation = str(p[7])
    if s.find('^') != -1:
        equation = Math_Functions_V2.format(firstEquation)
    else:
        equation = str(firstEquation)
    if lowerLimit is not None and upperLimit is not None and p[7] is not None:
        equation = (str(Math_Functions_V2.integration(equation, (Math_Functions_V2.symbols('x'), lowerLimit, upperLimit))))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass


# Defining derivatives
def p_result_derivation(p):
    '''result : DERIVATIVE OF expression
              | DERIVATIVE OF equation'''

    if s.find('^') != -1:
        equation = Math_Functions_V2.format(p[3])
    else:
        equation = str(p[3])
    if p[3] is not None:
        equation = (str(Math_Functions_V2.derivation(equation, Math_Functions_V2.symbols('x'))))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass


# Limits
def p_result_limit(p):
    '''result : LIMIT WHEN X GOES expression OF expression
              | LIMIT WHEN X GOES INFINITY OF expression
              | LIMIT WHEN X GOES expression OF equation
              | LIMIT WHEN X GOES INFINITY OF equation'''

    limit = str(p[3])
    tendency = str(p[5])
    firstEquation = str(p[7])

    if s.find('^') != -1:
        equation = Math_Functions_V2.format(firstEquation)
    else:
        equation = str(firstEquation)
    if limit is not None and tendency is not None and p[7] is not None:
        equation = (str(Math_Functions_V2.limits(equation, Math_Functions_V2.symbols('x'), tendency)))
        equation = Math_Functions_V2.reformat(equation)
        p[0] = equation
    else:
        pass


# Defining a Summation
def p_result_summation(p):
    '''result : SUMMATION FROM expression TO expression OF expression
              | SUMMATION FROM expression TO expression OF equation'''

    base = p[3]
    limitOf = p[5]
    firstEquation = str(p[7])
    if s.find('^') != -1:
        equation = Math_Functions_V2.format(firstEquation)
    else:
        equation = str(firstEquation)
    if base is not None and limitOf is not None and p[7] is not None:
        p[0] = Math_Functions_V2.summation(equation, base, limitOf, Math_Functions_V2.symbols('x'))
    else:
        pass


# Defining a factorial
def p_result_factorial(p):
    '''result : INT'''
    if p[1] is not None:
        n = p[1]
        p[0] = Math_Functions_V2.Factorial(n)
    else:
        pass


# def p_result_CartToPolar(p):
#     '''result : LPAR FLOAT COMMA FLOAT RPAR'''
#     if p[2] is not None and p[4] is not None:
#         x = p[2]
#         y = p[4]
#         p[0] = Math_Functions_V2.Cartersian_To_Polar(x, y)
#     else:
#         pass

# Defining the conversion of polar to cartesian
def p_result_PolarToCart(p):
    '''result : LPAR term COMMA term RPAR'''
    if p[2] is not None and p[4] is not None:
        x = p[2]
        y = p[4]
        if Math_Functions_V2.Cartersian_To_Polar():
            p[0] = Math_Functions_V2.Cartersian_To_Polar(x, y)
        elif Math_Functions_V2.Polar_To_Cartersian():
            p[0] = Math_Functions_V2.Polar_To_Cartersian(x, y)
    else:
        pass


# Defining the conversion of degress to radians
def p_result_DegToRads(p):
    '''result : term'''
    if p[1] is not None:
        x = p[1]
        if Math_Functions_V2.Degrees_To_Radians():
            p[0] = Math_Functions_V2.Degrees_To_Radians(x)
        elif Math_Functions_V2.Radians_To_Degrees():
            p[0] = Math_Functions_V2.Radians_To_Degrees(x)
    else:
        pass


# def p_result_RadsToDeg(p):
#     '''result : FLOAT'''
#     if p[1] is not None:
#         rad = p[1]
#         p[0] = Math_Functions_V2.Degrees_To_Radians(rad)
#     else:
#         pass

# Defining magnitude function
def p_result_magnitude(p):
    '''result : term term'''
    if p[1] is not None and p[2] is not None:
        x = p[1]
        y = p[2]
        p[0] = Math_Functions_V2.Magnitude(x, y)
    else:
        pass


# Defining magnitude function for 3 variables

def p_result_MagnitudeOfThree(p):
    '''result : term term term'''
    if p[1] is not None and p[2] is not None and p[3] is not None:
        x = p[1]
        y = p[2]
        z = p[3]
        p[0] = Math_Functions_V2.Magnitude_With_3_Variables(x, y, z)
    else:
        pass


# Defining distance
def p_result_DistanceBetweenTwo(p):
    '''result : term term term term'''
    if p[1] is not None and p[2] is not None and p[3] is not None and p[4] is not None:
        x1 = p[1]
        y1 = p[2]
        x2 = p[3]
        y2 = p[4]
        p[0] = Math_Functions_V2.Distance_Between_Two_Points(x1, y1, x2, y2)
    else:
        pass


# Rule for a product
def p_product_exp(p):
    '''result : PRODUCT FROM expression TO expression OF expression
              | PRODUCT FROM expression TO expression OF equation'''

    base = p[3]
    limitOf = p[5]
    firstEquation = str(p[7])
    if s.find('^') != -1:
        equation = Math_Functions_V2.format(firstEquation)
    else:
        equation = str(firstEquation)
    if base is not None and limitOf is not None and p[7] is not None:
        p[0] = Math_Functions_V2.notationProduct(equation, base, limitOf, Math_Functions_V2.symbols('x'))
    else:
        pass


#EQUATION
# Defining an equation
def p_equation_additions(p):
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


# Rule for a complex equation
def p_equation_complex(p):
    'equation : X'
    p[0] = str(p[1])


# Rule for a trigonometric equation
def p_trigonometry(p):
    '''equation : SIN LPAR expression RPAR
                | SIN LPAR equation RPAR
                | COS LPAR expression RPAR
                | COS LPAR equation RPAR
                | TAN LPAR expression RPAR
                | TAN LPAR equation RPAR'''
    p[0] = str(p[1]) + str(p[2]) + str(p[3]) + str(p[4])


# Equation encased in parenthesis
def p_equation_group(p):
    'equation : LPAR equation RPAR'
    print(p[1], p[2], p[3])
    p[0] = str(p[1]) + str(p[2]) + str(p[3])


# Rule for a negative expression
def p_expression_negative(p):
    "equation : MINUS equation %prec SIGN"
    p[0] = str('-') + str(p[2])


#ERROR
# If an error occurs
def p_error(p):
    if p:
        print("There is a syntax error at '%s'" % p.value)
    else:
        print("There is a syntax error at EOF")


# Parser Run


yacc.yacc()

# Testing
while 1:
    try:
        s = raw_input('Sphinx : ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s + '\n')


#######NOTES :
#######THERE ARE STILL SOME OTHER FUNCTIONS THAT NEED SOME TWEEKING AND SOME REMAIN WANTED TO BE ADDED#######