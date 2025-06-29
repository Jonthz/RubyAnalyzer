from AnalizadorSintacticoCopy import parser

def infer_type(expr):
    # Inferencia simple de tipo, debes adaptar según tu AST real
    if isinstance(expr, int):
        return "int"
    elif isinstance(expr, float):
        return "float"
    elif isinstance(expr, str):
        return "string"
    elif isinstance(expr, dict):
        # Si es una operación aritmética
        if expr.get("tipo") == "operacion":
            left = infer_type(expr.get("izq"))
            right = infer_type(expr.get("der"))
            if left == right:
                return left
            else:
                return "unknown"
        # Si es un return anidado
        if expr.get("tipo") == "return":
            return infer_type(expr.get("valor"))
        # Si es una variable, deberías consultar la tabla de símbolos (no implementado aquí)
    return "unknown"

# Pila para contexto de bucles
loop_stack = []

def analizar_semantica(ast):
    if isinstance(ast, list):
        for nodo in ast:
            analizar_semantica(nodo)
    elif isinstance(ast, dict):
        tipo = ast.get("tipo")
        if tipo == "metodo":
            print(f"Analizando método '{ast['nombre']}'")
            # Si el método tiene un valor de retorno explícito
            if "retorno" in ast:
                tipo_retorno = infer_type(ast["retorno"])
                # Aquí podrías agregar lógica para obtener el tipo esperado si lo declaras
                print(f"  Tipo inferido de retorno: {tipo_retorno}")
                # Ejemplo: si quieres que todos los métodos retornen int, puedes comparar aquí
                # if tipo_retorno != "int":
                #     print(f"Error: El método '{ast['nombre']}' retorna '{tipo_retorno}' pero se esperaba 'int'")
            # Analiza el cuerpo del método
            analizar_semantica(ast.get("cuerpo", []))
        elif tipo == "for" or tipo == "while":
            loop_stack.append(True)
            analizar_semantica(ast.get("cuerpo", []))
            loop_stack.pop()
        elif tipo == "if" or tipo == "if_else" or tipo == "if_elsif" or tipo == "if_elsif_else":
            # Analiza los cuerpos de las ramas del if
            analizar_semantica(ast.get("cuerpo_if", []))
            if "cuerpo_else" in ast:
                analizar_semantica(ast.get("cuerpo_else", []))
            if "cuerpo_elsif" in ast:
                analizar_semantica(ast.get("cuerpo_elsif", []))
        elif tipo == "break":
            if not loop_stack:
                print("Error semántico: 'break' fuera de un bucle")
        else:
            # Analiza recursivamente cualquier otro diccionario
            for v in ast.values():
                analizar_semantica(v)

def analizar_codigo(codigo):
    # Obtén el AST usando el parser
    ast = parser.parse(codigo, start='program')
    if ast is None:
        print("No se pudo analizar sintácticamente el código.")
        return
    print("=== Análisis Semántico ===")
    analizar_semantica(ast)
    print("=== Fin del Análisis Semántico ===")

