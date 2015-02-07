# coding: utf-8
from mapping import Cell


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

    def retrieve_race(self):
        if self.map.home.get_pos() == self.map.vampires[0].get_pos():
            self.race = "vampire"
        else:
            self.race = "werewolve"

    def get_cells(self):
        return self.map.vampires if self.race == 'vampire' else self.map.werewolves

    def update(self):
        return

    def get_legal_cells_for(self, cell):
        """
        Returns a list of possible cells
        """
        legal_cells = []
        if cell.x > 0:
            legal_cells.append(Cell(cell.x - 1, cell.y))
        if cell.y > 0:
            legal_cells.append(Cell(cell.x, cell.y - 1))
        if cell.x < self.map.size_x - 1:
            legal_cells.append(Cell(cell.x + 1, cell.y))
        if cell.y < self.map.size_y - 1:
            legal_cells.append(Cell(cell.x, cell.y + 1))

        return legal_cells


    def get_legal_moves_for(self, cell):
        """
        Returns a list of possible moves
        """
        legal_moves = []
        for legal_cell in self.get_legal_cells_for(cell):
            for count in xrange(1, cell.population):
                legal_moves.append([cell.x, cell.y, count, legal_cell.x, legal_cell.y])
        return legal_moves

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
        cells = self.get_cells()
        legal_moves = []
        for cell in cells:
            legal_moves += self.get_legal_moves_for(cell)
        move = [legal_moves[0]]
        return move
