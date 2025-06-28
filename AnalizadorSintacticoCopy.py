import ply.yacc as yacc
from AnalizadorLexico import tokens
import os
import datetime
from AnalizadorLexico import get_github_username

# ==========================================================================
# CONFIGURACIÓN DE PRECEDENCIA
# ==========================================================================
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

# ==========================================================================
# ESTRUCTURA BÁSICA DEL PROGRAMA
# ==========================================================================
# Regla de inicio
def p_program(p):
    '''program : statements END
               | statements'''
    print("Programa sintácticamente correcto.")

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo statement
    else:
        p[0] = p[1] + [p[2]]  # Varias declaraciones, agregamos el nuevo

def p_statement(p):
    '''statement :  expression'''
    print(f"Declaración: {p[1]}")
    p[0] = p[1]  # Retorna la expresión como declaración

# eliminado stament_block 

# ==========================================================================
# PARÁMETROS Y ELEMENTOS
# ==========================================================================
def p_params(p):
    '''params : expression
              | params COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo argumento
    else:
        p[0] = p[1] + [p[3]]  # Varios argumentos

def p_params_empty(p):
    '''params : empty'''
    p[0] = []  # Parámetros vacíos

def p_optional_elements(p):
    '''optional_elements : elements
                         | empty'''
    p[0] = p[1]

def p_elements(p):
    '''elements : expression
                | elements COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo elemento
    else:
        p[0] = p[1] + [p[3]]  # Lista con más elementos

def p_empty(p):
    '''empty :'''
    p[0] = []

# ==========================================================================
# EXPRESIONES Y TÉRMINOS ARITMÉTICOS
# ==========================================================================
def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]
    print(f"Expresión: {p[1]}")

def p_expression_var(p):
    '''expression : IDENTIFIER
                  | GLOBAL_VAR
                  | INSTANCE_VAR
                  | CLASS_VAR
                  | CONSTANT'''
    p[0] = p[1]
    print(f"Expresión de variable: {p[1]}")

def p_term_single_factor(p):
    '''term : factor'''
    p[0] = p[1]
    print(f"Término: {p[1]}")

def p_term_div(p):
    '''term : expression DIVIDE expression'''
    p[0] = p[1] / p[3]    

def p_term_times(p):
    '''term : expression TIMES expression'''
    p[0] = p[1] * p[3]

def p_expression_plus(p):
    '''term : expression PLUS expression'''
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    '''term : expression MINUS expression'''
    p[0] = p[1] - p[3]

def p_factor_num(p):
    '''factor : INTEGER
              | FLOAT '''
    p[0] = p[1]

def p_factor_string(p):
    'factor : STRING'
    p[0] = p[1]

def p_factor_power(p):
    'factor : factor POWER factor'
    p[0] = p[1] ** p[3]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_boolean(p):
    '''factor : TRUE
              | FALSE'''
    p[0] = p[1]
    print(f"Valor booleano: {p[1]}")

def p_factor_nil(p):
    '''factor : NIL'''
    p[0] = 'nil'
    print("Valor nil")

# ==========================================================================
# EXPRESIONES LÓGICAS Y DE COMPARACIÓN
# ==========================================================================
def p_expression_and(p):
    '''expression : expression AND expression'''
    p[0] = f"({p[1]} && {p[3]})"

def p_expression_or(p):
    '''expression : expression OR expression'''
    p[0] = f"({p[1]} || {p[3]})"


# Revisar si se necesita una regla para NOT
def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = f"(!{p[2]})"
    print(f"Expresión lógica NOT: {p[2]} negada a {p[0]}")
# Revisar si factor comparacion factor es necesario o podriamos reducirlo a statement comparacion statement

def p_expression_simbols(p):
    '''comparisonSimbol: GREATER
                     | LESS
                     | GREATER_EQUAL
                     | LESS_EQUAL
                     | EQUALS
                     | NOT_EQUALS'''

