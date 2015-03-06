#  wow Gab, much English, very comment
from copy import copy
import itertools
import random
from mapping import Move, Race


class Strategy(object):
    MAX_DEPTH = 4

    def __init__(self, race):
        self.race = race

    def get_next_move(self, state):
        """
        Returns the chosen move
        """
        move = random.choice(self.get_actions(state))
        print move
        return move

    def get_utility(self, state, race):
        """
        Returns the heuristic
        """
        utility = state.get_vampire_population() - state.get_werewolve_population()
        return (1 if race == Race.VAMPIRES else -1) * utility

    def is_terminal(self, state):
        """
        Returns bool if the state is terminal
        """
        return state.get_werewolve_population() == 0 or state.get_vampire_population() == 0

    def get_actions_for_cell(self, cell, state):
        """
        Returns a list of possible actions on a given cell
        (list of list of Move)
        """
        legal_unit_moves = []
        legal_turns = []

        for neighbor in state.get_neighbor_cells_of(cell):
            neighbor_race = state.get_race(neighbor.x, neighbor.y)
            neighbor_pop = state.get_pop(neighbor.x, neighbor.y)

            # /!\ only move everyone for now
            for count in xrange(1, cell.population + 1):
                if self.check_rules_on_unit_move(neighbor_race, neighbor_pop, count):
                    legal_unit_moves.append(Move(cell.x, cell.y, count, neighbor.x, neighbor.y))

        for length in xrange(1, cell.population + 1):
            # you can't make more moves than your total population
            # WARNING : this loop won't work when total pop is high (combination ftw)
            for turn in itertools.combinations(legal_unit_moves, length):
                if self.is_turn_legal(turn, state):
                    legal_turns.append(list(turn))

        return legal_turns

    def is_turn_legal(self, turn, state):
        """
        Return if move is legal i.e. to neighbor and not too many peons moved
        """
        cell_pop = {}  # monitor count for cell in move
        for move in turn:
            if abs(move.from_x - move.to_x) > 1 or abs(move.from_y - move.to_y) > 1:
                # destination is not neighbor
                return False

            # increase pop count
            if not cell_pop.get(move.from_x):
                cell_pop[move.from_x] = {}
            if not cell_pop[move.from_x].get(move.from_y):
                cell_pop[move.from_x][move.from_y] = 0

            cell_pop[move.from_x][move.from_y] += move.amount

        for x, temp in cell_pop.iteritems():
            for y, count in temp.iteritems():
                if count > state.get_pop(x, y):
                    return False

        return True

    def check_rules_on_unit_move(self, cell_race, cell_pop, move_pop):
        """
        Check a set of rules to discriminate cells
        """
        # TBM
        if cell_race != self.race and cell_pop > move_pop:
            return False
        return True

    def get_successors(self, state):
        """
        Returns possible successors to a given state
        """
        return [self.get_result(action, state) for action in self.get_actions()]

    def get_actions(self, state):
        """
        Returns a list of possible actions on a given state
        """
        result = []
        cells = state.vampires if self.race == Race.VAMPIRES else state.werewolves
        possibilities = [self.get_actions_for_cell(cell, state) for cell in cells]

        for length in xrange(1, len(cells) + 1):
            for move in itertools.combinations(possibilities, length):
                result.append(list(move))

        return result[0][0]  # TODO understand this

    def get_result(self, action, state):
        """
        Returns state resulting of applying given action on given state
        """
        new_state = copy(state)
        for move in action:
            new_state.apply_move(move)

        return new_state

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
        Returns the alpha of a given state with given depth, alpha beta
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
