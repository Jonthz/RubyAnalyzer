import sys
import os
from AnalizadorLexico import tokens, lex, test_lexical_analyzer

# Cambia la manera en que cargas los algoritmos desde archivos
def load_algorithm_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()  # Lee todo el contenido del archivo
    except FileNotFoundError:
        print(f"Error: El archivo {file_name} no se encuentra.")
        return None

def main():
    """Función principal que maneja la interfaz con el usuario"""
    print("=== ANALIZADOR LÉXICO RUBY ===")
    print("Seleccione una opción:")
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
            if line == "FIN":
                break
            lines.append(line)
        # Añadir las triples comillas al principio y final del código
        ruby_code = "\n".join(lines) 
        test_lexical_analyzer(ruby_code)
    
    elif option == "2":
        algorithm_code = load_algorithm_from_file('algorithms/insertion_sort.rb')
        if algorithm_code:
            print(f"\nAnalizando algoritmo de prueba Insertion Sort:")
            print("=" * 40)
            print(algorithm_code)
            print("=" * 40)
            test_lexical_analyzer(algorithm_code)
    
    elif option == "3":
        algorithm_code = load_algorithm_from_file('algorithms/quick_sort.rb')
        if algorithm_code:
            print(f"\nAnalizando algoritmo de prueba Quick Sort:")
            print("=" * 40)
            print(algorithm_code)
            print("=" * 40)
            test_lexical_analyzer(algorithm_code)
    
    elif option == "4":
        algorithm_code = load_algorithm_from_file('algorithms/class_algorithm.rb')
        if algorithm_code:
            print(f"\nAnalizando algoritmo de prueba Class:")
            print("=" * 40)
            print(algorithm_code)
            print("=" * 40)
            test_lexical_analyzer(algorithm_code)
    
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
