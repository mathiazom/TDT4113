"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 4 Calculator
made with ❤ by mathiom

Functions to be used in Calculator
"""

import numbers


class Operator:
    """
    Function taking exactly two number operands, and of a certain precedence
    """

    def __init__(self, operation, strength):
        self.operation = operation
        self.strength = strength

    def execute(self, operand1, operand2):
        """Perform the appropriate operation on the given operands"""
        return self.operation(operand1, operand2)

    def __str__(self):
        return self.operation.__name__


class Function:
    """
    Function taking a single number operand and applying some operation
    """

    def __init__(self, func):
        self.func = func

    def execute(self, operand, debug=True):
        """Perform the appropriate operation on the given operand"""
        if not isinstance(operand, numbers.Number):
            raise TypeError("The element must be a number")
        result = self.func(operand)

        if debug:
            print(f"Function {self.func.__name__} ({operand}) = {result}")

        return result

    def __str__(self):
        return self.func.__name__
