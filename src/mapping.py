# coding: utf-8
from message import Colors
from collections import namedtuple


class Race(object):
    VAMPIRES = "vampires"
    WEREWOLVES = "werewolves"
    HUMANS = "humans"


class Cell(object):
    """
    A cell
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x, self.y)


class PopulatedCell(Cell):
    def __init__(self, x, y, population=0):
        super(PopulatedCell, self).__init__(x, y)
        self.population = population


class House(PopulatedCell):
    def __str__(self):
        return "H" + str(self.population)


class Home(Cell):
    pass


class Vampires(PopulatedCell):
    def __str__(self):
        return Colors.RED + "V" + str(self.population) + Colors.END


class Werewolves(PopulatedCell):
    def __str__(self):
        return Colors.BLUE + "W" + str(self.population) + Colors.END


Move = namedtuple('Move', ['from_x', 'from_y', 'amount', 'to_x', 'to_y'])


class Map:
    """
    Contains a game map
    """
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.home = []
        self.houses = []
        self.vampires = []
        self.werewolves = []

    def set_home(self, x, y):
        self._check_bounds(x, y, "Home")
        self.home = Home(x, y)

    def add_house(self, x, y):
        self._check_bounds(x, y, "House")
        self.houses.append(House(x, y))

    def set_cell(self, x, y, cell_type):
        self.grid[y][x] = cell_type

    def get_cell(self, x, y):
        """
        Returns the cell if populated
        """
        return self.get_cell_in(x, y, self.houses + self.vampires + self.werewolves)

    def get_cell_in(self, x, y, array):
        """
        Returns the cell if in a given array
        """
        for cell in array:
            if cell.get_pos() == (x, y):
                return cell

    def get_pop(self, x, y):
        """
        Returns the population for a given cell
        """
        cell = self.get_cell(x, y)
        return cell.population if cell else 0

    def get_race(self, x, y):
        """
        Returns the population type for a given cell
        """
        if self.get_cell_in(x, y, self.houses):
            return Race.HUMANS
        elif self.get_cell_in(x, y, self.vampires):
            return Race.VAMPIRES
        if self.get_cell_in(x, y, self.werewolves):
            return Race.WEREWOLVES

    def init_counts(self, cells_info):
        """
        Init the number of humans, vampires, and werewolves on the map.
        """
        self.vampires = []
        self.werewolves = []
        self.houses = []

        for cell in cells_info:
            x, y, humans, vampires, werewolves = cell
            if humans > 0:
                self.houses.append(House(x, y, humans))
            if vampires > 0:
                self.vampires.append(Vampires(x, y, vampires))
            if werewolves > 0:
                self.werewolves.append(Werewolves(x, y, werewolves))

    def update_with_changes(self, changes):
        """
        Update the number of humans, vampires, and werewolves on the map from changes sent by
        server.
        """
        for change in changes:
            # clean previous list from change
            self.houses = [h for h in self.houses if h.get_pos() != (change[0], change[1])]
            self.vampires = [v for v in self.vampires if v.get_pos() != (change[0], change[1])]
            self.werewolves = [w for w in self.werewolves if w.get_pos() != (change[0], change[1])]

            # apply change
            amount = change[2] or change[3] or change[4]
            to_change, cell_type = (
                (self.houses, House) if change[2] else
                (self.vampires, Vampires) if change[3] else
                (self.werewolves, Werewolves) if change[4] else
                (None, None)
            )
            if to_change is not None:
                to_change.append(cell_type(change[0], change[1], amount))

    def get_state_after_move(self, move):
        return 0

    def get_werewolve_population(self):
        """
        Returns total werewolves pop
        """
        return sum([w.population for w in self.werewolves])

    def get_vampire_population(self):
        """
        Returns total vampires pop
        """
        return sum([v.population for v in self.vampires])

    def get_neighbor_cells_of(self, cell):
        """
        Returns a list of possible cells
        """
        legal_cells = []

        # straight directions
        if cell.x > 0:
            legal_cells.append(Cell(cell.x - 1, cell.y))
        if cell.y > 0:
            legal_cells.append(Cell(cell.x, cell.y - 1))
        if cell.x < self.map.size_x - 1:
            legal_cells.append(Cell(cell.x + 1, cell.y))
        if cell.y < self.map.size_y - 1:
            legal_cells.append(Cell(cell.x, cell.y + 1))

        # diagonal directions
        if cell.x > 0 and cell.y > 0:
            legal_cells.append(Cell(cell.x - 1, cell.y - 1))
        if cell.x < self.map.size_x - 1 and cell.y > 0:
            legal_cells.append(Cell(cell.x + 1, cell.y - 1))
        if cell.x > 0 and cell.y < self.map.size_y - 1:
            legal_cells.append(Cell(cell.x - 1, cell.y + 1))
        if cell.x < self.map.size_x - 1 and cell.y < self.map.size_y - 1:
            legal_cells.append(Cell(cell.x + 1, cell.y + 1))

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
        grid = [["  " for x in range(self.size_x)] for y in range(self.size_y)]
        for house in self.houses:
            grid[house.y][house.x] = str(house)
        for vampire in self.vampires:
            grid[vampire.y][vampire.x] = str(vampire)
        for werewolve in self.werewolves:
            grid[werewolve.y][werewolve.x] = str(werewolve)

        s = "  -" + "---" * self.size_x + "\n  "
        for x in range(self.size_y):
            for y in range(self.size_x):
                s += "|{}".format(grid[x][y])
            s += "|\n  "
        s += "-" + "---" * self.size_x
        return s
