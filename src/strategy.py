#  wow Gab, much English, very comment
import itertools
import random
from math import hypot
from copy import deepcopy
from mapping import Move, Race


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


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

    def get_bourrin_move(self, state):
        """
        Attack nearest human
        When no humans are left, attack nearest enemy
        """
        enemy_cells = state.get_cells(Race.WEREWOLVES if self.race == Race.VAMPIRES else Race.VAMPIRES)
        friend_cells = state.get_cells(self.race)
        human_cells = state.get_cells(Race.HUMANS)

        us, our_x, our_y = friend_cells[0]

        target = self.choose_target(us, our_x, our_y, enemy_cells, human_cells, state)
        print target
        move = self.get_move_to_next_target(us, our_x, our_y, target)

        return [move]

    def choose_target(self, us, our_x, our_y, enemy_cells, human_cells, state):
        # prio 1: avoid strong enemy
        print 1
        for cell, x, y in enemy_cells:
            if max([abs(our_x - x), abs(our_y - y)]) < 3 and cell.population >= us.population:
                target_x, target_y = our_x + sign(our_x - x), our_y + sign(our_y - y)
                if self.is_target_legal(target_x, target_y, state):
                    return target_x, target_y

        # avoid strong humans
        print 2
        for cell, x, y in human_cells:
            if max([abs(our_x - x), abs(our_y - y)]) < 2 and cell.population > us.population:
                target_x, target_y = our_x + sign(our_x - x), our_y + sign(our_y - y)
                if self.is_target_legal(target_x, target_y, state):
                    return target_x, target_y

        # prio 2: attack weak enemy
        print 3
        min_dist = float("inf")
        target_x, target_y = None, None
        for cell, x, y in enemy_cells:
            dist = max([abs(our_x - x), abs(our_y - y)])
            if dist < min_dist and cell.population * 1.5 <= us.population:
                min_dist = dist
                target_x, target_y = x, y

        if target_x is not None:
            return target_x, target_y

        # prio 3: attack weak human
        print 4
        for cell, x, y in human_cells:
            dist = max([abs(our_x - x), abs(our_y - y)])
            if dist < min_dist and cell.population <= us.population:
                min_dist = dist
                target_x, target_y = x, y

        if target_x is not None:
            return target_x, target_y

        # prio 4: attack anything
        print 5
        for cell, x, y in enemy_cells + human_cells:
            dist = max([abs(our_x - x), abs(our_y - y)])
            if dist < min_dist:
                min_dist = dist
                target_x, target_y = x, y

        return target_x, target_y

    def get_move_to_next_target(self, us, our_x, our_y, target):
        target_x, target_y = target

        move = Move(our_x, our_y, us.population,
                    our_x + sign(target_x - our_x), our_y + sign(target_y - our_y))

        # if not self.is_turn_legal([])
        return move

    def is_target_legal(self, target_x, target_y, state):
        return 0 < target_x < state.size_x and 0 < target_y < state.size_y

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

        for enemy_cell in enemy_cells:
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

        utility += 1000000 * state.get_population(self.race)

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
