
#  wow Gab, much English, very comments


def get_utility(state):
    pass


def is_terminal_test(state):
    pass


def get_successors(state):
    pass


def get_actions(state):
    pass


def get_result(action, state):
    pass


def max_value(state):
    if terminal_test(state):
        return utility(state)
    else:
        v = float("inf")*-1
        succ = successors(state)
        for action_state in succ:
            v = max(v, min_value(action_state[0]))
    return v


def min_value(state):
    if terminal_test(state):
        return utility(state)
    else:
        v = float("inf")
        succ = successors(state)
        for action_state in succ:
            v = min(v, max_value(action_state[0]))
    return v


def minimax(state):
    actions = actions(state)
    v = float("inf")*-1
    for act in actions:
        if min_value(result(act, state)) > v:
            v = min_value(result(act, state))
            act_to_play = act
    return act_to_play

