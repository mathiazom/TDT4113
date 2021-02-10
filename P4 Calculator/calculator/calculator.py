"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 4 Calculator
made with ❤ by mathiom

Core class of calculator module
"""

import numbers
import re
import numpy as np
from functions import Function, Operator
from containers import Queue, Stack


class Calculator:
    """
    Performs calculations with a set of operators and functions
    Can calculate based on text by converting it to RPN
    """

    def __init__(self):
        self.functions = {
            'EXP': Function(np.exp),
            'LOG': Function(np.log),
            'SIN': Function(np.sin),
            'COS': Function(np.cos),
            'SQRT': Function(np.sqrt)
        }

        self.operators = {
            'ADD': Operator(np.add, 0),
            'SUBTRACT': Operator(np.subtract, 0),
            'MULTIPLY': Operator(np.multiply, 1),
            'DIVIDE': Operator(np.divide, 1)
        }
        self.operators.update({
            'PLUS': self.operators['ADD'],
            'MINUS': self.operators['SUBTRACT'],
            'TIMES': self.operators['MULTIPLY']
        })

        self.output_queue = Queue()

    def normal_to_rpn(self, input_queue):
        """Uses shunting yard procedure to convert normal to RPN
            input_queue is a list of elements of the following types:
            numpy.Number, (, ), Function, Operator
        """

        operator_stack = Stack()

        while not input_queue.is_empty():
            item = input_queue.pop()
            if isinstance(item, numbers.Number):
                self.output_queue.push(item)
            elif isinstance(item, Function) or item == "(":
                operator_stack.push(item)
            elif item == ")":
                while operator_stack.peek() != "(":
                    top = operator_stack.pop()
                    self.output_queue.push(top)
                operator_stack.pop()
            elif isinstance(item, Operator):
                while not operator_stack.is_empty():
                    top = operator_stack.peek()
                    if top == "(" or isinstance(top, Operator) and top.strength < item.strength:
                        break
                    self.output_queue.push(operator_stack.pop())
                operator_stack.push(item)
            else:
                raise Exception("Calculation item not recognized")

        while not operator_stack.is_empty():
            self.output_queue.push(operator_stack.pop())

    def parse_text(self, text):
        """
        Converts a given text to a normal notation queue
        """

        normal = Queue()

        text = text.replace(" ", "").upper()

        target_conversion = [
            (r"^-?\d+(\.\d*)?", float),
            (r"^\(|^\)", str),
            ("|".join(["^" + f for f in self.functions]), self.functions.get),
            ("|".join(["^" + o for o in self.operators]), self.operators.get)
        ]

        while len(text) > 0:
            for target, conversion in target_conversion:
                match = re.search(target, text)
                if match is not None:
                    result = match.group(0)
                    text = text[match.end(0):]
                    normal.push(conversion(result))
                    break

        return normal

    def calculate_expression(self, text):
        """
        Calculates the result of a calculation given in text form
        e.g. "1 add 2 multiply 3" => 7
        """

        normal = self.parse_text(text)

        self.normal_to_rpn(normal)

        return self.calculate()

    def calculate(self):
        """
        Perform the calculation in the output queue
        """

        stack = Stack()

        while not self.output_queue.is_empty():
            item = self.output_queue.pop()
            if isinstance(item, numbers.Number):
                stack.push(item)
            elif isinstance(item, Function):
                stack.push(item.execute(stack.pop()))
            elif isinstance(item, Operator):
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.push(item.execute(
                    operand1,
                    operand2
                ))
            else:
                raise Exception("Calculation item not recognized", item)

        return stack.pop()
