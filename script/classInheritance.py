class A:
    """
    - init instaciated when we create object
    """
    def __init__(self):
        print("init A")
    def feature1(self):
        print("print feature A-1")

    def feature2(self):
        print("print feature A-2")


class B(A):
    """
    - if init is not defined then it will get initA because class B inherit class A
    - if we defined init in B it will access it
    - if we want to access both inits in A and B "Super" key is used
    - we will get both init A and B using super
    - if we have muptiple inheritance for class then it super will pick the left inherited Class A
    """
    def __init__(self):
        super().__init__()
        print("init B")


    def feature3(self):
        print("print feature B-3")

    def feature4(self):


      print("print feature B-4")


class C:
    def __init__(self):

        print("init C")

    def feature6(self):
        print("featurre C-6")


class D (A,C):
    def __init__(self):
        super().__init__()
        print("init d")

    def info(self):
        # super is used to access methods from parent Classes
        super().feature1()


