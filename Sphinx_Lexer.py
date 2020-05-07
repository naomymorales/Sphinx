
#Sphinx Language
# Authors: Julibert Diaz, Angel Hernandez, Anel Martinez, and Naomy Morales

#Lexer for Sphinx

import ply.lex as lex

tokens=['Name','Character','Float','Integer','String','Digit',

        'Plus','Minus','Mult','Div','Modulo','OR','AND','Not',

        'Equals', 'Less','Greater','Less_Equals','Greater_Equals','Not_Equals',

        'MulEquals', 'PlusEquals','MinusEquals','DivEquals','Increment','Decrement','Modequals',

        'Arrow','Question','LeftPar','RPAR','LeftBrac','RightBrac','LeftCurly','RightCurly','Comma','Period',

        'Semicolon','Colon', 'In','Let','For','While','If','Then','Else','To','True','False','Empty','Map','IS_NUMBER','IS_EMPTY',

        'FUNCTION','List','IS_CONS','Cons','First','Append','Rest','Newline','Indent','Dedent','Circumflex',

        'LeftShift','RightShift','DoubleStar','AndEquals','OrEquals','CirEqual','LeftShiftEqual','RightShiftEqual','Doublestar_Equals',

        'DoubleSlash','DoubleSlashEquals','At','AtEquals','Ellipsis','ColonEqual','Comment','None','Await',

        'Break','Class','As','Assert','Elif','Async','Continue','Def','Del','Except','Import','Try','Finally','Global','IS',

        'From','Lambda','Pass','Raise','Return','With'

        ]

#Whitespace
t_ignore=r' '

#Comments
t_Comment=r'\#'

#Types
t_Integer=r'\d+([uU]|[1L]|[uU][1L]|[1L][uU])?'
t_Float=r'((\d+)(\.\d+)(e(\+|-)?(\d+))?|(\d+)e(\+|-)?(/d+))([1L]|[fF])?'
t_String=r'\"([^\\\n]|(\\.))*?\"'

#Operators
t_Plus=r'\+'
t_Minus=r'-'
t_Mult=r'\*'
t_Div=r'/'
t_Modulo=r'%'
t_OR=r'\|'
t_AND=r'&'
t_Not=r'~'
t_Circumflex=r'\^'
t_Less=r'<'
t_Greater=r'>'
t_Less_Equals=r'<='
t_Greater_Equals=r'>='
t_Not_Equals=r'!='
t_LeftShift=r'<<'
t_RightShift=r'>>'
t_DoubleStar=r'\*\*'
t_DoubleSlash=r'//'

#Assignment
t_Equals='='
t_MulEquals=r'\*='
t_PlusEquals=r'\+='
t_MinusEquals=r'-='
t_DivEquals=r'/='
t_Modequals=r'%='
t_AndEquals=r'&='
t_OrEquals=r'\|='
t_CirEqual=r'^='
t_LeftShiftEqual=r'<<='
t_RightShiftEqual=r'>>='
t_Doublestar_Equals=r'\*\*='
t_DoubleSlashEquals=r'//='
t_ColonEqual=r':='
t_AtEquals=r'@='

#Delimiters
t_LeftPar=r'\('
t_RPAR= r'\)'
t_LeftBrac=r'\['
t_RightBrac=r'\]'
t_LeftCurly=r'\{'
t_RightCurly=r'\}'
t_Comma=r','
t_Period=r'\.'
t_Semicolon=r';'
t_Colon=r':'
t_Ellipsis=r'\.\.\.'

#Other

t_Arrow=r'->'
t_Question=r'\?'
t_At=r'\@'
t_Increment=r'\++'
t_Decrement=r'--'

#Reserved
t_None=r'None'
t_Await=r'await'
t_Break=r'break'
t_Class=r'class'
t_As=r'as'
t_Assert=r'assert'
t_Async=r'async'
t_Continue=r'continue'
t_Def=r'def'
t_Del=r'del'
t_Elif=r'elif'
t_Except=r'except'
t_Try=r'try'
t_Finally=r'finally'
t_From=r'from'
t_Global=r'global'
t_Import=r'import'
t_IS=r'is'
t_Lambda=r'lambda'
t_Pass=r'pass'
t_Raise='raise'
t_Return='return'
t_With='with'

t_Let=r'let'
t_In=r'in'
t_For=r'for'
t_While=r'while'
t_Map=r'map'
t_If=r'if'
t_Then=r'then'
t_Else='else'
t_To='to'
t_Empty='empty'
t_True=r'true'
t_False=r'false'
t_IS_NUMBER=r'number?'
t_FUNCTION=r'function?'
t_List=r'list?'
t_IS_EMPTY=r'list?'
t_IS_CONS=r'cons?'
t_Cons=r'cons'
t_First=r'first'
t_Rest=r'rest'


def t_Character(t):
    r'[a-z A-z_]'
    t.type = 'Character'
    return t

def t_Name(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value in tokens:
        t.type=tokens[t.value]
    else:
        t.type='Name'
    return t

def t_DIGIT(t):
    r'[0-9]'
    t.type = 'Digit'
    return t

def t_Newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Error detection
def t_error(t):
    print('Illegal character')
    t.lexer.skip(1)

#Builds lexer

lexer=lex.lex()

#Testing it
lexer.input("()is it working 2010-09 := ? _ @")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)





