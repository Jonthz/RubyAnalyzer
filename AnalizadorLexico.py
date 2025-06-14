import ply.lex as lex

# Definición de los tokens
tokens = [
    'DEF', 'IDENTIFIER', 'INTEGER', 'LBRACKET', 'RBRACKET', 'ASSIGN',
    'LPAREN', 'RPAREN', 'FOR', 'IN', 'DOT', 'RANGE', 'MINUS',
    'PLUS', 'GREATER', 'WHILE', 'END', 'RETURN', 'COMMENT', 'STRING'
]

# Definición de las expresiones regulares para los tokens
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOT = r'\.'
t_RANGE = r'\.\.|\.{3}'
t_MINUS = r'-'
t_PLUS = r'\+'
t_GREATER = r'>'


# Para las palabras clave, se definen como variables
keywords = {
    'def': 'DEF',
    'for': 'FOR',
    'in': 'IN',
    'while': 'WHILE',
    'end': 'END',
    'return': 'RETURN'
}

# Agregar las palabras clave al conjunto de tokens
for keyword in keywords:
    globals()[f't_{keywords[keyword]}'] = r'\b' + keyword + r'\b'


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

#Jonathan
def t_INTEGER(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\"[^\"]*\"|\'[^\']*\''
    t.value = t.value[1:-1]
    return t


def t_COMMENT(t):
    r'\#.*'
    pass  # Ignorar comentarios


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)

#Jonathan
# Define tokens for boolean values in Ruby
tokens.extend(['TRUE', 'FALSE'])

# Add boolean values to the keywords dictionary
keywords.update({
    'true': 'TRUE',
    'false': 'FALSE'
})

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Crear el analizador léxico
lexer = lex.lex()


lexer.input('''
def suma(a, b)
  return a + b
end''')
# Analizar el código
for token in lexer:
    print(token)

