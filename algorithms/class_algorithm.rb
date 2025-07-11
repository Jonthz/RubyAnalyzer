
# Algoritmo de Clases Intermedio - Compatible con Parser Actual

class Calculator
  def initialize
    puts "Calculadora inicializada"
  end

  def add(a, b)
    return a + b
  end

  def multiply(x, y)
    result = x * y
    return result
  end

  def divide(num, den)
    if den == 0
      puts "Error: División por cero"
      return 0
    else
      return num / den
    end
  end


class Student
  def initialize(name)
    puts "Estudiante creado"
  end

  def study(hours)
    if hours > 5
      puts "Estudiando mucho"
    else
      puts "Estudiando poco"
    end
    return hours * 2
  end

  def grade(score)
    if score >= 90
      return "A"
    elsif score >= 80
      return "B" 
    else
      return "C"
    end
  end
end

# Crear instancias
calc = Calculator.new
student = Student.new("Juan")

# Usar métodos con diferentes argumentos
result1 = calc.add(10, 5)
result2 = calc.multiply(3, 4) 
result3 = calc.divide(20, 4)
result4 = calc.divide(10, 0)


# Usar métodos del estudiante
study_time = student.study(6)
final_grade = student.grade(85)

puts "Resultados calculados"
puts result1
puts result2
puts result3
