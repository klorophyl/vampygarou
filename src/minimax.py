
#  wow Gab, much English, very comments


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


def max_value(state):
    if is_terminal(state):
        return get_utility(state)
    else:
        value = -float("inf")
        succ = get_successors(state)
        for action_state in succ:
            value = max(value, min_value(action_state[0]))
    return value


def min_value(state):
    if is_terminal(state):
        return get_utility(state)
    else:
        value = float("inf")
        succ = get_successors(state)
        for action_state in succ:
            value = min(value, max_value(action_state[0]))
    return value


def minimax(state):
    actions = get_actions(state)
    value = float("inf")*-1
    for act in actions:
        if min_value(get_result(act, state)) > value:
            value = min_value(get_result(act, state))
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
            value = max(value, min_value(action_state[0], alpha, beta))
            alpha = max(value, alpha)
            count++
    return alpha


def get_beta(state, alpha, beta):
    if is_terminal(state):
        return get_utility(state)
    else:
        value = float("inf")
        succ = get_successors(state)
        while count < succ.length and alpha < beta: 
            value = min(value, max_value(action_state[0], alpha, beta))
            beta = min(value, beta)
            count++
    return beta
