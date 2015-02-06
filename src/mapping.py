# coding: utf-8
from message import Colors


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

    def init_counts(self, cells_info):
        """
        Update the number of humans, vampires, and werewolves on the map.
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

    def _check_bounds(self, x, y, cell_type):
        if not 0 < x < self.size_x:
            raise ValueError(cell_type + " x outside bounds")
        if not 0 < y < self.size_y:
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
