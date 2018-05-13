import ply.yacc as yacc
from django.db.models import Q
from .exceptions import CompileException
from .lexer import tokens


assert tokens


def p_expression_and(p):
    '''expression : expression AND expression'''
    p[0] = p[1] & p[3]


def p_expression_or(p):
    '''expression : expression OR expression'''
    p[0] = p[1] | p[3]


def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = ~ p[2]


def p_expression_paren(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_expression_field(p):
    'expression : FIELD'
    field = str(p[1])
    key, value = field.split(':')
    if value.startswith('~'):
        p[0] = Q(**{key.strip().replace('.', '__') + '__iregex': value.strip()[1:]})
    elif value.startswith('*') and not value.endswith('*'):
        p[0] = Q(**{key.strip().replace('.', '__') + '__iendswith': value.strip().replace("*", "")})
    elif value.endswith('*') and not value.startswith('*'):
        p[0] = Q(**{key.strip().replace('.', '__') + '__istartswith': value.strip().replace("*", "")})
    elif value.endswith('*') and value.startswith('*'):
        p[0] = Q(**{key.strip().replace('.', '__') + '__icontains': value.strip().replace("*", "")})
    else:
        p[0] = Q(**{key.strip().replace('.', '__'): value.strip()})


def p_error(p):
    if p:
        raise CompileException(u"Parsing error around token: %s" % p.value)
    raise CompileException(u"Parsing error: unexpected end of expression")


precedence = (
    ('left', 'AND', 'OR'),
    ('right', 'NOT'),
)


def build_parser():
    return yacc.yacc()
