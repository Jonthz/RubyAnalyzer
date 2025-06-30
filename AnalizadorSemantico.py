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
    print(f"❌ Error Semántico: {message}")

def add_semantic_warning(message):
    """Agregar una advertencia semántica"""
    semantic_warnings.append(message)
    print(f"⚠️  Advertencia Semántica: {message}")

def infer_type(expr):
    """
    Inferencia de tipo simple y directa
    MEJORADO con sistema de compatibilidad Ruby (Jonathan Zambrano)
    """
    # ===== DETECCIÓN DE CONVERSIONES JZ (tu contribución) =====
    if isinstance(expr, dict) and expr.get("tipo") == "llamada_metodo":
        method_name = expr.get("nombre")
        target_obj = expr.get("objeto")
        
        # Mapeo de métodos de conversión Ruby (Jonathan Zambrano)
        conversion_methods_jz = {
            "to_i": "integer",          # Convertir a entero
            "to_f": "float",            # Convertir a flotante  
            "to_s": "string",           # Convertir a string
            "to_a": "array",            # Convertir a array
            "to_h": "hash",             # Convertir a hash
            "to_sym": "symbol",         # Convertir a símbolo
            "chomp": "string",          # Quitar salto de línea
            "strip": "string",          # Quitar espacios
            "upcase": "string",         # Mayúsculas
            "downcase": "string",       # Minúsculas
            "round": "integer",         # Redondear
            "floor": "integer",         # Piso
            "ceil": "integer"           # Techo
        }
        
        if method_name in conversion_methods_jz:
            print(f"🔄 [JZ] Conversión detectada: {method_name} -> {conversion_methods_jz[method_name]}")
            return conversion_methods_jz[method_name]
    
    # ===== INFERENCIA ORIGINAL (mantener base) =====
    if isinstance(expr, int):
        return "integer"
    elif isinstance(expr, float):
        return "float"
    elif isinstance(expr, str):
        # ===== MEJORA JZ: Detectar strings numéricos =====
        if expr.replace('.', '', 1).replace('-', '', 1).isdigit():
            print(f"🔍 [JZ] String numérico detectado: '{expr}'")
            return "string_numeric"
        elif expr.isdigit():
            print(f"🔍 [JZ] String numérico entero detectado: '{expr}'")
            return "string_numeric"
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
                # ===== MEJORA JZ: Inferencia más específica según operandos =====
                left_type = infer_type(expr.get("izq"))
                right_type = infer_type(expr.get("der"))
                
                # Concatenación de strings (JZ)
                if op == "+" and (left_type == "string" or right_type == "string"):
                    return "string"
                
                # Operaciones numéricas (JZ mejorado)
                if left_type == "float" or right_type == "float":
                    return "float"
                elif op == "/":  # División siempre retorna float en Ruby
                    return "float"
                elif left_type == "string_numeric" and right_type == "string_numeric":
                    return "numeric"  # Mantener compatibilidad
                else:
                    return "numeric"  # Simplificado original
                    
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
        print(f"✅ Método '{name}' registrado con {len(params) if params else 0} parámetros")
        # También mantener compatibilidad con defined_methods
        if name not in defined_methods:
            defined_methods.append(name)
    else:
        print(f"✅ Variable '{name}' declarada como {symbol_type}")

def lookup_variable(name):
    """Buscar una variable en la tabla de símbolos"""
    return symbol_table.get(name, None)

