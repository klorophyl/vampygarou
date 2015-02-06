#  friends et foes sont stockés dans des dictionnaires de type
#  {num_of_team:[coords,number_of_people]}


class data_of_map(object):
    def __init__(self, friends, foes):
        super(data_of_map, self).__init__()
        self.friends = friends
        self.foes = foes


# successors sera un dictionnaire avec en clé le numero de l'action
# (type bouger, splitter, etc...) et l'état correspondant à l'action

class State(object):
    def __init__(self, abs, ord, number_of_people, succ):
        super(State, self).__init__()
        self.coord = [abs, ord]
        self.number_of_people = number_of_people
        self.successors = succ

    def act(action):
        self.coord = successors[action].coord
        self.number_of_people = successors[action].number_of_people
        self.successors = successors[action].successors
        return successors[action]


#  heuristique va utiliser les datas de la map pour générer
#  une valeur pour chaque état
def heuristique(state):
    pass


def max_value(state):
    if state.successors.size = 0:
        return heuristique(state)
    else:
        h = 0
        for action in Actions
            if heuristique(state.act(action)) > h:
                h = heuristique(state.act(action))
                action_to_play = action
        return heuristique


def mon_value():
    pass


def minimax():
    return "chibre"


def act(state, action):
    return Actions[state]