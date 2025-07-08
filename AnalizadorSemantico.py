from AnalizadorSintacticoCopy import parser
import time
import os

# Tabla de símbolos simple - diccionario con información de variables
symbol_table = {}

# Lista para almacenar errores semánticos
semantic_errors = []

# Lista para almacenar advertencias
semantic_warnings = []

# Pila para contexto de bucles (para validar break)
loop_stack = []

# Lista para tracking de métodos definidos
defined_methods = []

def add_semantic_error(message):
    """Agregar un error semántico a la lista"""
    semantic_errors.append(message)
    print(f" Error Semántico: {message}")

def add_semantic_warning(message):
    """Agregar una advertencia semántica"""
    semantic_warnings.append(message)
    print(f"  Advertencia Semántica: {message}")

#Parte Giovanni
def infer_type(expr):
    """Inferencia de tipo simple y directa"""
    if isinstance(expr, int):
        return "integer"
    elif isinstance(expr, float):
        return "float"
    elif isinstance(expr, str):
        return "string"
    elif isinstance(expr, bool):
        return "boolean"
    elif expr is None:
        return "nil"
    elif isinstance(expr, list):
        return "array"
    elif isinstance(expr, dict):
        # Si es una operación
        if expr.get("tipo") == "operacion":
            op = expr.get("op")
            if op in ["+", "-", "*", "/", "**", "%"]:
                return "numeric"  # Simplificado
            elif op in ["==", "!=", ">", "<", ">=", "<=", "&&", "||"]:
                return "boolean"
        # Si es una variable
        elif expr.get("tipo") == "uso_variable":
            var_name = expr.get("nombre")
            if var_name in symbol_table:
                return symbol_table[var_name]['type']
            else:
                add_semantic_error(f"Variable '{var_name}' no está definida")
                return "undefined"
        # Si es un array
        elif expr.get("tipo") == "array":
            return "array"
        # Si es un hash
        elif expr.get("tipo") == "hash":
            return "hash"
    return "unknown"
#Fin Parte Giovanni

def declare_symbol(name, symbol_type, value=None, params=None, is_method=False):
    """Declarar un símbolo (variable o método) en la tabla de símbolos"""
    # Los parámetros se consideran "inicializados" porque reciben valores
    is_initialized = value is not None or is_method or symbol_type == "parameter"
    
    symbol_table[name] = {
        'type': symbol_type,
        'value': value,
        'initialized': is_initialized,  # ← CAMBIO AQUÍ
        'is_method': is_method,
        'params': params if params else [],
        'param_count': len(params) if params else 0
    }
    
    if is_method:
        print(f" Método '{name}' registrado con {len(params) if params else 0} parámetros")
        # También mantener compatibilidad con defined_methods
        if name not in defined_methods:
            defined_methods.append(name)
    else:
        print(f" Variable '{name}' declarada como {symbol_type}")

def lookup_variable(name):
    """Buscar una variable en la tabla de símbolos"""
    return symbol_table.get(name, None)

def is_compatible_types(type1, type2):
    """Verificar si dos tipos son compatibles"""
    if type1 == type2:
        return True
    # Permitir compatibilidad entre números
    if {type1, type2}.issubset({"integer", "float", "numeric"}):
        return True
    return False

# Validación de operaciones simplificada
def validar_operacion(op, izq, der):
    """Valida que dos operandos sean compatibles para la operación"""
    left_type = infer_type(izq)
    right_type = infer_type(der)
    
    # Operaciones aritméticas
    if op in ["+", "-", "*", "/", "**", "%"]:
        if is_compatible_types(left_type, right_type):
            print(f" Operación aritmética '{op}' válida entre '{left_type}' y '{right_type}'")
            return "numeric"
        else:
            add_semantic_error(f"Operación '{op}' entre tipos incompatibles: '{left_type}' y '{right_type}'")
            return "error"
    
    # Operaciones de comparación
    elif op in ["==", "!=", ">", "<", ">=", "<="]:
        if is_compatible_types(left_type, right_type):
            print(f" Comparación '{op}' válida entre '{left_type}' y '{right_type}'")
            return "boolean"
        else:
            add_semantic_error(f"Comparación '{op}' entre tipos incompatibles: '{left_type}' y '{right_type}'")
            return "boolean"  # Ruby permite comparar cualquier cosa
    
    # Operaciones lógicas
    elif op in ["&&", "||"]:
        print(f" Operación lógica '{op}' válida")
        return "boolean"
    
    else:
        add_semantic_error(f"Operador '{op}' no reconocido")
        return "error"


