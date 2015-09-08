class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return 'Name: %s, Age: %d' %(self.name, self.age)

    def __lt__(self, other):
        return self.age < other.age