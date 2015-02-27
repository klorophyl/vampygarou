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
            return get_utility(state)
        else:
            depth -= 1
            value = -float("inf")
            succ = get_successors(state)
            for action_state in succ:
                value = max(value, min_value(action_state[0], depth))
        return value

    def min_value(self, state, depth):
        if depth == 0 or self.is_terminal(state):
            return get_utility(state)
        else:
            depth -= 1
            value = float("inf")
            succ = get_successors(state)
            for action_state in succ:
                value = min(value, max_value(action_state[0], depth))
        return value

    def minimax(self, state, race):
        actions = get_actions(state)
        value = float("inf")*-1
        for act in actions:
            if min_value(get_result(act, state), MAX_DEPTH) > value:
                value = min_value(get_result(act, state), MAX_DEPTH)
                act_to_play = act
        return act_to_play

    def get_alpha(self, state, depth, alpha, beta):
        if depth == 0 or self.is_terminal(state):
            return get_utility(state)
        else:
            depth -= 1
            value = -float("inf")
            succ = get_successors(state)
            count = 0
            while count < succ.length and alpha < beta:
                value = max(value, min_value(succ(count), depth, alpha, beta))

                alpha = max(value, alpha)
                count += 1
        return alpha

    def get_beta(self, state, depth, alpha, beta):
        if depth == 0 or self.is_terminal(state):
            return get_utility(state)
        else:
            depth -= 1
            value = float("inf")
            succ = get_successors(state)
            count = 0
            while count < succ.length and alpha < beta:
                value = min(value, max_value(succ(count), depth, alpha, beta))
                beta = min(value, beta)
                count += 1
        return beta