def is_compatible_types(type1, type2):
    """
    Verificar si dos tipos son compatibles
    MEJORADO con sistema JZ (Jonathan Zambrano)
    """
    if type1 == type2:
        return True
    
    # ===== COMPATIBILIDAD ORIGINAL =====
    original_numeric = {"integer", "float", "numeric"}
    if {type1, type2}.issubset(original_numeric):
        return True
    
    # ===== MEJORAS JZ: Compatibilidad Ruby extendida =====
    
    # Compatibilidad numérica extendida (JZ)
    jz_numeric = {"integer", "float", "numeric", "string_numeric"}
    if {type1, type2}.issubset(jz_numeric):
        print(f"🔍 [JZ] Compatibilidad numérica extendida: {type1} ↔ {type2}")
        return True
    
    # Strings son compatibles entre sí (JZ)
    if type1 == "string" and type2 == "string":
        return True
    
    # String numérico con numéricos (JZ)
    if (type1 == "string_numeric" and type2 in original_numeric) or \
       (type2 == "string_numeric" and type1 in original_numeric):
        print(f"🔍 [JZ] Compatibilidad string numérico: {type1} ↔ {type2}")
        return True
    
    return False

# Validación de operaciones simplificada
def validar_operacion(op, izq, der):
    """
    Valida que dos operandos sean compatibles para la operación
    MEJORADO con sistema de compatibilidad Ruby (Jonathan Zambrano)
    """
    # Usar la función infer_type mejorada (que ya incluye detección JZ)
    left_type = infer_type(izq)
    right_type = infer_type(der)
    
    print(f"🔧 Validando operación: {left_type} {op} {right_type}")
    
    # ===== OPERACIONES ARITMÉTICAS =====
    if op in ["+", "-", "*", "/", "**", "%"]:
        
        # ===== MEJORA JZ: Concatenación inteligente =====
        if op == "+":
            if left_type == "string" or right_type == "string":
                if left_type == "string" and right_type == "string":
                    print(f"✅ [JZ] Concatenación de strings válida")
                    return "string"
                elif left_type == "string" and right_type in ["integer", "float"]:
                    add_semantic_warning(f"[JZ] Concatenación string + {right_type}: considere usar .to_s")
                    print(f"💡 [JZ] Sugerencia: Use {get_var_name_jz(der)}.to_s para convertir a string")
                    return "string"
                elif right_type == "string" and left_type in ["integer", "float"]:
                    add_semantic_warning(f"[JZ] Concatenación {left_type} + string: considere usar .to_s")
                    print(f"💡 [JZ] Sugerencia: Use {get_var_name_jz(izq)}.to_s para convertir a string")
                    return "string"
        
        # ===== VERIFICACIÓN DE COMPATIBILIDAD (original + JZ) =====
        if is_compatible_types(left_type, right_type):
            # ===== MEJORA JZ: Tipo resultante más específico =====
            if left_type == "float" or right_type == "float":
                result_type = "float"
            elif op == "/":  # División siempre retorna float en Ruby (JZ)
                result_type = "float"
            elif left_type == "string_numeric" and right_type == "string_numeric":
                add_semantic_warning(f"[JZ] Operación entre strings numéricos: considere conversión explícita")
                print(f"💡 [JZ] Sugerencia: Use .to.i o .to_f para convertir strings numéricos")
                result_type = "numeric"
            else:
                result_type = "numeric"  # Mantener original
            
            print(f"✅ Operación aritmética '{op}' válida entre '{left_type}' y '{right_type}' = {result_type}")
            return result_type
        else:
            # ===== MEJORA JZ: Sugerencias específicas para errores =====
            error_msg = f"Operación '{op}' entre tipos incompatibles: '{left_type}' y '{right_type}'"
            add_semantic_error(error_msg)
            
            # Sugerencias JZ según el tipo de error
            if left_type == "string" and right_type in ["integer", "float"]:
                print(f"💡 [JZ] Sugerencia: Use {get_var_name_jz(izq)}.to_i o .to_f para convertir el string")
            elif right_type == "string" and left_type in ["integer", "float"]:
                print(f"💡 [JZ] Sugerencia: Use {get_var_name_jz(der)}.to_i o .to_f para convertir el string")
            elif left_type == "string" and right_type == "string":
                if op == "+":
                    print(f"💡 [JZ] Nota: Concatenación de strings debería funcionar, verifique el contenido")
                else:
                    print(f"💡 [JZ] Sugerencia: Para operaciones numéricas con strings, use .to.i o .to.f")
            
            return "error"
    
    # ===== OPERACIONES DE COMPARACIÓN =====
    elif op in ["==", "!=", ">", "<", ">=", "<="]:
        
        # ===== MEJORA JZ: Comparaciones Ruby más permisivas =====
        if left_type == right_type:
            print(f"✅ [JZ] Comparación '{op}' válida entre tipos idénticos: {left_type}")
            return "boolean"
        
        # Comparaciones numéricas (JZ extendido)
        numeric_types = ["integer", "float", "numeric", "string_numeric"]
        if left_type in numeric_types and right_type in numeric_types:
            if left_type == "string_numeric" or right_type == "string_numeric":
                add_semantic_warning(f"[JZ] Comparación con string numérico: considere conversión explícita")
                print(f"💡 [JZ] Sugerencia: Use .to.i o .to_f para comparaciones más precisas")
            print(f"✅ [JZ] Comparación numérica '{op}' válida: {left_type} {op} {right_type}")
            return "boolean"
        
        # Compatibilidad original
        if is_compatible_types(left_type, right_type):
            print(f"✅ Comparación '{op}' válida entre '{left_type}' y '{right_type}'")
            return "boolean"
        else:
            # ===== MEJORA JZ: Comparaciones Ruby son más permisivas =====
            if op in ["==", "!="]:
                print(f"✅ [JZ] Comparación de igualdad '{op}' válida (Ruby permite cualquier tipo)")
                return "boolean"
            
            # Advertencia para comparaciones de orden (JZ)
            if op in [">", "<", ">=", "<="]:
                add_semantic_warning(f"[JZ] Comparación de orden '{op}' entre tipos diferentes: {left_type} y {right_type}")
                add_semantic_warning(f"[JZ] Esto puede lanzar una excepción en tiempo de ejecución")
            
            # Error menos severo (original mejorado)
            add_semantic_error(f"Comparación '{op}' entre tipos incompatibles: '{left_type}' y '{right_type}'")
            return "boolean"  # Ruby permite comparar cualquier cosa
    
    # ===== OPERACIONES LÓGICAS (original) =====
    elif op in ["&&", "||"]:
        print(f"✅ Operación lógica '{op}' válida")
        return "boolean"
    
    else:
        add_semantic_error(f"Operador '{op}' no reconocido")
        return "error"


