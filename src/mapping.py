# coding: utf-8
from message import Colors
from copy import deepcopy


class Race(object):
    NONE = "none"
    VAMPIRES = "vampires"
    WEREWOLVES = "werewolves"
    HUMANS = "humans"


class Cell(object):
    def __init__(self, race, population=0):
        if population < 0:
            raise ValueError("Population must be positive")
        self.population = population
        self.race = race

    def __repr__(self):
        return "<{} {}>".format(self.race, self.population)

    def __str__(self):
        if self.race == Race.NONE:
            return "  "
        elif self.race == Race.VAMPIRES:
            return "V{}".format(self.population)
        elif self.race == Race.WEREWOLVES:
            return "W{}".format(self.population)
        elif self.race == Race.HUMANS:
            return "H{}".format(self.population)


class Move(object):
    """
    A move
    """
    def __init__(self, from_x, from_y, amount, to_x, to_y):
        self.from_x = from_x
        self.from_y = from_y
        self.amount = amount
        self.to_x = to_x
        self.to_y = to_y

    def __repr__(self):
        return "<Move {} ({}, {}) => ({}, {})>".format(
            self.amount, self.from_x, self.from_y, self.to_x, self.to_y
        )


class Map:
    """
    Contains a game map
    """
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = [[Cell(Race.NONE) for y in range(self.size_y)] for x in range(self.size_x)]
        self.home = None

    def add_human(self, x, y):
        self._check_bounds(x, y, "Human")
        self.grid[x][y] = Cell(Race.HUMANS, 0)

    def get_pop(self, x, y):
        """
        Returns the population for a given cell
        """
        return self.grid[x][y].population

    def set_home(self, x, y):
        self.home = (x, y)

    def get_player_race(self):
        x, y = self.home
        return self.grid[x][y]

    def get_race(self, x, y):
        """
        Returns the race for a given cell
        """
        return self.grid[x][y].race

    def init_counts(self, cells_info):
        """
        Init the number of humans, vampires, and werewolves on the map.
        """
        self.vampires = []
        self.werewolves = []
        self.humans = []

        for cell in cells_info:
            x, y, humans, vampires, werewolves = cell
            if humans > 0:
                self.grid[x][y] = Cell(Race.HUMANS, humans)
            if vampires > 0:
                self.grid[x][y] = Cell(Race.VAMPIRES, vampires)
            if werewolves > 0:
                self.grid[x][y] = Cell(Race.WEREWOLVES, werewolves)

    def update_with_changes(self, changes):
        """
        Update the number of humans, vampires, and werewolves on the map from changes sent by
        server.
        """
        for cell in changes:
            x, y, humans, vampires, werewolves = cell
            if humans > 0:
                self.grid[x][y] = Cell(Race.HUMANS, humans)
            if vampires > 0:
                self.grid[x][y] = Cell(Race.VAMPIRES, vampires)
            if werewolves > 0:
                self.grid[x][y] = Cell(Race.WEREWOLVES, werewolves)

    def pop_cell_at(self, x, y):
        cell = deepcopy(self.grid[x][y])
        self.grid[x][y] = Cell(Race.EMPTY)

        return cell

    def apply_move(self, move):
        """
        Update the map with the given move
        TODO add battles
        """
        from_cell = self.pop_cell_at(move.from_x, move.from_y)
        to_cell = self.pop_cell_at(move.to_x, move.to_y)

        if to_cell.population > 0:
            print "Warning: moving on someone else"

        race = from_cell.race

        if from_cell.population < move.amount:
            raise ValueError("Negative population")
        elif from_cell.population == move.amount:
            self.grid[move.to_x, move.to_y] = Cell(race, to_cell.population + move.amount)
        else:
            self.grid[move.to_x, move.to_y] = Cell(race, to_cell.population + move.amount)
            self.grid[move.from_x, move.from_y] = Cell(race, from_cell.population - move.amount)

    def get_popultaion(self, race):
        """
        Returns total werewolves pop
        """
        return sum([cell.population for row in self.grid for cell in row if cell.race == race])

    def get_neighbor_cells_of(self, cell):
        """
        Returns a list of possible cells
        """
        legal_cells = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 < cell.x + x < self.size_x and 0 < cell.y + y < self.size_y \
                        and not (x == 0 and y == 0):
                    legal_cells.append(self.grid[x][y])

        return legal_cells

    def _check_bounds(self, x, y, cell_type):
        """
        Raises if cell is on boundary
        """
        if not 0 <= x < self.size_x:
            raise ValueError(cell_type + " x outside bounds")
        if not 0 <= y < self.size_y:
            raise ValueError(cell_type + " y outside bounds")

    def __repr__(self):
        """
        Representation of the map
        """
        s = "  -" + "---" * self.size_x + "\n  "
        for y in range(self.size_y):
            for x in range(self.size_x):
                s += "|{}".format(self.grid[x][y])
            s += "|\n  "
        s += "-" + "---" * self.size_x
        return s
