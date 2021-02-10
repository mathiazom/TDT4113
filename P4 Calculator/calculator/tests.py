"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 4 Calculator
made with ❤ by mathiom

Test cases
"""

import unittest
import numpy as np
from containers import Queue, Stack
from functions import Operator, Function
from calculator import Calculator


class TestQueue(unittest.TestCase):
    """Test cases for the Queue implementation"""

    def setUp(self):
        self.queue = Queue()

    def test_queue_empty_from_start(self):
        """Make sure the queue is empty before any push call"""
        self.assertTrue(self.queue.is_empty(), "Fresh queue was not empty")

        with self.assertRaises(
                AssertionError, msg="Peek on empty queue did not raise error"
        ) as catcher:
            self.queue.peek()
        self.assertEqual(catcher.exception.__class__, AssertionError)

    def test_queue_push(self):
        """Make sure push actually inserts the item at the bottom"""
        item1 = "aksiomo"
        item2 = "malsato"
        self.queue.push(item1)
        self.assertEqual(self.queue.peek(), item1, "Peek did not return first pushed item")
        self.queue.push(item2)
        self.assertEqual(self.queue.peek(), item1,
                         "Peek did not return first pushed item after second push"
                         )
        self.assertNotEqual(self.queue.peek(), item2, "Peek returned second item before first item")

    def test_queue_push_pop_list(self):
        """Make sure pushin items one by one will return the same list when popping"""
        items = ["aksiomo", "malsato", "vesto", "peko", "fabelo"]
        for item in items:
            self.queue.push(item)
        popped_list = []
        while not self.queue.is_empty():
            popped_list.append(self.queue.pop())
        self.assertListEqual(items, popped_list, "Pushed items did not equal popped items")

    def test_queue_peek(self):
        """Make sure a pushed item is visible through peek()"""
        item1 = "aksiomo"
        self.queue.push(item1)
        peeked = self.queue.peek()
        self.assertEqual(self.queue.peek(), peeked, "Peeked item changed without push or pop")

    def test_queue_pop(self):
        """Make sure pop() returns the first-in item"""
        item1 = "aksiomo"
        item2 = "malsato"
        self.queue.push(item1)
        self.queue.push(item2)
        self.assertEqual(item1, self.queue.pop(), "First pop did not return first in queue")
        self.assertEqual(item2, self.queue.pop(), "Second pop did not return second in queue")


class TestStack(unittest.TestCase):
    """Test cases for the Stack implementation"""

    def setUp(self):
        self.stack = Stack()

    def test_queue_empty_from_start(self):
        """Make sure the stack is empty before any push call"""
        self.assertTrue(self.stack.is_empty(), "Fresh stack was not empty")

        with self.assertRaises(
                AssertionError, msg="Peek on empty stack did not raise error"
        ) as catcher:
            self.stack.peek()
        self.assertEqual(catcher.exception.__class__, AssertionError)

    def test_queue_push(self):
        """Make sure push actually insert the item at the top"""
        item1 = "aksiomo"
        item2 = "malsato"
        self.stack.push(item1)
        self.assertEqual(self.stack.peek(), item1, "Peek did not return last pushed item")
        self.stack.push(item2)
        self.assertEqual(self.stack.peek(), item2,
                         "Peek did not return last pushed item after second push"
                         )
        self.assertNotEqual(self.stack.peek(), item1, "Peek returned first item before second item")

    def test_queue_push_pop_list(self):
        """Make sure pushin items one by one will return the (reversed) list when popping"""
        items = ["aksiomo", "malsato", "vesto", "peko", "fabelo"]
        for item in items:
            self.stack.push(item)
        popped_list = []
        while not self.stack.is_empty():
            popped_list.append(self.stack.pop())
        popped_list.reverse()
        self.assertListEqual(items, popped_list, "Pushed items did not equal popped items")

    def test_queue_peek(self):
        """Make sure a pushed item is visible through peek()"""
        item1 = "aksiomo"
        self.stack.push(item1)
        peeked = self.stack.peek()
        self.assertEqual(self.stack.peek(), peeked, "Peeked item changed without push or pop")

    def test_queue_pop(self):
        """Make sure pop() returns the last-in item"""
        item1 = "aksiomo"
        item2 = "malsato"
        self.stack.push(item1)
        self.stack.push(item2)
        self.assertEqual(item2, self.stack.pop(), "First pop did not return top in stack")
        self.assertEqual(item1, self.stack.pop(), "Second pop did not return top in stack")


class TestOperator(unittest.TestCase):
    """Test for the Operator implementation"""

    def test(self):
        """Check example calculation"""
        add_op = Operator(operation=np.add, strength=0)
        multiply_op = Operator(operation=np.multiply, strength=1)
        self.assertEqual(7, add_op.execute(1, multiply_op.execute(2, 3)))


class TestFunction(unittest.TestCase):
    """Test for the Function implementation"""

    def test(self):
        """Check example calculation"""
        exp_func = Function(np.exp)
        sin_func = Function(np.sin)
        self.assertEqual(1, exp_func.execute(sin_func.execute(0, debug=False), debug=False))


class CalculatorTest(unittest.TestCase):
    """Test for the Calculator implementation"""

    def test(self):
        """Check example calculation"""
        calc = Calculator()
        self.assertAlmostEqual(
            1096.633158428,
            calc.calculate_expression("EXP (1 add 2 multiply 3)")
        )
        self.assertAlmostEqual(
            148.4131591026,
            calc.calculate_expression(
                "EXP(((15 DIVIDE (7 SUBTRACT (1 ADD 1 ADD LOG 1))) MULTIPLY 3)SUBTRACT (2 ADD (1 ADD 1)))"
            )
        )
