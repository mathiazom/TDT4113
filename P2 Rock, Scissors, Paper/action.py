"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 2 Rock, Scissors, Paper
made with ❤ by mathiom

Defines the concept of an action in Rock, Paper, Scissors

"""

from enum import Enum
import random


class Action(Enum):
    """Represents one of the three choices in Rock, Paper, Scissors"""
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def counter(self):
        """Get the action that beats this action"""
        if self is Action.ROCK:
            return Action.PAPER
        if self is Action.PAPER:
            return Action.SCISSORS
        if self is Action.SCISSORS:
            return Action.ROCK
        raise Exception("Action not recognized")

    def __gt__(self, other):
        return self is other.counter()


def get_random_action():
    """Randomly pick from the available actions"""
    return Action(random.randint(1, len(Action)))