def p_expression_comparison(p):
    '''expression : expression comparisonSimbol expression
                  | LPAREN structureControlIf RPAREN comparisonSimbol LPAREN structureControl RPAREN
                  | p_vars comparisonSimbol p_vars'''
                
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

# ==========================================================================
# VARIABLES Y ASIGNACIONES
# ==========================================================================
def p_vars_statement(p):
    '''statement : p_vars
                 | p_gets_statement'''
    p[0] = p[1]  # Retorna la variable o la asignación


def p_vars(p):
    '''p_vars : p_local_var
    | p_global_var
    | p_instance_var
    | p_class_var
    | p_constant_var'''

def p_local_var(p):
    '''p_local_var : IDENTIFIER ASSIGN statement'''
    p[0] = f"{p[1]} = {p[3]}" 
    print(f"Variable local {p[1]} asignada con el valor {p[3]}")

def p_global_var(p):
    '''p_global_var : GLOBAL_VAR ASSIGN statement'''
    print(f"Variable global {p[1]} asignada con el valor {p[3]}")
    p[0] = f"{p[1]} = {p[3]}"

def p_instance_var(p):
    '''p_instance_var : INSTANCE_VAR ASSIGN statement'''
    print(f"Instance variable {p[1]} assigned with value {p[3]}")
    p[0] = f"{p[1]} = {p[3]}"

def p_class_var(p):
    '''p_class_var : CLASS_VAR ASSIGN statement'''
    print(f"Variable de clase {p[1]} asignada con el valor {p[3]}")
    p[0] = f"{p[1]} = {p[3]}"

def p_constant_var(p):
    '''p_constant_var : CONSTANT ASSIGN statement'''
    print(f"Constante {p[1]} asignada con el valor {p[3]}")
    p[0] = f"{p[1]} = {p[3]}"

def p_gets_statement(p):
    '''p_gets_statement : IDENTIFIER ASSIGN GETS'''
    p[0] = f"{p[1]} = gets"
    print(f"Entrada del usuario almacenada en la variable {p[1]}")

# ==========================================================================
# ESTRUCTURAS DE CONTROL
# ==========================================================================
def p_structure_control(p):
    '''statement : structureControl'''
    p[0] = p[1]  # Retorna la estructura de control

def p_structure_control_expression(p):
    '''structureControl: structureControlIf
    | structureControlWhile
    | structureControlFor'''

def p_if_statement(p):
    '''structureControlIf : IF expression statements END
                 | IF expression statements ELSE statements END
                 | IF expression statements ELSIF expression statements END
                 | IF expression statements ELSIF expression statements ELSE statements END'''
    print(f"Condición IF: {p[1]}  {p[2]}  {p[3]} con cuerpo {p[3]}")
    #semantico
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

def p_while_statement(p):
    '''structureControlWhile : WHILE expression statement END
                 | WHILE expression statements END'''
    p[0] = f"while ({p[2]}) {{{p[3]}}}"
    print(f"Bucle while: Mientras {p[2]}, ejecutar {p[3]}")

def p_for_statement(p):
    '''structureControlFor : FOR IDENTIFIER IN range statements END'''
    print(f"Estructura For: Iterando de {p[3]} con la variable {p[2]} ejecutando {p[5]}")

def p_range(p):
    '''range : factor RANGE factor'''
    p[0] = f"{p[1]}..{p[3]}"  # Rango de 1..5

def p_range_expr(p):
    '''range : expression RANGE expression'''
    p[0] = f"{p[1]}..{p[3]}"

# ver si nos ponemos a hacer los en linea

# ==========================================================================
# COLECCIONES (ARRAYS, HASHES, SETS)
# ==========================================================================
def p_array(p):
    '''expression : LBRACKET optional_elements RBRACKET'''
    p[0] = p[2]  # Devuelve la lista de elementos dentro del arreglo

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

def p_set(p):
    '''expression : SET DOT NEW LPAREN elements RPAREN
                  | SET DOT NEW'''
    p[0] = set(p[5]) if len(p) > 4 else set()
    print(f"Set created with elements: {p[0]}")

