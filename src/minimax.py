
#  wow Gab, much English, very comments


def utility(state):
    pass


def terminal_test(state):
    pass


def successors(state):
    pass


def actions(state):
    pass


def result(action, state):
    pass


def max_value(state):
    if terminal_test(state):
        return utility(state)
    else:
        v = -1000
        succ = successors(state)
        for action_state in succ:
            v = max(v, min_value(action_state[0]))
    return v


def min_value(state):
    if terminal_test(state):
        return utility(state)
    else:
        v = 1000
        succ = successors(state)
        for action_state in succ:
            v = min(v, max_value(action_state[0]))
    return v


def minimax(state):
    actions = actions(state)
    v = -1000
    for act in actions:
        if min_value(result(act, state))

