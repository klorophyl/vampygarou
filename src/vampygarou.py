# coding: utf-8
from strategy import Strategy


class Vampygarou:
    """
    IA implementation
    """

    def __init__(self, name, is_manual, is_random):
        self.name = name
        self.manual = is_manual
        self.random = is_random
        self.map = None
        self.race = None
        self.strategy = None

    def retrieve_race(self):
        self.strategy = Strategy(race=self.map.get_player_race())

    def get_moves(self):
        """
        Function returning the next moves

        params:         None
        return:         List of moves (moves = [from_x, from_y, amount, to_x, to_y])
        """
        if self.manual:
            return self.get_manual_moves()
        elif self.random:
            return self.strategy.get_random_move(self.map)

        return self.strategy.get_next_move(self.map)

    def get_manual_moves(self):
        """
        Ask for move to manual player
        """
        moves_raw = raw_input(
            "\nEnter list of moves \"from_x, from_y, amount, to_x, to_y;"
            "from_x,from_y,amount,to_x,to_y\" : \n"
        ).strip().split(";")

        moves = [map(int, move.split(",")) for move in moves_raw]

        for move in moves:
            if len(move) != 5:
                print "One of your move is illegal, please respect the syntax"
                return self.get_moves()

        return moves
