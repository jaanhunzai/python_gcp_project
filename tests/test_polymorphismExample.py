import unittest
from script.polymorphismExample import Student3

class test_polymorphismExample(unittest.TestCase):

    def setUp(self) -> None:
        print("**********setup******")
    def tearDown(self) -> None:
        print("********teardown********")


    def test_sum(self):
        num = Student3.sum(self,10,5)
        self.assertEqual(num,15)


    def test_mult(self):
        mul = Student3.mult(self,10,5)
        self.assertEqual(mul,50)


    def test_sub(self):
        sub = Student3.sub(self, 10,5)
        self.assertEqual(sub,5)


if __name__ == "__main__":
    unittest.main()