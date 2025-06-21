class Animal
  def initialize(name)
    @name = name
  end

  def speak
    raise "Método 'speak' debe ser implementado en la clase derivada"
  end

  def info
    "#{@name} es un animal."
  end
end

class Dog < Animal
  def initialize(name, breed)
    super(name)
    @breed = breed
  end

  def speak
    puts "#{@name}, el perro de raza #{@breed}, ladra."
  end

  def info
    "#{@name} es un perro de raza #{@breed}."
  end
end

class Cat < Animal
  def initialize(name)
    super(name)
  end

  def speak
    puts "#{@name}, el gato, maulla."
  end

  def info
    "#{@name} es un gato."
  end
end

# Métodos de orden superior (lambda y proc)
add = lambda { |a, b| a + b }
multiply = proc { |a, b| a * b }

# Crear instancias de las clases
dog = Dog.new("Rex", "Pastor Alemán")
cat = Cat.new("Whiskers")

# Control de flujo con excepciones y manejo de errores
begin
  dog.speak
  cat.speak

  puts "\nInformación del perro: #{dog.info}"
  puts "Información del gato: #{cat.info}"

  puts "\nResultado de la suma con lambda: #{add.call(5, 3)}"
  puts "Resultado de la multiplicación con proc: #{multiply.call(5, 3)}"

  raise "¡Algo salió mal!" if dog.nil?

rescue => e
  puts "Error: #{e.message}"
ensure
  puts "\nFin de la ejecución de Clases y Métodos Lambda."
end