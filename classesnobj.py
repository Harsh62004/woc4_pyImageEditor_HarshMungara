class Person :
    def __init__(self,name,age):
        self.name=name
        self.age=age
        
    def walk(self):
        print(self.name + ' is walking...')
 
    def speak(self):
        print('Hello my name is ' + self.name + ' and I am ' + str(self.age) + ' years old' )


hazel = Person('Hazel' , 17)

hazel.speak()
hazel.walk()

print('---------------')

augustus = Person('Augustus', 18)
augustus.speak()
augustus.walk()