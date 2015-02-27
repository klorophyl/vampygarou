
#  heuristique va utiliser les datas de la map pour générer
#  une valeur pour chaque état


def heuristique(state):
    pass


def max_value(state):
    if state.successors.size = 0:
        return heuristique(state)
    else:
        h = 0
        for action in Actions:
            if heuristique(state.act(action)) > h:
                h = heuristique(state.act(action))
                action_to_play = action
        return heuristique


def min_value():
    pass


def minimax():
    return "chibre"


def act(state, action):
    return Actions[state]
