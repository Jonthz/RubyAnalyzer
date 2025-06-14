import ply.lex as lex
import time
import os
import subprocess

# Función para obtener el nombre de usuario de GitHub
def get_github_username():
    try:
        # Ejecuta el comando git config para obtener el nombre de usuario de Git
        username = subprocess.check_output(["git", "config", "--get", "user.name"]).decode('utf-8').strip()
        return username
    except subprocess.CalledProcessError:
        return "usuarioGit"  # Valor predeterminado en caso de que no se encuentre el usuario

# Definición de los tokens
tokens = [
    'DEF', 'IDENTIFIER', 'NUMBER', 'LBRACKET', 'RBRACKET', 'ASSIGN',
    'LPAREN', 'RPAREN', 'FOR', 'IN', 'DOT', 'RANGE', 'MINUS',
    'PLUS', 'GREATER', 'WHILE', 'END', 'RETURN', 'COMMENT', 'STRING',
    'LBRACE', 'RBRACE', 'PIPE', 'COMMA', 'SEMICOLON', 'EQUALS', 'LESS', 'TIMES', 'DIVIDE', 'MOD', 'POWER'
]

# Definición de las expresiones regulares para los tokens
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PIPE = r'\|'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'
t_RANGE = r'\.\.|\.{3}'
t_MINUS = r'-'
t_PLUS = r'\+'
t_GREATER = r'>'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_POWER = r'\*\*'
t_EQUALS = r'=='
t_LESS = r'<'

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


def t_NUMBER(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\b\d+\.\d+\b'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'\"[^\"]*\"|\'[^\']*\''
    t.value = t.value[1:-1]
    return t


def t_COMMENT(t):
    r'\#.*'
    pass  # Ignorar comentarios

def t_GLOBAL_VAR(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_INSTANCE_VAR(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_CLASS_VAR(t):
    r'@@[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

error_tokens = [] 

def t_error(t):
    error_message = f"Error léxico: {t.value[0]} en la línea {t.lineno}"
    error_tokens.append(error_message)  # Guardamos el error en la lista
    print(error_message)  # Imprimir el error en consola
    t.lexer.skip(1)
# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Crear el analizador léxico
lexer = lex.lex()

# Función para registrar los logs con tokens y errores
def log_tokens_and_errors(tokens, errors):
    # Obtén el nombre de usuario de GitHub
    username = get_github_username()
    
    timestamp = time.strftime("%d-%m-%Y-%Hh%M")
    log_dir = 'logs'
    
    # Crear la carpeta de logs si no existe
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Crear el nombre del archivo de log
    log_filename = f"{log_dir}/lexico-{username}-{timestamp}.txt"

    # Registrar los tokens y los errores en el archivo de log
    with open(log_filename, 'w') as log_file:
        if tokens:
            log_file.write("Tokens reconocidos:\n")
            for token in tokens:
                log_file.write(f"{token}\n")
        else:
            log_file.write("No se reconocieron tokens válidos.\n")

        if errors:
            log_file.write("\nErrores léxicos:\n")
            for error in errors:
                log_file.write(f"{error}\n")
        if not tokens and not errors:
            log_file.write("No tokens recognized or lexical error.\n")

# Función de prueba para el analizador léxico
def test_lexical_analyzer(input_data):
    global error_tokens  # Usamos la lista global para los errores
    error_tokens = []  # Reiniciamos la lista de errores antes de cada prueba

    lexer.input(input_data)
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append(f"{token.type}: {token.value}")
    
    # Registra tanto los tokens como los errores encontrados
    log_tokens_and_errors(tokens, error_tokens)
    print(f"Tokens reconocidos:\n{tokens}")
    print(f"Errores léxicos: {error_tokens}")

# Prueba con un fragmento de código de Ruby
input_data = """
def quick_sort(arr)
  return arr if arr.length <= 1
  pivot = arr.delete_at(arr.length / 2)
  left, right = arr.partition { |x| x < pivot }
  return *quick_sort(left), pivot, *quick_sort(right)
end
"""

test_lexical_analyzer(input_data)