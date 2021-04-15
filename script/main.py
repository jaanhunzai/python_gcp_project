from class_concepts import Student
from classInheritance import *
from polymorphismExample import *


if __name__ =="__main__":
    s1 = Student("abc", 2)
    s2 = Student("xyz", 8)
    s1.show()
    #print(s1.school)
    print("access class variable",Student.get_school())
    #call static method
    Student.info()

    #
    a1 = B()
    c1 = D()
    c1.info()

    """
    Polymorphisum: Means many forms 
    """

    #ide = PyCharm()
    # in this case it act like any defined ide
    # this is called duck typing
    ide = MyEditor()
    lap = Laptop()
    lap.code(ide)

    """
    - Operator Overloading 
        - if we want to + int with str then it will gives error
        - when you a+b then behind the scane it is calling int-__add__(a,b) 
        - we have diffent methods get call for 
        - 
    """
    a1 = Student1(50,60)
    a2 = Student1(500,600)

    s3 = a1+a2

    """
    - Method Overloading 
    """
    s3 = Student3(50,60)

    # now if we want to pass three arguments
    # in the mathod we have to add None with arguments
    print("here Overloading",s3.sum(50,60,70))


    """
    - Method Overriding  
    - when you call function if it dont not find in class it will looking into parent class
    - if it exist it calls method overriding 
    """
