#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 8/3/21 8:53 AM
# @Author  : Sahib Jan
# @Email   : jaanhunzai.512@gmail.com
# @File    : eventhandler.py
# @Software: PyCharm


"""Module defines the concept of inheritance


Examples:
    Class concept and inheritance using super-sub class
TODO:
    *
"""


class Person():
    """
        person class with instance variables
    """

    # function is called automatically every time
    # the class is being used to create a new object.
    def __init__(self, fname, lname, age):
        self.fname = fname
        self.lname = lname
        self.age = age


class Student(Person):
    """
        student class inherits person class with additional instance variables
    """

    def __init__(self, fname, lname, age, year, grade):
        self.year = year
        self.grade = grade
        # super() function that will make the child class inherit
        # all the methods and properties from its parent:
        super().__init__(fname, lname, age)

    def inf(self) -> str:
        """
            returns str
        """
        return self.fname, self.lname, self.age, self.year, self.grade


my_sub = Student("Jan", "khan", 42, 2021, "A")
print(my_sub.fname)
print(my_sub.inf())
