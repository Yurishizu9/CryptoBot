

# change instance attribute

class Person:

    def __init__(self):
        self.name = 'Matt'
        self.height_cm = 173 

    def grow(self):
        self.height_cm += 10

    def name_change(self):
        self.name = 'Martin'


p1 = Person()

print(p1.name)

p1.name_change()

print(p1.name)
