"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 2 Rock, Scissors, Paper
made with ❤ by mathiom

Collection of players implementing different strategies

"""
from action import Action, get_random_action


class Player:
    """Abstract player picking actions based on some strategy"""

    def __init__(self):
        self.points = 0
        self.games_played = 0
        self.opponent_actions = []

    def get_action(self):
        """Provide action to be performed"""
        raise NotImplementedError("Method not implemented")

    def __str__(self):
        """Provide player name for logging"""
        return self.__class__.__name__

    def register_result(self, opponent_action, points):
        """Register game result for future games"""
        self.games_played += 1
        self.points += points
        self.opponent_actions.append(opponent_action)


class RandomPlayer(Player):
    """Player picking a random action every time"""

    def get_action(self):
        return get_random_action()


class SequentialPlayer(Player):
    """
    Player cycling through the available actions.
    First action is picked at random.
    """

    def __init__(self):
        super().__init__()
        self.prev_action = get_random_action()

    def get_action(self):
        action = None
        if self.prev_action is Action.SCISSORS:
            action = Action.ROCK
        elif self.prev_action is Action.ROCK:
            action = Action.PAPER
        elif self.prev_action is Action.PAPER:
            action = Action.SCISSORS
        self.prev_action = action
        return action


class MostCommonPlayer(Player):
    """Player countering the opponents most common actions"""

    def get_action(self):
        """Retrieve the opponents most common action, and counter it"""
        if len(self.opponent_actions) == 0:
            return get_random_action()
        most_common_action = max(self.opponent_actions, key=self.opponent_actions.count)
        return most_common_action.counter()


class HistorianPlayer(Player):
    """
    Player looking for patterns in the opponents play
    When picking an action, this player looks at a number (decided by "remember")
    of previous actions performed by the opponent. It then attempts to find this sequence
    in previous rounds and what action the opponent followed this up with. The Historian will then
    pick the counter of the most common follow-up. Else a random action is picked
    """

    def __init__(self, remember):
        super().__init__()
        self.remember = remember

    def __str__(self):
        """Provide player name for logging"""
        return f"{self.__class__.__name__}({self.remember})"

    def get_opponent_follow_ups(self, sequence):
        """Find the opponents previous follow-ups to the given sequence (if any)"""
        follow_ups = []
        for i in range(len(self.opponent_actions) - self.remember - 1):
            # Check if this index starts a previous occurrence of the sequence
            if self.opponent_actions[i:i + self.remember] == sequence:
                # Get the follow up of this previous occurrence of the sequence
                follow_ups.append(self.opponent_actions[i + self.remember])
        return follow_ups

    def get_action(self):
        # Check if total prev actions could allow another occurrence of sequence
        if len(self.opponent_actions) - 2 * self.remember < 1:
            print("Rolling the dice...")
            return get_random_action()
        # Extract the sequence to search for in previous rounds
        subsequence = self.opponent_actions[-self.remember:]
        follow_ups = self.get_opponent_follow_ups(subsequence)
        if len(follow_ups) == 0:
            # Found no previous occurrence of sequence
            return get_random_action()
        # Get counter of most common follow-up
        return max(follow_ups, key=follow_ups.count).counter()
