# coding: utf-8


class Vampygarou:
    """
    IA implementation
    """

    def __init__(self, name, manual):
        self.name = name
        self.manual = manual
        self.map = None
        self.race = None
        return

    def update(self):
        return

    def get_legal_moves_for(self, cell):
        """
        Returns a list of possible moves
        """
        return []

    def get_moves(self):
        """
        Function returning the next moves

        params:         None
        return:         List of moves (moves = [from_x, from_y, amount, to_x, to_y])
        """
        if self.manual:
            return self.get_manual_moves()

        return self.get_random_moves()

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
        cells = self.map.vampires if self.race == 'vampire' else self.map.werewolves
        legal_moves = []
        for cell in cells:
            legal_moves += self.get_legal_moves_for(cell)
        return [[0, 0, 0, 0, 0]]
