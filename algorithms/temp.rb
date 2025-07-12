# Manipulación y recorrido de arreglos con funciones básicas en Ruby
def sum(a, b)
  resultado = a + b
  return resultado
end

def verificar_numero(num)
  if num > 0
    return true
  end
  return false
end

def procesar_array(arr)
  total = 0
  for i in 0..(arr.length - 1)
    total = total + arr[i]
  end
  return total
end
