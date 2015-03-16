#  wow Gab, much English, very comment
import itertools
import random
import time
from math import hypot
from copy import deepcopy
from mapping import Move, Race


class Strategy(object):
    MAX_DEPTH = 2

    def __init__(self, race):
        self.race = race

    def get_next_move(self, state):
        """
        Returns the chosen move
        """
        return self.minimax(deepcopy(state))

    def get_random_move(self, state):
        """
        Choose a move randomly
        """
        time.sleep(0.5)  # TO BE REMOVED
        return random.choice(self.get_actions(state))

    def get_utility(self, state):
        """
        Returns the heuristic
        """
        utility = 10 * (state.get_vampire_population() - state.get_werewolve_population())
        dist = 0
        for vampire in state.vampires:
            for werewolve in state.werewolves:
                dist += hypot(vampire.x - werewolve.x, vampire.y - werewolve.y)

        if self.race == Race.WEREWOLVES:
            utility *= -1

        utility -= dist

        return utility

    def is_terminal(self, state):
        """
        Returns bool if the state is terminal
        """
        return state.get_werewolve_population() == 0 or state.get_vampire_population() == 0

    def get_actions_for_cell(self, cell, state):
        """
        Returns a list of possible actions on a given cell (list of list of Move)
        """
        legal_unit_moves = []
        legal_turns = []

        for neighbor in state.get_neighbor_cells_of(cell):
            neighbor_race = state.get_race(neighbor.x, neighbor.y)
            neighbor_pop = state.get_pop(neighbor.x, neighbor.y)

            # /!\ only move everyone or 1 for now
            for count in range(cell.population, cell.population + 1):
                if self.check_rules_on_unit_move(neighbor_race, neighbor_pop,
                                                 count, cell.population):
                    legal_unit_moves.append(Move(cell.x, cell.y, count, neighbor.x, neighbor.y))

        for length in xrange(1, cell.population + 1):
            # you can't make more moves than your total population
            # WARNING : this loop won't work when total pop is high (combination ftw)
            for moves in itertools.combinations(legal_unit_moves, length):
                if self.is_turn_legal(moves, state):
                    legal_turns.append(list(moves))

        legal_turns.append([])  # add an empty move

        return legal_turns

    def is_turn_legal(self, moves, state):
        """
        Return if move is legal i.e. to neighbor and not too many peons moved
        """
        cell_pop = {}  # monitor count for cell in move
        for move in moves:
            if abs(move.from_x - move.to_x) > 1 or abs(move.from_y - move.to_y) > 1:
                # destination is not neighbor
                return False

            # increase pop count
            if not cell_pop.get(move.from_x):
                cell_pop[move.from_x] = {}
            if not cell_pop[move.from_x].get(move.from_y):
                cell_pop[move.from_x][move.from_y] = 0

            cell_pop[move.from_x][move.from_y] += move.amount

        if set([(m.from_x, m.from_y) for m in moves]) & set([(m.to_x, m.to_y) for m in moves]):
            # some destinations are also departures
            return False

        for x, temp in cell_pop.iteritems():
            for y, count in temp.iteritems():
                if count > state.get_pop(x, y):
                    return False

        return True

    def check_rules_on_unit_move(self, cell_race, cell_pop, move_pop, total_pop_on_cell):
        """
        Check a set of rules to discriminate cells
        cell_race :         target cell race
        cell_pop :          target cell pop
        move_pop :          pop you want to move
        total_pop_on_cell:  total pop on current cell
        """
        # TBM with bataille aleatoire
        if cell_race != self.race and cell_pop > move_pop:
            return False
        if ((move_pop < total_pop_on_cell / 4 or move_pop > total_pop_on_cell * 3 / 4)
                and move_pop != total_pop_on_cell):
            # do not leave behind too few people
            return False
        return True

    def get_successors(self, state):
        """
        Returns possible successors to a given state
        """
        return [self.get_result(action, state) for action in self.get_actions(state)]

    def get_actions(self, state):
        """
        Returns a list of possible actions on a given state (list of list of list of Move)
        """
        result = []
        cells = state.vampires if self.race == Race.VAMPIRES else state.werewolves

        # all the possible actions, sorted by origin cell
        possibilities = [self.get_actions_for_cell(cell, state) for cell in cells]
        product = itertools.product(*possibilities)

        for action in product:
            if len(action) > 0:
                result.append([item for sublist in action for item in sublist])

        return result

    def get_result(self, action, state):
        """
        Returns state resulting of applying given action on given state
        """
        new_state = deepcopy(state)
        for move in action:
            new_state.apply_move(move)

        return new_state

    def minimax(self, state):
        """
        Return best action according to minimax on a given state and race
        """
        actions = self.get_actions(state)
        alpha = -float("inf")
        beta = float("inf")
        value = -float("inf")
        action_to_play = None
        for action in actions:
            action_value = self.min_value(
                self.get_result(action, state), Strategy.MAX_DEPTH, alpha, beta
            )
            if action_value > value:
                value = action_value
                action_to_play = action

        if action_to_play is None:
            raise ValueError("Something went wrong, action_value stayed at -inf")

        return action_to_play

    def max_value(self, state, depth, alpha, beta):
        """
        Returns max value according to minimax
        """
        if depth <= 0 or self.is_terminal(state):
            return self.get_utility(state)
        else:
            successors = self.get_successors(state)
            for action_state in successors:
                alpha = max(alpha, self.min_value(action_state, depth - 1, alpha, beta))
                if alpha >= beta:
                    return beta

        return alpha

    def min_value(self, state, depth, alpha, beta):
        """
        Returns min value according to minimax
        """
        if depth <= 0 or self.is_terminal(state):
            return self.get_utility(state)
        else:
            successors = self.get_successors(state)
            for action_state in successors:
                beta = min(beta, self.max_value(action_state, depth - 1, alpha, beta))
                if alpha >= beta:
                    return alpha

        return beta
