from ply.yacc import yacc
from django.db.models import Q
from exceptions import CompileException
from lexer import tokens


assert tokens

yacc.yaccdebug = False


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
    if ':' in field:
        key, value = field.split(':')
        key = key.strip().replace('.', '__')
        value = value.strip()
        if value.startswith('~'):
            p[0] = Q(**{key + '__iregex': value[1:]})
        elif value.startswith('*') and not value.endswith('*'):
            p[0] = Q(**{key + '__iendswith': value[1:]})
        elif value.endswith('*') and not value.startswith('*'):
            p[0] = Q(**{key + '__istartswith': value[:-1]})
        elif value.endswith('*') and value.startswith('*'):
            p[0] = Q(**{key + '__icontains': value[1:-1]})
        else:
            p[0] = Q(**{key + '__iexact': value})
    elif '>=' in field:
        key, value = field.split('>=')
        key = key.strip().replace('.', '__')
        p[0] = Q(**{key + '__gte': int(value)})
    elif '<=' in field:
        key, value = field.split('<=')
        key = key.strip().replace('.', '__')
        p[0] = Q(**{key + '__lte': int(value)})
    elif '>' in field:
        key, value = field.split('>')
        key = key.strip().replace('.', '__')
        p[0] = Q(**{key + '__gt': int(value)})
    elif '<' in field:
        key, value = field.split('<')
        key = key.strip().replace('.', '__')
        p[0] = Q(**{key + '__lt': int(value)})


def p_error(p):
    if p:
        raise CompileException(u"Parsing error around token: %s" % p.value)
    raise CompileException(u"Parsing error: unexpected end of expression")


precedence = (
    ('left', 'AND', 'OR'),
    ('right', 'NOT'),
)


def build_parser():
    return yacc()
