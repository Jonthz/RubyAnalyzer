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
# Parte de GIOVANNI
# Definición de los tokens
tokens = [
    'DEF', 'IDENTIFIER', 'LBRACKET', 'RBRACKET', 'ASSIGN',
    'LPAREN', 'RPAREN', 'HASH_ROCKET' ,'FOR', 'IN', 'DOT', 'RANGE', 'MINUS', 'GETS', 'SET',
    'PLUS', 'GREATER', 'WHILE', 'END', 'RETURN', 'COMMENT', 'STRING',
#fin de GIOVANNI
    'LBRACE', 'RBRACE', 'PIPE', 'COMMA', 'SEMICOLON', 
    'EQUALS', 'LESS', 'TIMES', 'DIVIDE', 'MOD', 'POWER',
    'FLOAT', 'GLOBAL_VAR', 'INSTANCE_VAR', 'CLASS_VAR',
    'AND', 'OR', 'NOT', 'NOT_EQUALS', 'GREATER_EQUAL', 'LESS_EQUAL', 'SPACESHIP'
]
# Parte de GIOVANNI
# Definición de las expresiones regulares para los tokens
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_HASH_ROCKET = r'=>'
#fin de GIOVANNI
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
# Parte de GIOVANNI
t_DOT = r'\.'

t_RANGE = r'\.\.|\.{3}'
t_MINUS = r'-'
t_PLUS = r'\+'
t_GREATER = r'>'
#fin de GIOVANNI
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_POWER = r'\*\*'
t_EQUALS = r'=='
t_LESS = r'<'
#GIOVANNI

t_NOT_EQUALS = r'!='
t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_SPACESHIP = r'<=>'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_SET = r'Set'
t_GETS = r'gets'


# Parte de GIOVANNI
#=== Parte de Darwin ====
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_POWER_ASSIGN = r'\*\*='
t_FLOOR_DIVIDE = r'//'
t_BITWISE_AND = r'\&'
t_PIPE = r'\|'
t_QUESTION_MARK = r'\?'  
#=== Parte de Jonathan ====

tokens.extend([
    'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN',
    'DIVIDE_ASSIGN', 'MOD_ASSIGN', 'POWER_ASSIGN', 'FLOOR_DIVIDE','BITWISE_AND', 'PUTS', 'QUESTION_MARK'
])
#=== Parte de Darwin ====

# Para las palabras clave, se definen como variables
keywords = {
    'def': 'DEF',
    'for': 'FOR',
    'in': 'IN',
    'while': 'WHILE',
    'end': 'END',
    'return': 'RETURN',
    'puts': 'PUTS',
    'gets': 'GETS',
    'Set': 'SET',
    'new': 'NEW'
}
#fin de GIOVANNI

# Parte de GIOVANNI

# Agregar las palabras clave al conjunto de tokens
for keyword in keywords:
    globals()[f't_{keywords[keyword]}'] = r'\b' + keyword + r'\b'


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*\??'
    # Primero verificar si es una palabra clave
    t.type = keywords.get(t.value, None)
    if t.type is None:
        # Si no es palabra clave, entonces verificar si es constante o identificador
        if t.value[0].isupper():
            t.type = 'CONSTANT'
        else:
            t.type = 'IDENTIFIER'
    return t
#fin de GIOVANNI


#=== Parte de Darwin ====
def t_FLOAT(t):
    r'\b\d+\.\d+\b'
    t.value = float(t.value)
    return t

# Parte de GIOVANNI
#=== Parte de Darwin ====

def t_STRING(t):
    r'\"[^\"]*\"|\'[^\']*\''
    t.value = t.value[1:-1]
    return t


def t_COMMENT(t):
    r'\#.*'
    pass  # Ignorar comentarios
#fin de GIOVANNI
def t_GLOBAL_VAR(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_INSTANCE_VAR(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_CLASS_VAR(t):
    r'@@[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'CLASS_VAR'  # Asegúrate de asignar un tipo para que PLY lo reconozca
    return t
# Parte de GIOVANNI
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

error_tokens = [] 

def t_error(t):
    error_message = f"Error léxico: {t.value[0]} en la línea {t.lineno}"
    error_tokens.append(error_message)  # Guardamos el error en la lista
    print(error_message)  # Imprimir el error en consola
    t.lexer.skip(1)
#fin de GIOVANNI
#=== Parte de Jonathan ====
tokens.extend([
    'THEN','INTEGER', 'TRUE', 'FALSE',
    'IF', 'ELSIF', 'ELSE', 'UNTIL', 'NEXT', 'BREAK', 'REDO', 'RETRY', 'CASE', 'WHEN',
    'CLASS', 'MODULE',
    'BEGIN', 'RESCUE', 'ENSURE', 'RAISE', 'NIL',
    'DO', 'LAMBDA', 'PROC', 'YIELD', 'SELF', 'SUPER', 'REQUIRE',
    'CONSTANT', 'NEW', 'INITIALIZE'
])


# Add boolean values to the keywords dictionary
keywords.update({
    'then': 'THEN',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'elsif': 'ELSIF',
    'else': 'ELSE',
    'until': 'UNTIL',
    'next': 'NEXT',
    'break': 'BREAK',
    'redo': 'REDO',
    'retry': 'RETRY',
    'case': 'CASE',
    'when': 'WHEN',
    'class': 'CLASS',
    'module': 'MODULE',
    'begin': 'BEGIN',
    'rescue': 'RESCUE',
    'ensure': 'ENSURE',
    'raise': 'RAISE',
    'nil': 'NIL',
    'do': 'DO',
    'lambda': 'LAMBDA',
    'proc': 'PROC',
    'yield': 'YIELD',
    'self': 'SELF',
    'super': 'SUPER',
    'require': 'REQUIRE',''
    'new': 'NEW',
    'initialize': 'INITIALIZE'
})

def t_MULTILINE_COMMENT(t):
    r'=begin(?:.|\n)*?=end'
    t.lexer.lineno += t.value.count('\n')  # Actualiza el contador de líneas
    pass

def t_INTEGER(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t

#=== Parte de Jonathan ====


# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Crear el analizador léxico
lexer = lex.lex()

#=== Parte de Darwin ====

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
    print(f"Análisis léxico completado. Logs guardados en: {os.path.abspath('logs')}")
    print(f"Tokens reconocidos:\n{tokens}")
    print(f"Errores léxicos: {error_tokens}")

#=== Parte de Darwin ====


