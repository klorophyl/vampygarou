
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
