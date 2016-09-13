# class and obj
class Person:
    population = 0

    def __init__(self, name):
        self.name = name
        print(self.name)
        Person.population += 1

    def __del__(self):
        print(self.name)
        Person.population -= 1
        if Person.population == 0:
            print('I am the last one')
        else:
            print('there are %d people left.' % (Person.population))

    def sayHi(self):
        print('His name is', self.name)

    def howMany(self):
        if Person.population == 1:
            print('I am the only person')
        else:
            print('we have  %d person here.' % (Person.population))


chenda = Person('chenda')
chenda.sayHi()
chenda.howMany()
