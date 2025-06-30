import ply.yacc as yacc
from AnalizadorLexico import tokens

# Inicio de Pacheco
precedence = (
    ('right', 'RETURN'),           # Dar prioridad adecuada a return
    ('nonassoc', 'THEN', 'ELSE', 'ELSIF'),  # Resolver el dangling else
    ('left', 'OR'),                # Operadores lógicos
    ('left', 'AND'),
    ('nonassoc', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUALS', 'NOT_EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),
    ('right', 'NOT'),              # Negación lógica
    ('nonassoc', 'HASH_ROCKET'),
    ('nonassoc', 'RANGE'),         # Para expresiones de rango
)


# Regla de inicio
def p_program(p):
    '''program : statements END
               | statements'''
    print("Programa sintácticamente correcto.")

# Definición de los parámetros de un método
def p_params(p):
    '''params : expression
              | params COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo argumento
    else:
        p[0] = p[1] + [p[3]]  # Varios argumentos

def p_params_declaration(p):
    '''params : IDENTIFIER
              | params COMMA IDENTIFIER
              | params COMMA STRING'''
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
    print(f"Declaración: {p[1]}")
    p[0] = p[1]  # Retorna la expresión como declaración

# Declaración de variables locales y asignación de objetos
def p_local_var(p):
    '''statement : IDENTIFIER ASSIGN STRING
                | IDENTIFIER ASSIGN  expression
                | IDENTIFIER ASSIGN factor'''
    p[0] = f"{p[1]} = {p[3]}" 
    print(f"Variable local {p[1]} asignada con el valor {p[3]}")

# Comienzo Jonathan
def p_global_var(p):
    '''statement : GLOBAL_VAR ASSIGN STRING
                 | GLOBAL_VAR ASSIGN expression
                 | GLOBAL_VAR ASSIGN factor'''
    print(f"Variable global {p[1]} asignada con el valor {p[3]}")
    p[0] = f"{p[1]} = {p[3]}"

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
    '''key_value : STRING HASH_ROCKET expression
                 | STRING HASH_ROCKET STRING
                 | STRING HASH_ROCKET factor
                 | expression HASH_ROCKET expression'''
    p[0] = (p[1], p[3])  # El par clave-valor es un tuple (clave, valor)
    print(f"Par clave-valor: {p[1]} => {p[3]}")

def p_expression_var(p):
    '''expression : IDENTIFIER
                  | GLOBAL_VAR
                  | INSTANCE_VAR'''
    p[0] = p[1]
    print(f"Expresión de variable: {p[1]}")

def p_if_statement(p):
    '''statement : IF expression statements END
                 | IF expression statements ELSE statements END
                 | IF expression statements ELSIF expression statements END
                 | IF expression statements ELSIF expression statements ELSE statements END'''
    print(f"Condición IF: {p[1]}  {p[2]}  {p[3]} con cuerpo {p[3]}")
    if len(p) == 5:  # if ... end
        p[0] = f"if ({p[2]}) {{{p[3]}}}"
        print(f"Condición IF: Si {p[2]} entonces {p[3]}")
    elif len(p) == 6:  # if ... then statement end
        p[0] = f"if ({p[2]}) {{{p[4]}}}"
        print(f"Condición IF con THEN: Si {p[2]} entonces {p[4]}")
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
    '''expression : statement GREATER statement
                  | statement LESS statement
                  | statement GREATER_EQUAL statement
                  | statement LESS_EQUAL statement
                  | statement EQUALS statement
                  | statement NOT_EQUALS statement
                  | statement GREATER factor
                  | statement LESS factor
                  | statement GREATER_EQUAL factor
                  | statement LESS_EQUAL factor
                  | statement EQUALS factor
                  | statement NOT_EQUALS factor'''
    operators = {
        '>': 'mayor que',
        '<': 'menor que',
        '>=': 'mayor o igual que',
        '<=': 'menor o igual que',
        '==': 'igual a',
        '!=': 'diferente de'
    }
    op_text = operators.get(p[2], p[2])
    p[0] = f"{p[1]} {p[2]} {p[3]}"
    print(f"Expresión de comparación: {p[1]} {op_text} {p[3]}")

# Declaración de método sin parámetros
def p_method_without_params_declaration(p):
    '''statement : DEF IDENTIFIER statements END'''
    p[0] = f"def {p[2]} con cuerpo {p[3]}"
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

# Soporte para variables de clase
def p_class_var(p):
    '''statement : CLASS_VAR ASSIGN expression
                 | CLASS_VAR ASSIGN factor'''
    print(f"Variable de clase {p[1]} asignada con el valor {p[3]}")
    p[0] = f"{p[1]} = {p[3]}"

# Soporte para constantes
def p_constant_var(p):
    '''statement : CONSTANT ASSIGN expression
                 | CONSTANT ASSIGN factor'''
    print(f"Constante {p[1]} asignada con el valor {p[3]}")
    p[0] = f"{p[1]} = {p[3]}"

# Soporte para valores booleanos
def p_factor_boolean(p):
    '''factor : TRUE
              | FALSE'''
    p[0] = p[1]
    print(f"Valor booleano: {p[1]}")

# Soporte para nil
def p_factor_nil(p):
    '''factor : NIL'''
    p[0] = 'nil'
    print("Valor nil")

def p_class_definition(p):
    '''statement : CLASS CONSTANT statements END
                 | CLASS CONSTANT LESS CONSTANT statements END
                 | CLASS CONSTANT SEMICOLON END'''
    if len(p) == 5 and p[3] == ';':  # Clase vacía con punto y coma
        p[0] = f"class {p[2]}; end"
        print(f"Definición de clase vacía: {p[2]}")
    elif len(p) == 5:  # Clase normal
        p[0] = f"class {p[2]} {{{p[3]}}}"
        print(f"Definición de clase: {p[2]} con contenido {p[3]}")
    else:  # Clase con herencia
        p[0] = f"class {p[2]} < {p[4]} {{{p[5]}}}"
        print(f"Definición de clase con herencia: {p[2]} hereda de {p[4]} con contenido {p[5]}")

def p_class_method(p):
    '''statement : DEF SELF DOT IDENTIFIER statement END
                 | DEF SELF DOT IDENTIFIER LPAREN params RPAREN statement END'''
    if len(p) == 7:  # Sin parámetros
        p[0] = f"def self.{p[4]} {{{p[5]}}}"
        print(f"Método de clase declarado: {p[4]} con cuerpo {p[5]}")
    else:  # Con parámetros
        p[0] = f"def self.{p[4]}({', '.join(p[6])}) {{{p[8]}}}"
        print(f"Método de clase con parámetros declarado: {p[4]} con parámetros {p[6]} y cuerpo {p[8]}")

# Inicializador (constructor) para clases
def p_initialize_method(p):
    '''statement : DEF INITIALIZE statement END
                 | DEF INITIALIZE LPAREN params RPAREN statement END'''
    if len(p) == 5:  # Sin parámetros
        p[0] = f"def initialize {{{p[3]}}}"
        print(f"Constructor sin parámetros declarado con cuerpo {p[3]}")
    else:  # Con parámetros
        p[0] = f"def initialize({', '.join(p[4])}) {{{p[6]}}}"
        print(f"Constructor con parámetros declarado con parámetros {p[4]} y cuerpo {p[6]}")
# Añadir después de las reglas de clase existentes

# Instanciación de objetos
def p_object_instantiation(p):
    '''expression : CONSTANT DOT NEW
                  | CONSTANT DOT NEW LPAREN RPAREN
                  | CONSTANT DOT NEW LPAREN params RPAREN'''
    if len(p) == 4:  # MyClass.new
        p[0] = f"{p[1]}.new"
        print(f"Instanciación del objeto de clase {p[1]} sin parámetros")
    elif len(p) == 6:  # MyClass.new()
        p[0] = f"{p[1]}.new()"
        print(f"Instanciación del objeto de clase {p[1]} sin parámetros")
    else:  # MyClass.new(param1, param2)
        params_str = ', '.join(p[5])
        p[0] = f"{p[1]}.new({params_str})"
        print(f"Instanciación del objeto de clase {p[1]} con parámetros: {params_str}")
# Fin Jonathan

# Parte de Giovanni 

def p_instance_var(p):
    '''statement : INSTANCE_VAR ASSIGN expression
                | INSTANCE_VAR ASSIGN STRING
                | INSTANCE_VAR ASSIGN factor'''
    print(f"Instance variable {p[1]} assigned with value {p[3]}")
    p[0] = f"{p[1]} = {p[3]}"

def p_set(p):
    '''expression : SET DOT NEW LPAREN elements RPAREN
                  | SET DOT NEW'''
    p[0] = set(p[5]) if p[5] else set()
    print(f"Set created with elements: {p[0]}")


def p_optional_elements(p):
    '''optional_elements : elements
                         | empty'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    p[0] = []

