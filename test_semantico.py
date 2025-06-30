#!/usr/bin/env python3
"""
Archivo de prueba para el analizador semántico
"""

from AnalizadorSemantico import analizar_codigo, test_semantic_analyzer

def test_basic_operations():
    """Prueba operaciones básicas"""
    print("="*50)
    print("PRUEBA 1: Operaciones básicas")
    print("="*50)
    
    code = """
    x = 5
    y = 10
    suma = x + y
    resta = y - x
    """
    analizar_codigo(code)

def test_method_definition():
    """Prueba definición de métodos"""
    print("\n" + "="*50)
    print("PRUEBA 2: Definición de métodos")
    print("="*50)
    
    code = """
    def suma(a, b)
        resultado = a + b
        return resultado
    end
    """
    analizar_codigo(code)

def test_control_structures():
    """Prueba estructuras de control"""
    print("\n" + "="*50)
    print("PRUEBA 3: Estructuras de control")
    print("="*50)
    
    code = """
    x = 10
    if x > 5
        puts "Mayor a 5"
    else
        puts "Menor o igual a 5"
    end
    """
    analizar_codigo(code)

def test_errors():
    """Prueba detección de errores"""
    print("\n" + "="*50)
    print("PRUEBA 4: Detección de errores")
    print("="*50)
    
    code = """
    x = 5
    y = x + z
    break
    """
    analizar_codigo(code)

if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBAS DEL ANALIZADOR SEMÁNTICO")
    print("="*60)
    
    # Ejecutar todas las pruebas
    test_basic_operations()
    test_method_definition()
    test_control_structures()
    test_errors()
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
