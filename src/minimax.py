#  wow Gab, much English, very comment


class Strategy(object):
    MAX_DEPTH = 4

    def __init__(self, race):
        self.race = race
        return

    def get_next_move(self):
        """
        Returns the chosen move
        """
        return None

    def get_utility(self, state, race):
        """
        Returns the heuristic
        """
        utility = state.get_vampire_population - state.get_werewolve_population
        if race == "vampires":
            return utility
        else:
            return -utility

    def is_terminal(self, state):
        """
        Returns bool if the state is terminal
        """
        pass

    def get_successors(self, state):
        """
        Returns possible successors to a given state
        """
        pass

    def get_actions(self, state):
        """
        Returns a list of possible actions on a given state
        """
        pass

    def get_result(self, action, state):
        """
        Returns state resulting of applying given action on given state
        """
        pass

    def max_value(self, state, depth):
        """
        Returns max value according to minimax
        """
        if depth == 0 or self.is_terminal(state):
            return self.get_utility(state)
        else:
            depth -= 1
            value = -float("inf")
            succ = self.get_successors(state)
            for action_state in succ:
                value = max(value, self.min_value(action_state[0], depth))
        return value

    def min_value(self, state, depth):
        """
        Returns min value according to minimax
        """
        if depth == 0 or self.is_terminal(state):
            return self.get_utility(state)
        else:
            depth -= 1
            value = float("inf")
            succ = self.get_successors(state)
            for action_state in succ:
                value = min(value, self.max_value(action_state[0], depth))
        return value

    def minimax(self, state, race):
        """
        Return best action according to minimax on a given state and race
        """
        actions = self.get_actions(state)
        value = -float("inf")
        for act in actions:
            if self.min_value(self.get_result(act, state), Strategy.MAX_DEPTH) > value:
                value = self.min_value(self.get_result(act, state), Strategy.MAX_DEPTH)
                act_to_play = act
        return act_to_play

    def get_alpha(self, state, depth, alpha, beta):
        """
        Returns the alpha of a given state with given depth, alpha beta
        """
        if depth == 0 or self.is_terminal(state):
            return self.get_utility(state)
        else:
            depth -= 1
            value = -float("inf")
            succ = self.get_successors(state)
            count = 0
            while count < succ.length and alpha < beta:
                value = max(value, self.min_value(succ(count), depth, alpha, beta))

                alpha = max(value, alpha)
                count += 1
        return alpha

    def get_beta(self, state, depth, alpha, beta):
        """
        Returns the beta of a given state with given depth, alpha beta
        """
        if depth == 0 or self.is_terminal(state):
            return self.get_utility(state)
        else:
            depth -= 1
            value = float("inf")
            succ = self.get_successors(state)
            count = 0
            while count < succ.length and alpha < beta:
                value = min(value, self.max_value(succ(count), depth, alpha, beta))
                beta = min(value, beta)
                count += 1
        return beta