def p_while_statement(p):
    '''statement : WHILE expression statement END
                 | WHILE expression statements END'''
    p[0] = f"while ({p[2]}) {{{p[3]}}}"
    print(f"Bucle while: Mientras {p[2]}, ejecutar {p[3]}")

def p_gets_statement(p):
    '''statement : IDENTIFIER ASSIGN GETS'''
    p[0] = f"{p[1]} = gets"
    print(f"Entrada del usuario almacenada en la variable {p[1]}")
    
def p_method_with_params_declaration(p):
    '''statement : DEF IDENTIFIER LPAREN params RPAREN statements END'''
    print(f"Método con parámetros declarado: {p[2]} con parámetros {p[4]} y cuerpo {p[6]}")

def p_raise_statement(p):
    '''statement : RAISE expression
                 | RAISE STRING'''
    print(f"Raise lanzado con mensaje: {p[2]}")

def p_begin_rescue_ensure(p):
    '''statement : BEGIN statements RESCUE statements ENSURE statements END'''
    print("Bloque begin-rescue-ensure ejecutado")


def p_range_expr(p):
    '''range : expression RANGE expression'''
    p[0] = f"{p[1]}..{p[3]}"

def p_expression_and(p):
    '''expression : expression AND expression'''
    p[0] = f"({p[1]} && {p[3]})"

