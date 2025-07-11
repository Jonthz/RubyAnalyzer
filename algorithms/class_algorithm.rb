class Animal
  def initialize(name)
    @name = name
  end

  def speak(var)
    puts var
    puts "El animal hace un sonido."
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
