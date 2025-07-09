# Algoritmo de Ordenamiento por Inserción Mejorado
def insertion_sort(arr)
  # Verificar si el parámetro es un arreglo

  for i in 1..arr.length - 1
    key = arr[i]
    j = i - 1

  # Mover los elementos de arr[0..i-1] que son mayores que key, una posición hacia adelante
    while j >= 0 && arr[j] > key
      arr[j + 1] = arr[j]
      j -= 1
    end
    arr[j + 1] = key
  end
  return arr
end
