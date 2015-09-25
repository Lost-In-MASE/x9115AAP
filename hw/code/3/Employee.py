class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '[Name: %s, Age: %d]' %(self.name, self.age)

    def __lt__(self, other):
        return self.age < other.age
        
if __name__ == "__main__":
    employees = []
    employees.append(Employee("Parth", 2))
    employees.append(Employee("Aadi", 3))
    employees.append(Employee("Abhi", 1))
    print(sorted(employees))