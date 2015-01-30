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
            moves_raw = raw_input(
                "\nEnter list of moves \"from_x,from_y,amount,to_x,to_y;from_x,from_y,amount,to_x,to_y\" : \n"
            ).strip().split(";")

            moves = [map(int, move.split(",")) for move in moves_raw]

            for move in moves:
                if len(move) != 5:
                    print "One of your move is illegal, please respect syntax"
                    return self.get_moves()

            return moves

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
        self.grid = [[Map.EMPTY for x in range(size_x)] for y in range(size_y)]

    def set_home(self, x, y):
        if not 0 < x < self.size_x:
            raise ValueError("Home x outside bounds")
        if not 0 < y < self.size_y:
            raise ValueError("Home y outside bounds")

        self.set_cell(x, y, Map.HOME)

    def add_house(self, x, y):
        self.set_cell(x, y, Map.HOUSE)

    def set_cell(self, x, y, cell_type):
        self.grid[y][x] = cell_type

    def __repr__(self):
        """
        Representation of the map
        """
        s = "  -" + "---" * self.size_x + "\n  "
        for x in range(self.size_y):
            for y in range(self.size_x):
                s += "|{} ".format(self.grid[x][y])
            s += "|\n  "
        s += "-" + "---" * self.size_x
        return s
