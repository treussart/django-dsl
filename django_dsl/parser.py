from ply.yacc import yacc
from datetime import date
from django.db.models import Q
from exceptions import CompileException
from lexer import tokens
from re import match, search


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
    if search(r':True$', field) or search(r':False$', field):
        key, value = field.split(':', 1)
        key = key.strip().replace('.', '__')
        value = value.strip()
        if value == 'False':
            value = False
        elif value == 'True':
            value = True
        else:
            raise CompileException("Parsing error: True or False")
        p[0] = Q(**{key + '__isnull': value})
    elif ':' in field and not search(r'[><=].*:', field):
        key, value = field.split(':', 1)
        key = key.strip().replace('.', '__')
        value = value.strip()
        if value.startswith('~'):
            p[0] = Q(**{key + '__iregex': value[1:]})
        elif value.startswith('*') and value.endswith('*') and not value.endswith('\*'):
            p[0] = Q(**{key + '__icontains': value[1:len(value) - 1]})
        elif value.startswith('*') and value.endswith('\*'):
            p[0] = Q(**{key + '__iendswith': value[1:len(value) - 2] + '*'})
        elif value.startswith('*') and not value.endswith('*'):
            p[0] = Q(**{key + '__iendswith': value[1:]})
        elif value.startswith('\*') and value.endswith('*') and not value.endswith('\*'):
            p[0] = Q(**{key + '__istartswith': '*' + value[2:-1]})
        elif value.startswith('\~') and value.endswith('*') and not value.endswith('\*'):
            p[0] = Q(**{key + '__istartswith': value[1:-1]})
        elif not value.startswith('*') and value.endswith('*') and not value.endswith('\*'):
            p[0] = Q(**{key + '__istartswith': value[0:len(value) - 1]})
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
                if value.startswith('\*'):
                    value = value.replace('\*', '*', 1)
                if value.endswith('\*'):
                    value = value[0:len(value) - 2] + '*'
                if value.startswith('\~'):
                    value = value[1:]
                p[0] = Q(**{key + '__iexact': value})
    elif '>=' in field:
        p[0] = extract(field, '>=', 'gte')
    elif '<=' in field:
        p[0] = extract(field, '<=', 'lte')
    elif '>' in field:
        p[0] = extract(field, '>', 'gt')
    elif '<' in field:
        p[0] = extract(field, '<', 'lt')


def extract(field, pattern, pattern2):
    key, value = field.split(pattern, 1)
    key = key.strip().replace('.', '__')
    value = test_value(value.strip())
    if isinstance(value, date):
        return Q(**{key + '__date__' + pattern2: value})
    else:
        return Q(**{key + '__' + pattern2: value})


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
