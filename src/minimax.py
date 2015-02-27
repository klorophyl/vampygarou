#  wow Gab, much English, very comment


class Strategy(object):
    MAX_DEPTH = 4

    def __init__(self, race):
        self.race = race
        return

    def get_next_move(self):
        return None

    def get_utility(self, state, race):
        utility = state.get_vampire_population - state.get_werewolve_population
        if race == "vampires":
            return utility
        else:
            return -utility

    def is_terminal(self, state):
        pass

    def get_successors(self, state):
        pass

    def get_actions(self, state):
        pass

    def get_result(self, action, state):
        pass

    def max_value(self, state, depth):
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
        actions = self.get_actions(state)
        value = float("inf")*-1
        for act in actions:
            if self.min_value(self.get_result(act, state), Strategy.MAX_DEPTH) > value:
                value = self.min_value(self.get_result(act, state), Strategy.MAX_DEPTH)
                act_to_play = act
        return act_to_play

    def get_alpha(self, state, depth, alpha, beta):
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
