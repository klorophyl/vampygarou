
#  wow Gab, much English, very comments
MAX_DEPTH = 4


def get_utility(state):
    pass


def is_terminal(state):
    pass


def get_successors(state):
    pass


def get_actions(state):
    pass


def get_result(action, state):
    pass


def max_value(state, depth):
    if depth == 0:
        return get_utility(state)
    else:
        depth -= 1
        value = -float("inf")
        succ = get_successors(state)
        for action_state in succ:
            value = max(value, min_value(action_state[0], depth))
    return value


def min_value(state, depth):
    if depth == 0:
        return get_utility(state)
    else:
        depth -= 1
        value = float("inf")
        succ = get_successors(state)
        for action_state in succ:
            value = min(value, max_value(action_state[0], depth))
    return value


def minimax(state):
    actions = get_actions(state)
    value = float("inf")*-1
    for act in actions:
        if min_value(get_result(act, state), MAX_DEPTH) > value:
            value = min_value(get_result(act, state), MAX_DEPTH)
            act_to_play = act
    return act_to_play


def get_alpha(state, alpha, beta):
    if is_terminal(state):
        return get_utility(state)
    else:
        value = -float("inf")
        succ = get_successors(state)
        count = 0
        while count < succ.length and alpha < beta:
            value = max(value, min_value(succ(count), alpha, beta))

            alpha = max(value, alpha)
            count += 1
    return alpha


def get_beta(state, alpha, beta):
    if is_terminal(state):
        return get_utility(state)
    else:
        value = float("inf")
        succ = get_successors(state)
        count = 0
        while count < succ.length and alpha < beta:
            value = min(value, max_value(succ(count), alpha, beta))
            beta = min(value, beta)
            count += 1
    return beta