def analizar_semantica(ast):
    """Función principal del análisis semántico - versión con debug"""
    print(f"🔍 DEBUG: Analizando AST: {ast}")
    print(f"🔍 DEBUG: Tipo de AST: {type(ast)}")
    
    if isinstance(ast, list):
        print(f"🔍 DEBUG: Lista con {len(ast)} elementos")
        for i, nodo in enumerate(ast):
            print(f"🔍 DEBUG: Elemento {i}: {nodo}")
            analizar_semantica(nodo)
    elif isinstance(ast, dict):
        tipo = ast.get("tipo")
        print(f"🔍 DEBUG: Diccionario con tipo: {tipo}")
        
        # Asignación de variable
        if tipo == "asignacion":
            var_name = ast.get("variable")
            valor = ast.get("valor")
            
            print(f"🔍 DEBUG: Procesando asignación - Variable: {var_name}, Valor: {valor}")
            
            # Analizar primero el valor
            analizar_semantica(valor)
            
            # Inferir tipo del valor
            value_type = infer_type(valor)
            print(f"🔍 DEBUG: Tipo inferido: {value_type}")
            
            # Actualizar tabla de símbolos
            declare_symbol(var_name, value_type, valor)
            print(f"🔍 DEBUG: Tabla de símbolos actualizada: {symbol_table}")
            
        # Uso de variable
        elif tipo == "uso_variable":
            var_name = ast.get("nombre")
            var_info = lookup_variable(var_name)
            if not var_info:
                add_semantic_error(f"Variable '{var_name}' usada sin ser declarada")
            else:
                print(f"✅ Uso válido de variable '{var_name}' (tipo: {var_info['type']})")
                
        # Uso de identificador (puede ser variable o método)
        elif tipo == "uso_identificador":
            var_name = ast.get("nombre")
            
            # Buscar en la tabla de símbolos
            symbol_info = lookup_variable(var_name)
            
            if symbol_info:
                if symbol_info.get('is_method', False):
                    print(f"✅ Llamada válida a método '{var_name}()' (sin argumentos)")
                else:
                    print(f"✅ Uso válido de variable '{var_name}' (tipo: {symbol_info['type']})")
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
            
        # Método
        elif tipo == "metodo":
            method_name = ast.get("nombre")
            params = ast.get("parametros", [])
            cuerpo = ast.get("cuerpo", [])
            
            print(f"🔧 Analizando definición de método: {method_name}")
            print(f"🔧 Parámetros encontrados: {params}")
            
            # REGISTRAR EL MÉTODO EN LA TABLA DE SÍMBOLOS (tu sugerencia)
            declare_symbol(method_name, "metodo", None, params, True)
            
            # CORREGIR: Analizar parámetros como variables locales del método
            for param in params:
                if isinstance(param, str):
                    declare_symbol(param, "parameter", None, None, False)
                    print(f"  📋 Parámetro '{param}' declarado como variable local")
                elif isinstance(param, dict) and param.get("tipo") == "uso_variable":
                    # Si los parámetros vienen como diccionarios de uso_variable
                    param_name = param.get("nombre")
                    if param_name:
                        declare_symbol(param_name, "parameter", None, None, False)
                        print(f"  📋 Parámetro '{param_name}' declarado como variable local")
            
            # Analizar cuerpo del método (aquí ya deberían estar disponibles los parámetros)
            if cuerpo:
                print(f"🔧 Analizando cuerpo del método {method_name}")
                analizar_semantica(cuerpo)
            
            print(f"✅ Método {method_name} completamente procesado")
            
        # Estructuras de control con bucles
        elif tipo in ["for", "while", "for_inline", "while_inline"]:
            print(f"🔄 Analizando estructura de control: {tipo}")
            
            # Entrar a contexto de bucle
            loop_stack.append(True)
            
            # Analizar condición si existe
            if "condicion" in ast:
                analizar_semantica(ast["condicion"])
                
            # Para bucles for, declarar variable de iteración
            if tipo.startswith("for") and "variable" in ast:
                var_iter = ast["variable"]
                declare_symbol(var_iter, "integer", 0)
                print(f"  🔢 Variable de iteración '{var_iter}' declarada")
            
            # Analizar cuerpo
            analizar_semantica(ast.get("cuerpo", []))
            
            # Salir del contexto de bucle
            loop_stack.pop()
            
        # Estructuras condicionales
        elif tipo in ["if", "if_else", "if_elsif", "if_elsif_else", "if_inline", "if_else_inline"]:
            print(f"🔀 Analizando estructura condicional: {tipo}")
            
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
                print("✅ Break válido dentro de un bucle")
                
        # Arrays, hashes, sets
        elif tipo in ["array", "hash", "set"]:
            print(f"📦 Analizando colección: {tipo}")
            # Analizar elementos si los hay
            if "elementos" in ast:
                analizar_semantica(ast["elementos"])
                
        # Llamada a método
        elif tipo == "llamada_metodo":
            method_name = ast.get("nombre")
            args = ast.get("argumentos", [])
            
            print(f"📞 Analizando llamada a método '{method_name}' con {len(args)} argumentos")
            
            # ===== MEJORA JZ: Métodos de conversión integrados =====
            conversion_methods_jz = ["to_i", "to_f", "to_s", "to_a", "to_h", "to_sym", "chomp", "strip", "upcase", "downcase", "round", "floor", "ceil"]
            
            if method_name in conversion_methods_jz:
                print(f"✅ [JZ] Método de conversión integrado '{method_name}' reconocido")
                # Los métodos de conversión no necesitan verificación de argumentos
            else:
                # ===== VERIFICACIÓN DE ARGUMENTOS JZ (tu contribución) =====
                print(f"🔍 [JZ] Verificando argumentos para método definido por usuario...")
                analyze_method_call_jz(method_name, args)
            
            # Analizar los argumentos (siempre necesario)
            for arg in args:
                analizar_semantica(arg)
                
        # Puts statement
        elif tipo == "puts":
            print(f"📄 Analizando puts")
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
    print("\n📋 TABLA DE SÍMBOLOS - VARIABLES:")
    if variables:
        for var_name, var_info in variables.items():
            status = "✅ Inicializada" if var_info['initialized'] else "⚠️  Sin inicializar"
            print(f"  • {var_name}: {var_info['type']} - {status}")
    else:
        print("  (Ninguna)")
    
    # Mostrar métodos
    print("\n🔧 TABLA DE SÍMBOLOS - MÉTODOS:")
    if methods:
        for method_name, method_info in methods.items():
            param_count = method_info['param_count']
            param_text = f"({param_count} parámetros)" if param_count > 0 else "(sin parámetros)"
            print(f"  • {method_name}: metodo {param_text}")
    else:
        print("  (Ninguno)")
    
    # Mostrar errores
    if semantic_errors:
        print(f"\n❌ ERRORES SEMÁNTICOS ENCONTRADOS ({len(semantic_errors)}):")
        for i, error in enumerate(semantic_errors, 1):
            print(f"  {i}. {error}")
    else:
        print("\n✅ NO SE ENCONTRARON ERRORES SEMÁNTICOS")
    
    # Mostrar advertencias
    if semantic_warnings:
        print(f"\n⚠️  ADVERTENCIAS SEMÁNTICAS ({len(semantic_warnings)}):")
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
        
        print(f"\n💾 Log guardado en: {log_filename}")
        
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
            print("❌ No se pudo analizar sintácticamente el código.")
            return
    except Exception as e:
        print(f"❌ Error en análisis sintáctico: {e}")
        return
    
    print("🔍 INICIANDO ANÁLISIS SEMÁNTICO...")
    print("-" * 40)
    
    try:
        # Realizar análisis semántico
        analizar_semantica(ast)
        
        # Generar reporte
        generar_reporte_semantico()
        
        # Guardar log
        log_semantic_analysis(codigo, semantic_errors, semantic_warnings)
        
        print("✅ Análisis semántico completado.")
        
    except Exception as e:
        add_semantic_error(f"Error interno durante análisis: {e}")
        print(f"❌ Error durante análisis semántico: {e}")

