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

    def get_legal_moves_for(self):
        """
        Returns a list of possible moves
        """
        return

    def get_moves(self):
        """
        Function returning the next moves

        params:         None
        return:         List of moves (moves = [from_x, from_y, amount, to_x, to_y])
        """
        if self.manual:
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

        return [[0, 0, 0, 0, 0]]