def p_expression_or(p):
    '''expression : expression OR expression'''
    p[0] = f"({p[1]} || {p[3]})"


# fin de parte de Giovanni

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]
    print(f"Expresión: {p[1]}")

def p_term_div(p):
    '''term : factor DIVIDE factor
            | statement DIVIDE statement
            | factor DIVIDE statement
            | statement DIVIDE factor'''
    p[0] = p[1] / p[3]    

def p_term_times(p):
    '''term : factor TIMES factor
            | statement TIMES statement
            | factor TIMES statement
            | statement TIMES factor'''
    p[0] = p[1] * p[3]

def p_expression_plus(p):
    '''term : factor PLUS factor
            | statement PLUS statement
            | factor PLUS statement
            | statement PLUS factor'''
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    '''term : factor MINUS factor
            | statement MINUS statement
            | factor MINUS statement
            | statement MINUS factor'''
    p[0] = p[1] - p[3]



def p_factor_num(p):
    '''factor : INTEGER
              | FLOAT '''
    p[0] = p[1]


# Arreglo (array)
def p_array(p):
    '''expression : LBRACKET optional_elements RBRACKET'''
    p[0] = p[2]  # Devuelve la lista de elementos dentro del arreglo

# Elementos dentro del arreglo
def p_elements(p):
    '''elements : statement
                | elements COMMA  expression
                | factor COMMA factor
                | elements COMMA factor'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo elemento
    else:
        p[0] = p[1] + [p[3]]  # Lista con más elementos

# Declaración de la estructura `for`
def p_for_statement(p):
    '''statement : FOR IDENTIFIER IN range statements END'''
    print(f"Estructura For: Iterando de {p[3]} con la variable {p[2]} ejecutando {p[5]}")

# Definición del rango (de número a número)
def p_range(p):
    '''range : factor RANGE factor'''
    p[0] = f"{p[1]}..{p[3]}"  # Rango de 1..5

# Impresión con puts
def p_puts_statement(p):
    '''statement : PUTS statement
                | PUTS STRING
                | PUTS factor'''
    print(f"Imprimiendo con puts: {p[2]}")

def p_method_with_return_declaration(p):
    '''statement : DEF IDENTIFIER LPAREN params RPAREN statements RETURN statements END
                |  DEF IDENTIFIER statements RETURN statements END '''
    print(f"Method with parameters declared: {p[2]} with parameters {p[4]} and body {p[6]}")



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
        
        # No devolver el token - permite que el parser intente recuperarse
        return None
    
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