def analizar_semantica(ast):
    """Función principal del análisis semántico - versión con debug"""
    print(f" DEBUG: Analizando AST: {ast}")
    print(f" DEBUG: Tipo de AST: {type(ast)}")
# Parte Giovanni    
    if isinstance(ast, list):
        print(f" DEBUG: Lista con {len(ast)} elementos")
        for i, nodo in enumerate(ast):
            print(f" DEBUG: Elemento {i}: {nodo}")
            analizar_semantica(nodo)
    elif isinstance(ast, dict):
        tipo = ast.get("tipo")
        print(f" DEBUG: Diccionario con tipo: {tipo}")
        
        # Asignación de variable
        if tipo == "asignacion":
            var_name = ast.get("variable")
            valor = ast.get("valor")
            
            print(f" DEBUG: Procesando asignación - Variable: {var_name}, Valor: {valor}")
            
            # Analizar primero el valor
            analizar_semantica(valor)
            
            # Inferir tipo del valor
            value_type = infer_type(valor)
            print(f" DEBUG: Tipo inferido: {value_type}")
            
            # Actualizar tabla de símbolos
            declare_symbol(var_name, value_type, valor)
            print(f" DEBUG: Tabla de símbolos actualizada: {symbol_table}")
            
        # Uso de variable
        elif tipo == "uso_variable":
            var_name = ast.get("nombre")
            var_info = lookup_variable(var_name)
            if not var_info:
                add_semantic_error(f"Variable '{var_name}' usada sin ser declarada")
            else:
                print(f" Uso válido de variable '{var_name}' (tipo: {var_info['type']})")
                
        # Uso de identificador (puede ser variable o método)
        elif tipo == "uso_identificador":
            var_name = ast.get("nombre")
            
            # Buscar en la tabla de símbolos
            symbol_info = lookup_variable(var_name)
            
            if symbol_info:
                if symbol_info.get('is_method', False):
                    print(f" Llamada válida a método '{var_name}()' (sin argumentos)")
                else:
                    print(f" Uso válido de variable '{var_name}' (tipo: {symbol_info['type']})")
            else:
                add_semantic_error(f"Identificador '{var_name}' no está definido")

        # Operación
        elif tipo == "operacion":
            # Analizar operandos primero
            if "izq" in ast:
                analizar_semantica(ast.get("izq"))
            if "der" in ast:
                analizar_semantica(ast.get("der"))
            # Validar la operación
            validar_operacion(ast.get("op"), ast.get("izq"), ast.get("der"))
