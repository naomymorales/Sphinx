import sys
import math
import Sphinx_Lexer

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

