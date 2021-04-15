"""
Polymorphisum: Means many forms
- objects have multiple form
- There are four way of implementing polymorphisum
    - Duck typing
    - Operator Overloading
    - Method Overloading
    - Method Overriding
"""
class PyCharm:
    def execute(self):
        print("compile")
        print("run")

# if we have other ide and have same method we can just simple change it ide object and get execute the code
class MyEditor:
    def execute(self):
        print("spelling")
        print("code")
        print("compile")
        print("run")
# to execute this we need to create ide object of pycharm type and pass to code function in laptop class
class Laptop:

    def code(self,ide):
        ide.execute()


class Student1:
    def __init__(self,m1,m2):
        self.m1 =m1
        self.m2 = m2
    # we have to define own method that can add two studdent marks in Class and return s3 of class type
    def __add__(self,other):
        m1 = self.m1+other.m1
        m2 = self.m2 + other.m2
        s3 = Student1(m1,m2)
        return s3

"""
- Method overload 
    - if we have two method with same name but taking differnt argument 
"""
class Student3:
    def __init__(self,m1,m2):
        self.m1 = m2
        self.m2 = m2
    # BY adding None in argument so that we can pass less or more argument
    def sum (self,a = None,b=None,c=None):
        s3 = a+b+c
        return s3
"""
- Method Overriding 
"""