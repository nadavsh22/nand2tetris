import re

KEYWORD = 1
SYMBOL = 2
INT_CONST = 3
STRING_CONST = 4
IDENTIFIER = 5
OLD_SUFFIX = "jack"
NEW_SUFFIX = "xml"
elementDict = {KEYWORD: 'keyword', SYMBOL: 'symbol', INT_CONST:
    'integerConstant', STRING_CONST: 'stringConstant', IDENTIFIER:
                   'identifier'}

# REGEX
LEXICAL_ELEMENTS_MATCHES = ['KEYWORD', 'SYMBOL', 'INT_CONST', 'STRING_CONST',
                            'IDENTIFIER']
KEYWORD_REGEX = (
"((class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)(\t|\r|\n)+)")
keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void',
            'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
SYMBOLS_REGEX = '([{}()[\].,;+~=/\-*|&<>])'
INT_CON_REGEX = '(\d+)'
STR_CON_REGEX = '(\\"[^\n"]*.\\")'
IDENT_REGEX = '([A-Za-z_]\w*)'

# merging all the different regex's
LEXICAL_ELEMENTS = '{}|{}|{}|{}|{}'.format(KEYWORD_REGEX, SYMBOLS_REGEX, INT_CON_REGEX,
                                           STR_CON_REGEX, IDENT_REGEX)
LEXICAL_ELEMENTS_REGEX = re.compile(LEXICAL_ELEMENTS)
COMMENT_REGEX = re.compile(r'/\*(.*?)\*/|\/\*.*\*\/|//.[^\n]*[^\";]',
                           re.MULTILINE | re.DOTALL)  # //.[^\n]*[^\";]

symbDict = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}

# use and identify
TOKEN_ERROR = -1
