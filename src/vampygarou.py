# coding: utf-8
import random

from strategy import Strategy
from mapping import Race


class Vampygarou:
    """
    IA implementation
    """

    def __init__(self, name, manual):
        self.name = name
        self.manual = manual
        self.map = None
        self.race = None
        self.strategy = Strategy("feed")
        return

    def retrieve_race(self):
        if self.map.home.get_pos() == self.map.vampires[0].get_pos():
            self.race = Race.VAMPIRES
        else:
            self.race = Race.WEREWOLVES

    def update(self):
        return

    def get_moves(self):
        """
        Function returning the next moves

        params:         None
        return:         List of moves (moves = [from_x, from_y, amount, to_x, to_y])
        """
        if self.manual:
            return self.get_manual_moves()

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

    def get_random_moves(self):
        """
        Choose a random moves in all legal moves
        """
        legal_moves = []
        for cell in self.get_cells():
            legal_moves += self.get_legal_moves_for(cell)

        return list(random.choice(legal_moves))
