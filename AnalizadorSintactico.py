import ply.yacc as yacc
from AnalizadorLexico import tokens

# Inicio de Pacheco
precedence = (
    ('nonassoc', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUALS', 'NOT_EQUALS'),  # Comparaciones
    ('left', 'PLUS', 'MINUS'),  # Suma y resta
    ('left', 'TIMES', 'DIVIDE'),  # Multiplicación y división
    ('right', 'POWER'),  # Exponenciación
    ('right', 'HASH_ROCKET'),  # Para los hashes
)


# Regla de inicio
def p_program(p):
    '''program : statements END
               | statements'''
    print("Programa sintácticamente correcto.")

# Definición de los parámetros de un método
def p_params(p):
    '''params : IDENTIFIER
              | params COMMA IDENTIFIER'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo parámetro
    else:
        p[0] = p[1] + [p[3]]  # Varios parámetros, agregamos el nuevo

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo statement
    else:
        p[0] = p[1] + [p[2]]  # Varias declaraciones, agregamos el nuevo

# Definición de una declaración
def p_statement(p):
    '''statement :  expression'''

# Declaración de variables locales
def p_local_var(p):
    '''statement : IDENTIFIER ASSIGN INTEGER
                 | IDENTIFIER ASSIGN FLOAT'''
    print(f"Variable local {p[1]} asignada con el valor {p[3]}")

# Comienzo Jonathan
def p_global_var(p):
    '''statement : GLOBAL_VAR ASSIGN STRING
                 | GLOBAL_VAR ASSIGN expression'''
    print(f"Variable global {p[1]} asignada con el valor {p[3]}")

def p_factor_power(p):
    'factor : factor POWER factor'
    p[0] = p[1] ** p[3]

def p_factor_string(p):
    'factor : STRING'
    p[0] = p[1]

def p_hash(p):
    '''expression : LBRACE key_value_pairs RBRACE'''
    p[0] = dict(p[2])  # Convierte la lista de pares clave-valor en un diccionario
    print(f"Hash creado con {len(p[2])} pares clave-valor")

def p_empty_hash(p):
    '''expression : LBRACE RBRACE'''
    p[0] = {}  # Hash vacío
    print("Hash vacío creado")

def p_key_value_pairs(p):
    '''key_value_pairs : key_value
                       | key_value_pairs COMMA key_value'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo par clave-valor
    else:
        p[0] = p[1] + [p[3]]  # Varios pares clave-valor

def p_key_value(p):
    '''key_value : expression HASH_ROCKET expression'''
    p[0] = (p[1], p[3])  # El par clave-valor es un tuple (clave, valor)
    print(f"Par clave-valor: {p[1]} => {p[3]}")

def p_expression_var(p):
    '''expression : IDENTIFIER
                  | GLOBAL_VAR
                  | INSTANCE_VAR'''
    p[0] = p[1]

def p_statement_block(p):
    '''statement : statement statement'''
    p[0] = f"{p[1]}; {p[2]}" if p[1] and p[2] else p[1] or p[2]

def p_if_statement(p):
    '''statement : IF expression statement END
                 | IF expression statement ELSE statement END
                 | IF expression statement ELSIF expression statement END
                 | IF expression statement ELSIF expression statement ELSE statement END'''
    if len(p) == 5:  # if ... end
        p[0] = f"if ({p[2]}) {{{p[3]}}}"
        print(f"Condición IF: Si {p[2]} entonces {p[3]}")
    elif len(p) == 7:  # if ... else ... end
        p[0] = f"if ({p[2]}) {{{p[3]}}} else {{{p[5]}}}"
        print(f"Condición IF-ELSE: Si {p[2]} entonces {p[3]} sino {p[5]}")
    elif len(p) == 8:  # if ... elsif ... end
        p[0] = f"if ({p[2]}) {{{p[3]}}} else if ({p[5]}) {{{p[6]}}}"
        print(f"Condición IF-ELSIF: Si {p[2]} entonces {p[3]} sino si {p[5]} entonces {p[6]}")
    else:  # if ... elsif ... else ... end
        p[0] = f"if ({p[2]}) {{{p[3]}}} else if ({p[5]}) {{{p[6]}}} else {{{p[8]}}}"
        print(f"Condición IF-ELSIF-ELSE: Si {p[2]} entonces {p[3]} sino si {p[5]} entonces {p[6]} sino {p[8]}")

# Para permitir expresiones de comparación
def p_expression_comparison(p):
    '''expression : expression GREATER expression
                  | expression LESS expression
                  | expression GREATER_EQUAL expression
                  | expression LESS_EQUAL expression
                  | expression EQUALS expression
                  | expression NOT_EQUALS expression'''
    operators = {
        '>': 'mayor que',
        '<': 'menor que',
        '>=': 'mayor o igual que',
        '<=': 'menor o igual que',
        '==': 'igual a',
        '!=': 'diferente de'
    }
    op_text = operators.get(p[2], p[2])
    p[0] = f"{p[1]} {op_text} {p[3]}"

# Declaración de método sin parámetros
def p_method_without_params_declaration(p):
    '''statement : DEF IDENTIFIER statement END'''
    p[0] = f"def {p[2]} {p[3]}"
    print(f"Método sin parámetros declarado: {p[2]} con cuerpo {p[3]}")

# Llamada a métodos sin parámetros
def p_method_call_without_params(p):
    '''statement : IDENTIFIER'''  # Elimina la línea | expression
    if isinstance(p[1], str) and p[1] not in ['puts', 'gets', 'print']:
        # Solo identificadores que no sean palabras reservadas
        p[0] = p[1]
        print(f"Llamada al método sin parámetros: {p[1]}")
    else:
        p[0] = p[1]



# Fin Jonathan

# Parte de Giovanni 

def p_instance_var(p):
    '''statement : INSTANCE_VAR ASSIGN INTEGER
                 | INSTANCE_VAR ASSIGN FLOAT'''
    print(f"Instance variable {p[1]} assigned with value {p[3]}")

def p_set(p):
    '''statement : SETNEW LPAREN optional_elements RPAREN'''
    p[0] = set(p[3]) if p[3] else set()
    print(f"Set created with elements: {p[0]}")

def p_optional_elements(p):
    '''optional_elements : elements
                         | empty'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = []

def p_while_statement(p):
    '''statement : WHILE expression statement END'''
    print(f"While loop: While {p[2]}, execute {p[3]}")

def p_gets_statement(p):
    '''statement : IDENTIFIER ASSIGN GETS'''
    print(f"User input stored in variable {p[1]}")
    
def p_method_with_params_declaration(p):
    '''statement : DEF IDENTIFIER LPAREN params RPAREN statement END'''
    print(f"Method with parameters declared: {p[2]} with parameters {p[4]} and body {p[6]}")

def p_method_call_with_params(p):
    '''statement : IDENTIFIER LPAREN params RPAREN'''
    print(f"Method call: {p[1]} with arguments {p[3]}")

# fin de parte de Giovanni

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_div(p):
    'term : factor DIVIDE factor'
    p[0] = p[1] / p[3]    

def p_term_times(p):
    'term : factor TIMES factor'
    p[0] = p[1] * p[3]

def p_expression_plus(p):
    'expression : expression PLUS factor'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS factor'
    p[0] = p[1] - p[3]


def p_factor_num(p):
    '''factor : INTEGER
              | FLOAT '''
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Arreglo (array)
def p_array(p):
    '''expression : LBRACKET elements RBRACKET'''
    p[0] = p[2]  # Devuelve la lista de elementos dentro del arreglo

# Elementos dentro del arreglo
def p_elements(p):
    '''elements : expression
                | elements COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo elemento
    else:
        p[0] = p[1] + [p[3]]  # Lista con más elementos

# Declaración de la estructura `for`
def p_for_statement(p):
    '''statement : FOR IDENTIFIER IN range statement'''
    print(f"Estructura For: Iterando de {p[3]} con la variable {p[2]} ejecutando {p[5]}")

# Definición del rango (de número a número)
def p_range(p):
    '''range : INTEGER DOUBLE_DOT INTEGER
             | FLOAT DOUBLE_DOT FLOAT'''
    p[0] = f"{p[1]}..{p[3]}"  # Rango de 1..5

# Impresión con puts
def p_puts_statement(p):
    '''statement : PUTS statement'''
    print(f"Imprimiendo con puts: {p[2]}")

# Manejo de errores
def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: Token inesperado '{p.value}'")
    else:
        print("Error de sintaxis: Fin de archivo inesperado.")

# Crear el analizador sintáctico
parser = yacc.yacc()

def test_parser(input_code):
    import os
    import datetime
    from AnalizadorLexico import get_github_username
    
    print("Parsing Ruby code:")
    print(input_code)
    
    # Crear directorio de logs si no existe
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Obtener nombre de usuario de GitHub
    username = get_github_username()
    
    # Obtener fecha y hora actual
    now = datetime.datetime.now()
    date_str = now.strftime("%d%m%Y")
    time_str = now.strftime("%Hh%M")
    
    # Nombre del archivo de log
    log_filename = f"{log_dir}/sintactico-{username}-{date_str}-{time_str}.txt"
    
    # Lista para almacenar errores
    syntax_errors = []
    
    # Crear una variable para saber si hubo errores
    had_errors = [False]
    
    # Función personalizada para manejar errores
    def custom_error_handler(p):
        had_errors[0] = True
        if p:
            error_msg = f"Error sintáctico en línea {p.lineno if hasattr(p, 'lineno') else 'desconocida'}: Token inesperado '{p.value}'"
            syntax_errors.append(error_msg)
            print(error_msg)
        else:
            error_msg = "Error sintáctico: Fin de archivo inesperado"
            syntax_errors.append(error_msg)
            print(error_msg)
        return p
    
    # Guardar referencia al analizador original
    global parser
    original_parser = parser
    
    # Crear un nuevo analizador con nuestra función de error
    parser = yacc.yacc(errorlog=yacc.NullLogger())
    parser.errorfunc = custom_error_handler
    
    # Realizar el análisis
    try:
        result = parser.parse(input_code)
        if not had_errors[0]:
            syntax_errors.append("No se encontraron errores sintácticos")
    except Exception as e:
        syntax_errors.append(f"Error durante el análisis: {str(e)}")
    
    # Restaurar el analizador original
    parser = original_parser
    
    # Escribir el log
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        log_file.write(f"=== Análisis Sintáctico de Código Ruby ===\n")
        log_file.write(f"Fecha: {now.strftime('%d/%m/%Y')}\n")
        log_file.write(f"Hora: {now.strftime('%H:%M:%S')}\n")
        log_file.write(f"Usuario: {username}\n\n")
        
        log_file.write("--- Código Analizado ---\n")
        log_file.write(input_code)
        log_file.write("\n\n--- Resultados del Análisis ---\n")
        
        for error in syntax_errors:
            log_file.write(f"{error}\n")
    
    print(f"Análisis sintáctico completado. Logs guardados en: {os.path.abspath(log_filename)}")
    print("Parse finished.")

__all__ = ["parser", "test_parser"]
