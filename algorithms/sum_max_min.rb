def suma_mayores(arr, limite)
  suma = 0
  for i in 0..(arr.length - 1)
    if arr[i] > limite
      suma = suma + arr[i]
    end
  end
  return suma
end

def suma_menores(arr, limite)
  suma = 0
  for i in 0..(arr.length - 1)
    if arr[i] < limite
      suma = suma + arr[i]
    end 
  end
  return suma
end

numeros = [1, 5, 10, 15, 20, 25, 30, 2, 8, 50]
limite = 10
resultado1 = suma_mayores(numeros, limite)
resultado2 = suma_menores(numeros, limite)

puts "Suma de los mayores:"
puts resultado1
puts "Suma de los menores:" 
puts resultado2