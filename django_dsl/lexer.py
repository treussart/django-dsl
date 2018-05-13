import ply.lex as lex
from exceptions import CompileException
from datetime import date


# List of token names.   This is always required
tokens = (
    'LPAREN',
    'RPAREN',
    'FIELD',
    'AND',
    'OR',
    'NOT',
)

# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_FIELD = r'[A-Za-z0-9\_\.]+(:|<|>|<=|>=)[A-Za-z0-9\_\~\*\.\^\$\?\{\}\[\]\|\!\\\/\+\-éèàû]+'
t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    raise CompileException("Compilation Error : Cannot make sense of : %s" % t.value)


def t_DATE(t):
    r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
    day = int(t.lexer.lexmatch.group('day'))
    month = int(t.lexer.lexmatch.group('month'))
    year = int(t.lexer.lexmatch.group('year'))
    t.value = date(year, month, day)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def build_lexer():
    return lex.lex()