# ==========================================================================
# MÉTODOS Y CLASES
# ==========================================================================
def p_method_without_params_declaration(p):
    '''statement : DEF IDENTIFIER statements END'''
    p[0] = f"def {p[2]} con cuerpo {p[3]}"
    print(f"Método sin parámetros declarado: {p[2]} con cuerpo {p[3]}")

def p_method_with_params_declaration(p):
    '''statement : DEF IDENTIFIER LPAREN params RPAREN statements END'''
    print(f"Método con parámetros declarado: {p[2]} con parámetros {p[4]} y cuerpo {p[6]}")
    p[0] = f"def {p[2]}({', '.join(map(str, p[4]))}) {{{p[6]}}}"

def p_method_with_return_declaration(p):
    '''statement : DEF IDENTIFIER LPAREN params RPAREN statements RETURN statements END
                |  DEF IDENTIFIER statements RETURN statements END '''
    if len(p) == 10:  # Con parámetros y return
        p[0] = f"def {p[2]}({', '.join(map(str, p[4]))}) {{{p[6]}; return {p[8]}}}"
    else:  # Sin parámetros, con return
        p[0] = f"def {p[2]} {{{p[3]}; return {p[5]}}}"
    print(f"Method with return declared: {p[2]}")

def p_method_call_without_params(p):
    '''statement : IDENTIFIER'''
    if isinstance(p[1], str) and p[1] not in ['puts', 'gets', 'print']:
        # Solo identificadores que no sean palabras reservadas
        p[0] = p[1]
        print(f"Llamada al método sin parámetros: {p[1]}")
    else:
        p[0] = p[1]

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
        p[0] = f"def self.{p[4]}({', '.join(map(str, p[6]))}) {{{p[8]}}}"
        print(f"Método de clase con parámetros declarado: {p[4]} con parámetros {p[6]} y cuerpo {p[8]}")

def p_initialize_method(p):
    '''statement : DEF INITIALIZE statement END
                 | DEF INITIALIZE LPAREN params RPAREN statement END'''
    if len(p) == 5:  # Sin parámetros
        p[0] = f"def initialize {{{p[3]}}}"
        print(f"Constructor sin parámetros declarado con cuerpo {p[3]}")
    else:  # Con parámetros
        p[0] = f"def initialize({', '.join(map(str, p[4]))}) {{{p[6]}}}"
        print(f"Constructor con parámetros declarado con parámetros {p[4]} y cuerpo {p[6]}")

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
        params_str = ', '.join(map(str, p[5]))
        p[0] = f"{p[1]}.new({params_str})"
        print(f"Instanciación del objeto de clase {p[1]} con parámetros: {params_str}")

# ==========================================================================
# ENTRADA/SALIDA
# ==========================================================================
def p_puts_statement(p):
    '''statement : PUTS statement
                | PUTS STRING
                | PUTS factor'''
    print(f"Imprimiendo con puts: {p[2]}")
    p[0] = f"puts {p[2]}"

# ==========================================================================
# MANEJO DE ERRORES Y EXCEPCIONES
# ==========================================================================
def p_begin_rescue_ensure(p):
    '''statement : BEGIN statements RESCUE statements ENSURE statements END'''
    print("Bloque begin-rescue-ensure ejecutado")
    p[0] = f"begin {{{p[2]}}} rescue {{{p[4]}}} ensure {{{p[6]}}}"

def p_raise_statement(p):
    '''statement : RAISE expression
                 | RAISE STRING'''
    print(f"Raise lanzado con mensaje: {p[2]}")
    p[0] = f"raise {p[2]}"

def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}: Token inesperado '{p.value}'")
    else:
        print("Error de sintaxis: Fin de archivo inesperado.")

# ==========================================================================
# INICIALIZACIÓN Y UTILIDADES
# ==========================================================================
# Crear el analizador sintáctico
parser = yacc.yacc()

def test_parser(input_code):
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