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
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

    def __repr__(self):
        """
        Representation of the map
        """
        s = ""
        for _ in range(self.size_y):
            for _ in range(self.size_x):
                s += "|  "
            s += "\n"
        return s
