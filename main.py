import sys
import os
from AnalizadorLexico import tokens, lex, test_lexical_analyzer
from AnalizadorSintactico import yacc, test_parser

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
    print("5. Salir")
    
    option = input("\nOpción: ")
    
    if option == "1":
        print("\nIngrese código Ruby (escriba 'FIN' en una línea para terminar):")
        lines = []
        while True:
            line = input()
            print(f"Entrada: {line}")  # Mostrar la línea ingresada
            if line == "FIN":
                print("Fin de entrada de código.")
                break
            lines.append(line)  # Añadir la línea al arreglo
            print(f"Procesando línea: {line}")  # Mostrar el procesamiento de la línea
            # Añadir las triples comillas al principio y final2
            #  del código
            ruby_code = "\n".join(lines) 
            print("\nCódigo Ruby ingresado:")
            # Ejecutar análisis según selección
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
