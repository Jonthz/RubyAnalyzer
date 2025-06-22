import ply.yacc as yacc
from AnalizadorLexico import tokens

# Inicio de Pacheco
precedence = (
    ('left', 'PLUS', 'MINUS'),  # Suma y resta tienen la menor precedencia
    ('left', 'TIMES', 'DIVIDE'),  # Multiplicación y división tienen mayor precedencia
    ('right', 'POWER'),  # Exponenciación tiene la mayor precedencia
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

# Parte de Giovanni 

def p_instance_var(p):
    '''statement : INSTANCE_VAR ASSIGN INTEGER
                 | INSTANCE_VAR ASSIGN FLOAT'''
    print(f"Instance variable {p[1]} assigned with value {p[3]}")

def p_set(p):
    '''expression : SETNEW LPAREN elements RPAREN'''
    p[0] = set(p[3])
    print(f"Set created with elements: {p[0]}")

def p_while_statement(p):
    '''statement : WHILE expression statement END'''
    print(f"While loop: While {p[2]}, execute {p[3]}")

def p_gets_statement(p):
    '''statement : IDENTIFIER ASSIGN GETS'''
    print(f"User input stored in variable {p[1]}")

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

# Declaración de método con retorno
def p_method_with_return_declaration(p):
    '''statement : DEF IDENTIFIER LPAREN params RPAREN statement END'''
    print(f"Método con retorno declarado: {p[2]} con los parámetros {p[4]} y cuerpo {p[6]}")

# Llamada a métodos con retorno
def p_method_call_with_return(p):
    '''statement : IDENTIFIER LPAREN params RPAREN'''
    print(f"Llamada al método con retorno {p[1]} con los parámetros {p[3]}")

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

#Fin Pacheco
def test_parser(input_code):
    print("Parsing Ruby code:")
    print(input_code)
    try:
        parser.parse(input_code)
        return True
    except Exception as e:
        print("Error de sintaxis en la entrada.")
        return False

__all__ = ["parser", "test_parser"]
