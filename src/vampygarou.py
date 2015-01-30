# coding: utf-8


class Vampygarou:
    """
    IA implementation
    """

    def __init__(self, manual):
        self.manual = manual
        return

    def update(self):
        return

    def get_moves(self):
        """
        Function returning the next moves

        params:         None
        return:         List of moves (moves = [from_x, from_y, amount, to_x, to_y])
        """
        if self.manual:
            return [[0, 0, 0, 0, 0]]
        return [[0, 0, 0, 0, 0]]


class Map:
    """
    Contains a game map
    """
    EMPTY = " "
    HOME = "S"
    HOUSE = "H"

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = [[Map.EMPTY for _ in range(size_x)] for _ in range(size_y)]

    def set_home(self, home_x, home_y):
        self.grid[home_x][home_y] = Map.HOME

    def add_house(self, house_x, house_y):
        self.grid[house_x][house_y] = Map.HOUSE

    def __repr__(self):
        """
        Representation of the map
        """
        s = "  "
        for x in range(self.size_y):
            for y in range(self.size_x):
                s += "|{} ".format(self.grid[x][y])
            s += "\n  "
        return s
