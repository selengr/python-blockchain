class Animal():
    def __init__(self, name, species, age, sound):
        self.name = name
        self.species = species
        self.age = age
        self.sound = sound
        
        
    def make_sound(self):
        return f"im a lion {self.sound}"
    
    def zoo_name(self): 
        return "welcome to kerman zoo live"

    def info(self): 
        if(self.name == "lion"):
            return f"i am the strongest animal of all the world that set iam a {self.name}"
    
    def __str__(self):
        return f"you know who is the strongest animal of all the world meeeeee"
    
    
animal = Animal("lion", "german", 5, "bark bark")
print(animal)
print(animal.name)
print(animal.sound)

# print(animal.make_sound())
# print(animal.zoo_name())
print(animal.info())