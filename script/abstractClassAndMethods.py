"""
- if the method have only defination not declaration not defination is called abstract Methods
and if class have abstract methods are classed abstract class
- using abstract class we can not create object
- for making abstract we have to import abc abstractmethod
"""
from abc import ABC,abstractmethod

class Computer (ABC):
    @abstractmethod
    # this decrotor shows abstrct method
    def process (self):
        """
        if the method have only defination not declaration not defination is called abstract Methods

        """
        pass


class Laptop(Computer):
    # if you define method it will work
    def process(self):
        print("it is running ")

if __name__ =="__main__":
    comp = Computer()
    comp.process()

    lap = Laptop()
    lap.process()