# Fin Parte Giovanni           
        # Método
        elif tipo == "metodo":
            method_name = ast.get("nombre")
            params = ast.get("parametros", [])
            cuerpo = ast.get("cuerpo", [])
            
            print(f" Analizando definición de método: {method_name}")
            print(f" Parámetros encontrados: {params}")
            
            # REGISTRAR EL MÉTODO EN LA TABLA DE SÍMBOLOS (tu sugerencia)
            declare_symbol(method_name, "metodo", None, params, True)
            
            # CORREGIR: Analizar parámetros como variables locales del método
            for param in params:
                if isinstance(param, str):
                    declare_symbol(param, "parameter", None, None, False)
                    print(f"   Parámetro '{param}' declarado como variable local")
                elif isinstance(param, dict) and param.get("tipo") == "uso_variable":
                    # Si los parámetros vienen como diccionarios de uso_variable
                    param_name = param.get("nombre")
                    if param_name:
                        declare_symbol(param_name, "parameter", None, None, False)
                        print(f"   Parámetro '{param_name}' declarado como variable local")
            
            # Analizar cuerpo del método (aquí ya deberían estar disponibles los parámetros)
            if cuerpo:
                print(f" Analizando cuerpo del método {method_name}")
                analizar_semantica(cuerpo)
            
            print(f" Método {method_name} completamente procesado")
            
        # Estructuras de control con bucles
        elif tipo in ["for", "while", "for_inline", "while_inline"]:
            print(f"Analizando estructura de control: {tipo}")
            
            # Entrar a contexto de bucle
            loop_stack.append(True)
            
            # Analizar condición si existe
            if "condicion" in ast:
                analizar_semantica(ast["condicion"])
                
            # Para bucles for, declarar variable de iteración
            if tipo.startswith("for") and "variable" in ast:
                var_iter = ast["variable"]
                declare_symbol(var_iter, "integer", 0)
                print(f"   Variable de iteración '{var_iter}' declarada")
            
            # Analizar cuerpo
            analizar_semantica(ast.get("cuerpo", []))
            
            # Salir del contexto de bucle
            loop_stack.pop()
            
        # Estructuras condicionales
        elif tipo in ["if", "if_else", "if_elsif", "if_elsif_else", "if_inline", "if_else_inline"]:
            print(f" Analizando estructura condicional: {tipo}")
            
            # Analizar condición
            if "condicion" in ast:
                analizar_semantica(ast["condicion"])
                
            # Analizar cuerpos
            if "cuerpo_if" in ast:
                analizar_semantica(ast["cuerpo_if"])
            elif "cuerpo" in ast:
                analizar_semantica(ast["cuerpo"])
                
            if "cuerpo_else" in ast:
                analizar_semantica(ast["cuerpo_else"])
                
            if "cuerpo_elsif" in ast:
                analizar_semantica(ast["cuerpo_elsif"])
                
        # Break statement
        elif tipo == "break":
            if not loop_stack:
                add_semantic_error("'break' fuera de un bucle")
            else:
                print(" Break válido dentro de un bucle")
                
        # Arrays, hashes, sets
        elif tipo in ["array", "hash", "set"]:
            print(f" Analizando colección: {tipo}")
            # Analizar elementos si los hay
            if "elementos" in ast:
                analizar_semantica(ast["elementos"])
                
        # Llamada a método
        elif tipo == "llamada_metodo":
            method_name = ast.get("nombre")
            args = ast.get("argumentos", [])
            
            print(f" Analizando llamada a método '{method_name}' con {len(args)} argumentos")
            
            # Buscar el método en la tabla de símbolos
            method_info = lookup_variable(method_name)
            
            if method_info and method_info.get('is_method', False):
                expected_params = method_info['param_count']
                actual_args = len(args)
                
                if expected_params == actual_args:
                    print(f" Llamada válida: método '{method_name}' espera {expected_params} argumentos y recibió {actual_args}")
                else:
                    add_semantic_error(f"Método '{method_name}' espera {expected_params} parámetros, pero recibió {actual_args}")
            else:
                add_semantic_warning(f"Método '{method_name}' no está definido o no es un método")
            
            # Analizar los argumentos
            for arg in args:
                analizar_semantica(arg)
                
        # Puts statement
        elif tipo == "puts":
            print(f" Analizando puts")
            # Analizar el valor que se va a imprimir
            if "valor" in ast:
                analizar_semantica(ast["valor"])
                
        else:
            # Analiza recursivamente cualquier otro diccionario
            for key, value in ast.items():
                if key != "tipo":  # Evitar recursión infinita
                    analizar_semantica(value)

def generar_reporte_semantico():
    """Generar un reporte completo del análisis semántico"""
    print("\n" + "="*50)
    print("    REPORTE DE ANÁLISIS SEMÁNTICO")
    print("="*50)
    
    # Separar variables y métodos
    variables = {}
    methods = {}
    
    for name, info in symbol_table.items():
        if info.get('is_method', False):
            methods[name] = info
        else:
            variables[name] = info
    
    # Mostrar variables
    print("\n TABLA DE SÍMBOLOS - VARIABLES:")
    if variables:
        for var_name, var_info in variables.items():
            status = " Inicializada" if var_info['initialized'] else "  Sin inicializar"
            print(f"  • {var_name}: {var_info['type']} - {status}")
    else:
        print("  (Ninguna)")
    
    # Mostrar métodos
    print("\n TABLA DE SÍMBOLOS - MÉTODOS:")
    if methods:
        for method_name, method_info in methods.items():
            param_count = method_info['param_count']
            param_text = f"({param_count} parámetros)" if param_count > 0 else "(sin parámetros)"
            print(f"  • {method_name}: metodo {param_text}")
    else:
        print("  (Ninguno)")
    
    # Mostrar errores
    if semantic_errors:
        print(f"\n ERRORES SEMÁNTICOS ENCONTRADOS ({len(semantic_errors)}):")
        for i, error in enumerate(semantic_errors, 1):
            print(f"  {i}. {error}")
    else:
        print("\n NO SE ENCONTRARON ERRORES SEMÁNTICOS")
    
    # Mostrar advertencias
    if semantic_warnings:
        print(f"\n  ADVERTENCIAS SEMÁNTICAS ({len(semantic_warnings)}):")
        for i, warning in enumerate(semantic_warnings, 1):
            print(f"  {i}. {warning}")
    
    print("\n" + "="*50)

