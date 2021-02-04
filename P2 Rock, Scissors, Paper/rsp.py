"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 2 Rock, Scissors, Paper
made with ❤ by mathiom

Simulates a single game or tournament between two players of Rock, Paper, Scissors

"""

from termcolor import colored
import players
import matplotlib.pyplot as plt

POINTS_WIN = 1
POINTS_TIE = 0.5
POINTS_LOSS = 0


class SingleGame:
    """Single round of Rock, Paper, Scissors"""

    def __init__(self, player1, player2):
        self.player1 = player1
        self.action1 = None
        self.player2 = player2
        self.action2 = None
        self.winner = None

    def perform_game(self):
        """Retrieve actions from each player and decide results"""
        self.action1 = self.player1.get_action()
        self.action2 = self.player2.get_action()
        player1points = POINTS_LOSS
        player2points = POINTS_LOSS
        if self.action1 is self.action2:
            self.winner = None
            player1points = POINTS_TIE
            player2points = POINTS_TIE
        elif self.action1 > self.action2:
            self.winner = self.player1
            player1points = POINTS_WIN
        else:
            self.winner = self.player2
            player2points = POINTS_WIN
        self.player1.register_result(self.action2, player1points)
        self.player2.register_result(self.action1, player2points)

    def show_result(self):
        """Log actions and results"""
        msg = f"\n#{self.__hash__()} " + \
              colored(str(self.action1), "blue") + " v. " + \
              colored(str(self.action2), "red") + " "
        if self.winner is None:
            msg += colored("It's a tie!", "green")
        else:
            color = "blue" if self.winner == self.player1 else "red"
            msg += colored(f"{self.winner} is the winner!", color)
        print(msg)


class Tournament:
    """Set of single games with the same players competing"""

    def __init__(self, player1, player2, number_of_games):
        self.player1 = player1
        self.player2 = player2
        self.number_of_games = number_of_games

    def arrange_single_game(self):
        """Perform a single game between the tournaments players"""
        game = SingleGame(self.player1, self.player2)
        game.perform_game()
        game.show_result()

    def arrange(self):
        """Arrange the specified number of games and plot results"""
        # Running average of points per game for each player
        points = [[], []]
        games_range = range(1, self.number_of_games + 1)
        # Perform tournament games in series
        for i in games_range:
            self.arrange_single_game()
            # Calculate current average points per game
            points[0].append(self.player1.points / i)
            points[1].append(self.player2.points / i)
        # Plot progression of average points per game
        plt.plot(games_range, points[0], c="blue", label=self.player1)
        plt.plot(games_range, points[1], c="red", label=self.player2)
        plt.axhline(y=0.5, c='black', ls='dotted')
        plt.legend(loc="lower left")
        plt.show()


Tournament(players.RandomPlayer(), players.RandomPlayer(), 300).arrange()
