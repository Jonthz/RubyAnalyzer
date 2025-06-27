import sys
import os
from AnalizadorLexico import tokens, lex, test_lexical_analyzer
from AnalizadorSintacticoCopy import yacc, test_parser

# Cambia la manera en que cargas los algoritmos desde archivos
def load_algorithm_from_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()  # Lee todo el contenido del archivo
    except FileNotFoundError:
        print(f"Error: El archivo {file_name} no se encuentra.")
        return None

def main():
    """Función principal que maneja la interfaz con el usuario"""
    print("=== SISTEMA DE ANÁLISIS DE CÓDIGO RUBY ===")
    print("Seleccione el tipo de análisis:")
    print("1. Análisis Léxico")
    print("2. Análisis Sintáctico")
    print("3. Salir")

    tipo = input("\nOpción: ")

    if tipo == "3":
        print("¡Hasta luego!")
        sys.exit(0)
    elif tipo not in ("1", "2"):
        print("Opción inválida. Intente de nuevo.")
        return main()

    print("\nSeleccione una opción:")
    print("1. Ingresar código Ruby manualmente")
    print("2. Usar algoritmo de prueba Insertion Sort")
    print("3. Usar algoritmo de prueba Quick Sort")
    print("4. Usar algoritmo de prueba Class")
    print("5. Usar algoritmo de prueba temp")
    print("6. Salir")

    option = input("\nOpción: ")

    if option == "1":
        print("\nIngrese código Ruby (escriba 'FIN' en una línea para terminar):")
        
        # Crear una lista para almacenar las líneas del código
        lines = []
        
        while True:
            # Leer la entrada del usuario
            line = input()
            
            # Salir del bucle si se ingresa 'FIN'
            if line == "FIN":
                break
            
            # Agregar la línea a la lista de líneas
            lines.append(line)
        
        # Unir todas las líneas en un solo bloque de código
        ruby_code = "\n".join(lines)
        
        # Verificar si el código está vacío después de ingresar 'FIN'
        if ruby_code.strip() == "":  # Si ruby_code está vacío (sin código), no hacer análisis
            print("No se ingresó código Ruby. Análisis cancelado.")
        else:
            print("\nCódigo Ruby ingresado:")
            print(ruby_code)
            
            # Ejecutar análisis según la selección
            if tipo == "1":
                test_lexical_analyzer(ruby_code)
            else:
                test_parser(ruby_code)


    elif option == "2":
        algorithm_code = load_algorithm_from_file('algorithms/insertion_sort.rb')
        if algorithm_code:
            print(f"\nAnalizando algoritmo de prueba Insertion Sort:")
            print("=" * 40)
            print(algorithm_code)
            print("=" * 40)

            # Ejecutar análisis según selección
            if tipo == "1":
                test_lexical_analyzer(algorithm_code)
            else:
                test_parser(algorithm_code)
    
    elif option == "3":
        algorithm_code = load_algorithm_from_file('algorithms/quick_sort.rb')
        if algorithm_code:
            print(f"\nAnalizando algoritmo de prueba Quick Sort:")
            print("=" * 40)
            print(algorithm_code)
            print("=" * 40)

            # Ejecutar análisis según selección
            if tipo == "1":
                test_lexical_analyzer(algorithm_code)
            else:
                test_parser(algorithm_code)
    
    elif option == "4":
        algorithm_code = load_algorithm_from_file('algorithms/class_algorithm.rb')
        if algorithm_code:
            print(f"\nAnalizando algoritmo de prueba Class:")
            print("=" * 40)
            print(algorithm_code)
            print("=" * 40)

            # Ejecutar análisis según selección
            if tipo == "1":
                test_lexical_analyzer(algorithm_code)
            else:
                test_parser(algorithm_code)
    
    elif option == "5":
        algorithm_code = load_algorithm_from_file('algorithms/temp.rb')
        if algorithm_code:
            print(f"\nAnalizando algoritmo de prueba temp:")
            print("=" * 40)
            print(algorithm_code)
            print("=" * 40)

            # Ejecutar análisis según selección
            if tipo == "1":
                test_lexical_analyzer(algorithm_code)
            else:
                test_parser(algorithm_code)
    
    elif option == "6":
        print("¡Hasta luego!")
        sys.exit(0)
    
    else:
        print("Opción no válida. Intente de nuevo.")
    
    # Preguntar si desea continuar
    continue_option = input("\n¿Desea realizar otro análisis? (s/n): ")
    if continue_option.lower() == 's':
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar pantalla
        main()  # Recursividad para volver al menú principal

if __name__ == "__main__":
    main()
