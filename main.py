import sys
import os
from AnalizadorLexico import tokens, lex, test_lexical_analyzer

algortithms = {
    "2": '''def insertion_sort(arr)
  for i in 1..arr.length - 1
    key = arr[i]
    j = i - 1
    # Mueve los elementos de arr[0..i-1] que son mayores que key, una posición hacia adelante
    while j >= 0 && arr[j] > key
      arr[j + 1] = arr[j]
      j -= 1
    end
    arr[j + 1] = key
  end
  return arr
end

# Prueba de Ordenamiento por Inserción
arr = [12, 11, 13, 5, 6]
puts "Arreglo original: #{arr}"
sorted_arr = insertion_sort(arr)
puts "Arreglo ordenado: #{sorted_arr}"''',
    "3": '''def quick_sort(arr)
  return arr if arr.length <= 1
  
  pivot = arr.delete_at(arr.length / 2) # Elige el pivote
  left, right = arr.partition { |x| x < pivot }
  
  return *quick_sort(left), pivot, *quick_sort(right)
end

# Prueba de Ordenamiento Rápido
arr = [12, 11, 13, 5, 6]
puts "Arreglo original: #{arr}"
sorted_arr = quick_sort(arr)
puts''',
    "4": '''class Animal
  def initialize(name)
    @name = name
  end
  
  def speak
    puts "#{@name} hace un sonido."
  end
end

# Definición de clase derivada
class Dog < Animal
  def initialize(name, breed)
    super(name) # Llama al inicializador de la clase base
    @breed = breed
  end
  
  def speak
    puts "#{@name}, el perro de raza #{@breed}, ladra."
  end
end

# Crear un objeto de la clase derivada
dog = Dog.new("Rex", "Pastor Alemán")
dog.speak'''
}


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
        ruby_code = "'''\n" + "\n".join(lines) + "\n'''"
        test_lexical_analyzer(ruby_code)
    
    elif option in ["2", "3", "4"]:
        # Aquí se cargarían los algoritmos de prueba
        algorithms = {
            "2": algortithms["2"],
            "3": algortithms["3"],
            "4": algortithms["4"]
        } 
        print(f"\nAnalizando algoritmo de prueba {int(option) - 1}:")
        print("=" * 40)
        print(algorithms[option])
        print("=" * 40)
        
        test_lexical_analyzer(algorithms[option])
    
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