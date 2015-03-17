#  wow Gab, much English, very comment
import itertools
import random
import time
from math import hypot
from copy import deepcopy
from mapping import Move, Race, Map


class Strategy(object):
    MAX_DEPTH = 3
    MAX_POP_MOVABLE = 4
    SUB_MAP_COUNT = 2

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
        return random.choice(self.get_actions(state))

    def get_utility(self, state):
        """
        Returns the heuristic
        """
        utility = 0
        coeff_enemy = 1000
        coeff_human = 100

        enemy_cells = state.get_cells(Race.WEREWOLVES if self.race == Race.VAMPIRES else Race.VAMPIRES)
        friend_cells = state.get_cells(self.race)
        human_cells = state.get_cells(Race.HUMANS)

        werewolves = state.get_population(Race.WEREWOLVES)
        vampires = state.get_population(Race.VAMPIRES)
        if state.get_population(self.race) == 0:
            return -float("inf")

        if state.get_population(self.race) == vampires + werewolves:
            return float("inf")

        for friend_cell in friend_cells:
            dist_min = float("inf")
            for human_cell in human_cells:
                if hypot(friend_cell[1] - human_cell[1], friend_cell[2] - human_cell[2]) < dist_min:
                    dist_min = hypot(friend_cell[1] - human_cell[1], friend_cell[2] - human_cell[2])
                    closest_human = human_cell
            surplus_pop = closest_human[0].population if closest_human[0].population < friend_cell[0].population else 0
            danger = 0
            for enemy_cell in enemy_cells:
                if hypot(enemy_cell[1] - closest_human[1], enemy_cell[2] - closest_human[2]) < dist_min:
                    if friend_cell[0].population > 1.5 * (enemy_cell[0].population + surplus_pop ):
                        danger += 0
                    else:
                        danger += (enemy_cell[0].population - friend_cell[0].population)*5

            utility += 3*surplus_pop - 2*danger + 3*dist_min

        """for enemy_cell in enemy_cells: 
            for friend_cell in friend_cells:
                dist = hypot(friend_cell[1] - enemy_cell[1], friend_cell[2] - enemy_cell[2])
                enemy_pop = enemy_cell[0].population
                friend_pop = friend_cell[0].population
                diff_pop = friend_pop - enemy_pop
                utility += coeff_enemy / dist * (diff_pop if friend_pop > 1.5 * enemy_pop else 0)

        for human_cell in human_cells:
            for friend_cell in friend_cells:
                dist = hypot(friend_cell[1] - human_cell[1], friend_cell[2] - human_cell[2])
                human_pop = human_cell[0].population
                friend_pop = friend_cell[0].population
                diff_pop = friend_pop - human_pop
                utility += coeff_human / dist * (diff_pop if diff_pop > 0 else 0)

        utility += 1000000 * state.get_population(self.race)"""

        return utility

    def is_terminal(self, state):
        """
        Returns bool if the state is terminal
        """
        werewolves = state.get_population(Race.WEREWOLVES)
        vampires = state.get_population(Race.VAMPIRES)
        return werewolves == 0 or vampires == 0

    def get_actions_for_cell(self, cell, x, y, state):
        """
        Returns a list of possible actions on a given cell (list of list of Move)
        """
        legal_unit_moves = []
        legal_turns = []

        for neighbor, neighbor_x, neighbor_y in state.get_neighbor_cells_of(x, y):
            # /!\ only move everyone or 1 for now
            for count in xrange(1, cell.population + 1):
                if self.check_rules_on_unit_move(neighbor.race, neighbor.population,
                                                 count, cell.population):
                    legal_unit_moves.append(Move(x, y, count, neighbor_x, neighbor_y))

        for length in xrange(1, cell.population / self.MAX_POP_MOVABLE + 1):
            # you can't make more moves than your total population
            # WARNING : this loop won't work when total pop is high (combination ftw)
            combi = list(itertools.combinations(legal_unit_moves, length))
            for moves in combi:
                if self.is_turn_legal(moves, state):
                    legal_turns.append(list(moves))

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

        if (move_pop != total_pop_on_cell
                and (move_pop < self.MAX_POP_MOVABLE
                     or (total_pop_on_cell - move_pop < self.MAX_POP_MOVABLE))):
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
        cells = state.get_player_cells_and_coordinates()

        # all the possible actions, sorted by origin cell
        possibilities = [self.get_actions_for_cell(cell, x, y, state) for cell, x, y in cells]
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

        # 1 : determiner les zones d'interet
        self.evaluate_sub_zones(state)
        # 2 : trier actions

        for action in actions:
            action_value = self.min_value(
                self.get_result(action, state), Strategy.MAX_DEPTH - 1, alpha, beta
            )
            if action_value > value:
                value = action_value
                action_to_play = action

        if action_to_play is None:
            raise ValueError("Something went wrong, action_value stayed at -inf")

        return action_to_play

    def evaluate_sub_zones(self, state):
        """
        Split map into subzones and evaluate their worth
        """
        subzones = []
        subzone_size_x = state.size_x / self.SUB_MAP_COUNT
        subzone_size_y = state.size_y / self.SUB_MAP_COUNT

        for i in xrange(0, self.SUB_MAP_COUNT):
            for j in xrange(0, self.SUB_MAP_COUNT):
                offset_x = 0 if i != self.SUB_MAP_COUNT - 1 else state.size_x - self.SUB_MAP_COUNT * subzone_size_x
                offset_y = 0 if j != self.SUB_MAP_COUNT - 1 else state.size_y - self.SUB_MAP_COUNT * subzone_size_y
                subzone = Map(subzone_size_x + offset_x, subzone_size_y + offset_y)
                changes = []
                for k in xrange(0, subzone.size_x):
                    for l in xrange(0, subzone_size_y):
                        world_coord = (k + i * subzone_size_x, l + j * subzone_size_y)
                        cell = state.grid[world_coord[0]][world_coord[1]]
                        human_pop = 0 if cell.race != Race.HUMANS else cell.population
                        wolf_pop = 0 if cell.race != Race.WEREWOLVES else cell.population
                        vampire_pop = 0 if cell.race != Race.VAMPIRES else cell.population
                        changes.append((k, l, human_pop, vampire_pop, wolf_pop))
                subzone.update_with_changes(changes)
                subzones.append(subzone)

        

        # import ipdb; ipdb.set_trace()

    def max_value(self, state, depth, alpha, beta):
        """
        Returns max value according to minimax
        """
        # print "max_value, depth: %s, alpha : %s, beta : %s" % (depth, alpha, beta)
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
        # print "min_value, depth: %s, alpha : %s, beta : %s" % (depth, alpha, beta)
        if depth <= 0 or self.is_terminal(state):
            return self.get_utility(state)
        else:
            successors = self.get_successors(state)
            for action_state in successors:
                beta = min(beta, self.max_value(action_state, depth - 1, alpha, beta))
                if alpha >= beta:
                    return alpha

        return beta
