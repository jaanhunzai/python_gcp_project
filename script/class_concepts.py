class Student:
    """
    - class variable, this can be access using objects
    - as well as Student class
    """
    school = "AKU"

    def __init__(self, name, rollno):
        """
        - init function is automatically triggered when object is created
        - it takes self "the object" and other arguments
        - used to initialize the paramaters
        - the sub class can be access using self
        :param name:
        :param rollno:
        """
        self.name = name
        self.rollno = rollno
        self.lap = self.Laptop()

    # the decorator is used to explicity mention what type of method this is
    @classmethod
    def get_school(cls):
        """
        - there are three type of methods
            - classMethods : used to access class variables
            - instanceMethods: used to access and change instance variables
            - staticMethods: used to access and change other type of info
        - this is a class type method
        - use to access class variables such as school

        """
        return cls.school

    @staticmethod
    def info():
        """
            - this is statics method
            - not for instance varaible or class variables

        """
        print("this is statics methods")


    def show(self):
        """
        - the show method of laptop class can be access through object lap
        :return:
        """
        print(self.name, self.rollno)
        self.lap.show()

    class Laptop:
        def __init__(self):
            self.brand = "HP"
            self.cpu = "i5"
            self.ram = 8

        def show(self):
            print(self.brand, self.cpu, self.ram)




