from .lexer import build_lexer
from .parser import build_parser


def compile(expr):
    # create separate lexer and parser for each compilation
    # to be thread-safe
    lexer = build_lexer()
    parser = build_parser()
    # now, parse!
    return parser.parse(expr, lexer=lexer)
