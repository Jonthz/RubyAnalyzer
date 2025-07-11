# REEMPLAZAR el contenido de class_algorithm.rb con este código de prueba:

class Calculator
  def initialize(name)
    @name = name
  end

  def add_numbers(x, y)
    puts "Sumando números"
    result = x + y
    puts result
    return result
  end

  def info()
    puts @name
  end
end

class Cat < Animal
  def initialize(name)
    @name = name
  end
  
  def speak
    puts "#{@name} says: Meow!"
  end

end

cat = Cat.new("Whiskers")
animal = Animal.new("Generic Animal")

animal.speak("hola", 2, 3, "hola")
animal.info
cat.speak()
