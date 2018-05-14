from ply.yacc import yacc
from datetime import date
from django.db.models import Q
from exceptions import CompileException
from lexer import tokens
from re import match


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
    if ':True' in field or ':False' in field:
        key, value = field.split(':', 1)
        key = key.strip().replace('.', '__')
        value = value.strip()
        if value == 'False':
            value = False
        else:
            value = True
        p[0] = Q(**{key + '__isnull': value})
    elif ':' in field:
        key, value = field.split(':', 1)
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
            if match(r'(?P<startyear>\d{4})-(?P<startmonth>\d{1,2})-(?P<startday>\d{1,2})_(?P<endyear>\d{4})-'
                     r'(?P<endmonth>\d{1,2})-(?P<endday>\d{1,2})', value):
                t = match(r'(?P<startyear>\d{4})-(?P<startmonth>\d{1,2})-(?P<startday>\d{1,2})_'
                          r'(?P<endyear>\d{4})-(?P<endmonth>\d{1,2})-(?P<endday>\d{1,2})', value)
                p[0] = Q(**{key + '__range': (date(int(t.group('startyear')),
                                                   int(t.group('startmonth')),
                                                   int(t.group('startday'))),
                                              date(int(t.group('endyear')),
                                                   int(t.group('endmonth')),
                                                   int(t.group('endday'))))})
            else:
                p[0] = Q(**{key + '__iexact': value})
    elif '>=' in field:
        key, value = field.split('>=', 1)
        key = key.strip().replace('.', '__')
        value = test_value(value.strip())
        if isinstance(value, date):
            p[0] = Q(**{key + '__date__gte': value})
        else:
            p[0] = Q(**{key + '__gte': value})
    elif '<=' in field:
        key, value = field.split('<=', 1)
        key = key.strip().replace('.', '__')
        value = test_value(value.strip())
        if isinstance(value, date):
            p[0] = Q(**{key + '__date__lte': value})
        else:
            p[0] = Q(**{key + '__lte': value})
    elif '>' in field:
        key, value = field.split('>', 1)
        key = key.strip().replace('.', '__')
        value = test_value(value.strip())
        if isinstance(value, date):
            p[0] = Q(**{key + '__date__gt': value})
        else:
            p[0] = Q(**{key + '__gt': value})
    elif '<' in field:
        key, value = field.split('<', 1)
        key = key.strip().replace('.', '__')
        value = test_value(value.strip())
        if isinstance(value, date):
            p[0] = Q(**{key + '__date__lt': value})
        else:
            p[0] = Q(**{key + '__lt': value})


def test_value(value):
    if match(r'^\d+$', value):
        return int(value)
    else:
        t = match(r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})', value)
        if t:
            return date(int(t.group('year')), int(t.group('month')), int(t.group('day')))
        else:
            raise CompileException("Parsing error: value not an integer or a date")


def p_error(p):
    if p:
        raise CompileException("Parsing error around token: %s" % p.value)
    raise CompileException("Parsing error: unexpected end of expression")


precedence = (
    ('left', 'AND', 'OR'),
    ('right', 'NOT'),
)


def build_parser():
    return yacc()