def log_semantic_analysis(codigo, errores, warnings):
    """Registrar el análisis semántico en logs de forma simple"""
    try:
        # Obtener información del usuario
        import subprocess
        try:
            username = subprocess.check_output(["git", "config", "--get", "user.name"]).decode('utf-8').strip()
        except:
            username = "usuarioGit"
        
        timestamp = time.strftime("%d%m%Y-%Hh%M")
        log_dir = 'logs'
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_filename = f"{log_dir}/semantico-{username}-{timestamp}.txt"
        
        with open(log_filename, 'w', encoding='utf-8') as log_file:
            log_file.write("ANÁLISIS SEMÁNTICO - REPORTE\n")
            log_file.write("="*40 + "\n\n")
            log_file.write(f"Fecha: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            log_file.write(f"Usuario: {username}\n\n")
            
            log_file.write("CÓDIGO ANALIZADO:\n")
            log_file.write("-" * 20 + "\n")
            log_file.write(codigo + "\n\n")
            
            log_file.write("TABLA DE SÍMBOLOS:\n")
            log_file.write("-" * 20 + "\n")
            if symbol_table:
                for var_name, var_info in symbol_table.items():
                    status = "Inicializada" if var_info['initialized'] else "Sin inicializar"
                    log_file.write(f"  {var_name}: {var_info['type']} ({status})\n")
            else:
                log_file.write("  (Vacía)\n")
            
            if defined_methods:
                log_file.write(f"\nMÉTODOS DEFINIDOS:\n")
                log_file.write("-" * 20 + "\n")
                for method in defined_methods:
                    log_file.write(f"  {method}\n")
            
            if errores:
                log_file.write(f"\nERRORES ENCONTRADOS ({len(errores)}):\n")
                log_file.write("-" * 20 + "\n")
                for i, error in enumerate(errores, 1):
                    log_file.write(f"{i}. {error}\n")
            
            if warnings:
                log_file.write(f"\nADVERTENCIAS ({len(warnings)}):\n")
                log_file.write("-" * 20 + "\n")
                for i, warning in enumerate(warnings, 1):
                    log_file.write(f"{i}. {warning}\n")
            
            if not errores and not warnings:
                log_file.write("\nNO SE ENCONTRARON ERRORES NI ADVERTENCIAS\n")
        
        print(f"\n Log guardado en: {log_filename}")
        
    except Exception as e:
        print(f"Error al guardar log: {e}")

def analizar_codigo(codigo):
    """Función principal para analizar código - versión simplificada"""
    global semantic_errors, semantic_warnings, symbol_table, defined_methods
    
    # Reiniciar estado
    semantic_errors = []
    semantic_warnings = []
    symbol_table = {}  # Tabla simple
    defined_methods = []
    
    # Obtener AST del parser sintáctico
    try:
        ast = parser.parse(codigo)
        if ast is None:
            print(" No se pudo analizar sintácticamente el código.")
            return
    except Exception as e:
        print(f" Error en análisis sintáctico: {e}")
        return
    
    print(" INICIANDO ANÁLISIS SEMÁNTICO...")
    print("-" * 40)
    
    try:
        # Realizar análisis semántico
        analizar_semantica(ast)
        
        # Generar reporte
        generar_reporte_semantico()
        
        # Guardar log
        log_semantic_analysis(codigo, semantic_errors, semantic_warnings)
        
        print(" Análisis semántico completado.")
        
    except Exception as e:
        add_semantic_error(f"Error interno durante análisis: {e}")
        print(f" Error durante análisis semántico: {e}")

# Función de utilidad para testing
def test_semantic_analyzer():
    """Función de prueba simple para el analizador semántico"""
    test_code = """
    x = 5
    y = 10
    suma = x + y
    puts suma
    """
    
    print(" PROBANDO ANALIZADOR SEMÁNTICO SIMPLE")
    analizar_codigo(test_code)

def test_assignment_debug():
    """Función de prueba específica para asignaciones"""
    test_code = "x = 5"
    
    print(" PROBANDO ASIGNACIÓN SIMPLE")
    print(f"Código: {test_code}")
    
    # Obtener AST directamente del parser
    ast = parser.parse(test_code)
    print(f"AST obtenido: {ast}")
    
    # Analizar manualmente
    if ast:
        print(" Analizando AST manualmente...")
        analizar_semantica(ast)
        print(f" Tabla de símbolos final: {symbol_table}")
    else:
        print(" AST es None")

# ← AGREGAR ESTA LÍNEA AL FINAL:
if __name__ == "__main__":
    print(" EJECUTANDO PRUEBA DE DEBUG")
    test_assignment_debug()