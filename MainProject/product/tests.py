from django.test import TestCase
from .calculator import Calculator


# Create your tests here.
class CalculatorTest(TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.add(2, 3), 5)
        self.assertEqual(self.calculator.add(4, 6), 10)
        self.assertEqual(self.calculator.add(5, 0), 5)
        self.assertEqual(self.calculator.add(7, 1), 8)

    def test_isEven(self):
        self.assertTrue(self.calculator.is_even(2))
        self.assertFalse(self.calculator.is_even(13))
        self.assertTrue(self.calculator.is_even(0))
        self.assertFalse(self.calculator.is_even(-3))

        with self.assertRaises(TypeError):
            self.calculator.is_even("string")



