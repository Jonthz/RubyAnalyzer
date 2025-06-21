# Algoritmo de Ordenamiento Rápido Mejorado
def quick_sort(arr)
  # Verificar si el parámetro es un arreglo
  raise 'El parámetro debe ser un arreglo' unless arr.is_a?(Array)
  raise 'El arreglo no puede estar vacío' if arr.empty?

  return arr if arr.length <= 1

  pivot = arr.delete_at(arr.length / 2)  # Elige el pivote
  left, right = arr.partition { |x| x < pivot }

  # Llamadas recursivas y uso del operador de splat para devolver el resultado
  return *quick_sort(left), pivot, *quick_sort(right)
rescue => e
  puts "Error: #{e.message}"
  return []
end

# Función para imprimir el arreglo de manera visual
def print_array(arr)
  puts "Arreglo: [#{arr.join(", ")}]"
end

# Prueba de Quick Sort con múltiples escenarios
begin
  arr1 = [12, 11, 13, 5, 6]
  puts "Arreglo original: #{arr1}"
  sorted_arr1 = quick_sort(arr1)
  puts "Arreglo ordenado: #{sorted_arr1}"

  # Caso con arreglo vacío
  arr2 = []
  puts "\nArreglo vacío:"
  sorted_arr2 = quick_sort(arr2)
  print_array(sorted_arr2)

  # Caso con un solo elemento
  arr3 = [8]
  puts "\nArreglo con un solo elemento:"
  sorted_arr3 = quick_sort(arr3)
  print_array(sorted_arr3)
  
  # Caso con números negativos
  arr4 = [-5, -9, -1, -4, -7]
  puts "\nArreglo con números negativos:"
  sorted_arr4 = quick_sort(arr4)
  print_array(sorted_arr4)

  # Caso con mezcla de números positivos y negativos
  arr5 = [15, -2, 9, -8, 6, 7]
  puts "\nArreglo mixto (positivos y negativos):"
  sorted_arr5 = quick_sort(arr5)
  print_array(sorted_arr5)
rescue => e
  puts "Excepción capturada: #{e.message}"
ensure
  puts "\nFin de la ejecución de Quick Sort."
end