# Agregar después de la línea 659 en AnalizadorSemantico.py:

# ==========================================================================
# COMPROBACIÓN DE ARGUMENTOS EN MÉTODOS - Jonathan Zambrano
# ==========================================================================

def check_method_arguments_jz(method_name, provided_args, call_location="método"):
    """
    Verificar que los métodos sean llamados con la cantidad correcta de argumentos
    y que los tipos coincidan (Jonathan Zambrano)
    
    Args:
        method_name: Nombre del método a verificar
        provided_args: Lista de argumentos proporcionados
        call_location: Contexto de la llamada (para mensajes)
    
    Returns:
        dict: {"valid": bool, "errors": list, "warnings": list}
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    print(f"🔍 [JZ] Verificando argumentos para método '{method_name}'")
    print(f"🔍 [JZ] Argumentos proporcionados: {len(provided_args)} - {provided_args}")
    
    # Buscar el método en la tabla de símbolos
    method_info = lookup_variable(method_name)
    
    if not method_info:
        # Método no encontrado
        error_msg = f"[JZ] Método '{method_name}' no está definido"
        result["errors"].append(error_msg)
        result["valid"] = False
        add_semantic_error(error_msg)
        print(f"❌ [JZ] {error_msg}")
        return result
    
    if not method_info.get('is_method', False):
        # No es un método
        error_msg = f"[JZ] '{method_name}' no es un método"
        result["errors"].append(error_msg)
        result["valid"] = False
        add_semantic_error(error_msg)
        print(f"❌ [JZ] {error_msg}")
        return result
    
    # Obtener información del método
    expected_params = method_info.get('param_count', 0)
    actual_args = len(provided_args)
    method_params = method_info.get('params', [])
    
    print(f"📋 [JZ] Método '{method_name}' espera {expected_params} parámetros")
    print(f"📋 [JZ] Parámetros definidos: {method_params}")
    
    # ===== VERIFICACIÓN DE CANTIDAD DE ARGUMENTOS =====
    if expected_params != actual_args:
        error_msg = f"[JZ] Método '{method_name}' espera {expected_params} argumentos, pero recibió {actual_args}"
        result["errors"].append(error_msg)
        result["valid"] = False
        add_semantic_error(error_msg)
        print(f"❌ [JZ] {error_msg}")
        
        # Sugerencias específicas
        if actual_args < expected_params:
            missing = expected_params - actual_args
            print(f"💡 [JZ] Faltan {missing} argumento(s)")
            if method_params:
                missing_params = method_params[actual_args:]
                print(f"💡 [JZ] Parámetros faltantes: {missing_params}")
        else:
            excess = actual_args - expected_params
            print(f"💡 [JZ] Sobran {excess} argumento(s)")
        
        return result
    
    # ===== VERIFICACIÓN DE TIPOS DE ARGUMENTOS =====
    print(f"✅ [JZ] Cantidad de argumentos correcta ({actual_args})")
    
    # Analizar tipos de cada argumento
    for i, arg in enumerate(provided_args):
        arg_type = infer_type(arg)
        param_name = method_params[i] if i < len(method_params) else f"param_{i+1}"
        
        print(f"🔍 [JZ] Argumento {i+1} ({param_name}): tipo '{arg_type}'")
        
        # ===== VERIFICACIONES DE TIPO ESPECÍFICAS JZ =====
        
        # 1. Verificar argumentos no definidos
        if arg_type == "undefined":
            error_msg = f"[JZ] Argumento {i+1} para '{method_name}' usa variable no definida"
            result["errors"].append(error_msg)
            result["valid"] = False
            add_semantic_error(error_msg)
            print(f"❌ [JZ] {error_msg}")
        
        # 2. Verificar tipos problemáticos
        elif arg_type == "unknown":
            warning_msg = f"[JZ] Argumento {i+1} para '{method_name}' tiene tipo desconocido"
            result["warnings"].append(warning_msg)
            add_semantic_warning(warning_msg)
            print(f"⚠️ [JZ] {warning_msg}")
        
        # 3. Verificar strings numéricos (sugerir conversión)
        elif arg_type == "string_numeric":
            warning_msg = f"[JZ] Argumento {i+1} para '{method_name}' es string numérico: considere conversión explícita"
            result["warnings"].append(warning_msg)
            add_semantic_warning(warning_msg)
            print(f"⚠️ [JZ] {warning_msg}")
            print(f"💡 [JZ] Sugerencia: Use .to_i o .to_f si el método espera un número")
        
        # 4. Análisis de compatibilidad avanzada
        else:
            print(f"✅ [JZ] Argumento {i+1} ({param_name}): tipo '{arg_type}' válido")
    
    # ===== VERIFICACIONES ADICIONALES JZ =====
    
    # Verificar si hay mezcla de tipos incompatibles
    arg_types = [infer_type(arg) for arg in provided_args]
    unique_types = set(arg_types)
    
    if len(unique_types) > 1:
        # Hay mezcla de tipos - verificar compatibilidad
        problematic_combinations = []
        
        for i in range(len(arg_types)):
            for j in range(i+1, len(arg_types)):
                type1, type2 = arg_types[i], arg_types[j]
                if not is_compatible_types(type1, type2):
                    problematic_combinations.append((i+1, type1, j+1, type2))
        
        if problematic_combinations:
            warning_msg = f"[JZ] Método '{method_name}' recibe tipos incompatibles:"
            result["warnings"].append(warning_msg)
            add_semantic_warning(warning_msg)
            print(f"⚠️ [JZ] {warning_msg}")
            
            for arg1_pos, type1, arg2_pos, type2 in problematic_combinations:
                incompatible_msg = f"[JZ] Argumento {arg1_pos} ({type1}) incompatible con argumento {arg2_pos} ({type2})"
                print(f"  ⚠️ [JZ] {incompatible_msg}")
                
                # Sugerencias específicas
                suggest_argument_conversion_jz(arg1_pos, type1, type2)
                suggest_argument_conversion_jz(arg2_pos, type2, type1)
    
    if result["valid"]:
        success_msg = f"✅ [JZ] Llamada a método '{method_name}' válida: {actual_args} argumentos correctos"
        print(success_msg)
    
    return result

# Agregar función auxiliar después de check_method_arguments_jz:

def get_var_name_jz(expr):
    """
    Función auxiliar para obtener nombre de variable (Jonathan Zambrano)
    """
    if isinstance(expr, dict):
        if expr.get("tipo") == "uso_variable":
            return expr.get("nombre", "variable")
        elif expr.get("tipo") == "llamada_metodo":
            obj = expr.get("objeto")
            if isinstance(obj, dict) and obj.get("tipo") == "uso_variable":
                return obj.get("nombre", "variable")
            elif isinstance(obj, str):
                return obj
    elif isinstance(expr, str):
        return f"'{expr}'"
    elif isinstance(expr, (int, float)):
        return str(expr) 
    return "valor"

def suggest_argument_conversion_jz(arg_position, from_type, to_type):
    """
    Sugerir conversiones para argumentos incompatibles (Jonathan Zambrano)
    """
    conversion_suggestions = {
        ("string", "integer"): "Use .to_i para convertir string a entero",
        ("string", "float"): "Use .to_f para convertir string a decimal", 
        ("string", "numeric"): "Use .to_i o .to_f para convertir string a número",
        ("integer", "string"): "Use .to_s para convertir entero a string",
        ("float", "string"): "Use .to_s para convertir decimal a string",
        ("string_numeric", "integer"): "Use .to_i para convertir string numérico a entero",
        ("string_numeric", "float"): "Use .to_f para convertir string numérico a decimal"
    }
    
    suggestion = conversion_suggestions.get((from_type, to_type))
    if suggestion:
        print(f"💡 [JZ] Para argumento {arg_position}: {suggestion}")

def analyze_method_call_jz(method_name, arguments):
    """
    Analizar llamada a método completa (Jonathan Zambrano)
    Función principal que verifica argumentos y compatibilidad
    """
    print(f"\n🔍 [JZ] === ANÁLISIS DE LLAMADA A MÉTODO ===")
    print(f"🔍 [JZ] Método: {method_name}")
    print(f"🔍 [JZ] Argumentos: {arguments}")
    
    # Analizar cada argumento primero
    for i, arg in enumerate(arguments):
        print(f"🔍 [JZ] Analizando argumento {i+1}...")
        analizar_semantica(arg)
    
    # Verificar argumentos
    result = check_method_arguments_jz(method_name, arguments)
    
    print(f"🔍 [JZ] === FIN ANÁLISIS DE LLAMADA ===\n")
    
    return result