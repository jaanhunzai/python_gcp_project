#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 9/6/21 5:17 AM
# @Author  : Sahib Jan
# @Email   : jaanhunzai.512@gmail.com
# @File    : poly_method_overriding.py
# @Software: PyCharm

"""
- Polymorphism refers to the condition of occurance in different forms
- it refers to use of a single type entity (method, operator, object) to represent different scenarios
"""


"""
-  polymorphism in addition operator
- Single operator + has been used to carry out different operations for distinct data types.
"""
num1 = 1
num = 2

print(num1+num)


st1 = "this"
str2 = "that"
print(st1+str2)

#Function Polymorphism in Python
# the function len can run for many data types
print(len("this is what len finction in poly perirms"))
print(len(["this","that","you","we"]))
print(len({"a":"A","b":"B"}))

"""
- Polymorphism and Inheritance
- function override: method in childclss that have the same name as in method in parent class
- if method in parent class dont well fit for child class overriding use
"""

from math import pi

class Shape:

    def __int__(self, name):
        self.name = name

    def area(self):
        pass

    def fact(self):
        return "i am 2D"
    def __str__(self):
        return self.name


class Square(Shape):
    def __init__(self, length,name):
       super().__init__()
       self.name = name
       self.length = length
        
    def area(self):
        return self.length*2

    def fact(self):
        return "sides are equal in Square"

class Circle(Shape):
    def __init__(self, radious, name):
       super(Circle, self).__init__()
       self.radious = radious
       self.name = name
    def area(self):
        return pi*self.radious*2

seq = Square(4, "seq")
cir = Circle(7,"cir")

print(seq)
print(seq.fact(), seq.length)
print("________")
print(cir)
print(cir.name,cir.fact(), cir.area())