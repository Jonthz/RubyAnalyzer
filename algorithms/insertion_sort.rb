# Algoritmo de Ordenamiento por Inserción Mejorado sin uso de arr[j+1] = arr[j]
def insertion_sort(arr)
  if arr.empty
   return arr
  end

  for i in 1..(arr.length)
    key = arr[i]
    j = i - 1

    # Buscar la posición correcta para insertar key
    while j >= 0 && arr[j] > key
      j -= 1
    end

    # Insertar y eliminar key para evitar desplazamientos manuales
    arr.insert(j + 1, key)
    if (j + 1 != i)
    arr.delete_at(i + 1)
    end 

  end
  return arr
end

def verificar_ordenamiento(arr)
  for i in 1..(arr.length)
    if arr[i - 1] > arr[i]
     return false 
    else
     return true
    end
  end
  return true
end

# Programa principal
numeros = [64, 34, 25, 12, 22, 11, 90, 5]
copia_numeros = numeros.dup
resultado = insertion_sort(copia_numeros)
es_correcto = verificar_ordenamiento(resultado)

puts "Array original:"
puts numeros.inspect
puts "Array ordenado:"
puts resultado.inspect
puts "Ordenamiento correcto: #{es_correcto}"