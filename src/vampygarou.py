# coding: utf-8
import random, itertools

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

    def get_cell(self, x, y):
        cell = [cell for cell in self.get_cells() if cell.get_pos() == (x, y)]
        return cell[0] if cell else None

    def update(self):
        return

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

    def is_move_legal(self, move):
        """
        Return if move is legal ie to neighbor and not to many peons moved
        """
        cell_pop = {}   # monitor count for cell in move
        for cell_move in move:
            if abs(cell_move[0] - cell_move[3]) > 1 or abs(cell_move[1] - cell_move[4]) > 1:
                # destination is not neighbor
                return False

            # increase pop count
            if not cell_pop.get(cell_move[0]):
                cell_pop[cell_move[0]] = {}
            if not cell_pop[cell_move[0]].get(cell_move[1]):
                cell_pop[cell_move[0]][cell_move[1]] = 0

            cell_pop[cell_move[0]][cell_move[1]] += cell_move[2]

        for x, temp in cell_pop.iteritems():
            for y, count in temp.iteritems():
                if count > self.get_cell(x, y).population:
                    return False

        return True

    def get_legal_moves_for(self, cell):
        """
        Returns a list of possible moves
        """
        legal_unit_moves = []
        legal_moves = []
        total_pop = sum(cell.population for cell in self.get_cells())

        for legal_cell in self.get_neighbor_cells_of(cell):
            for count in range(1, cell.population + 1):
                legal_unit_moves.append([cell.x, cell.y, count, legal_cell.x, legal_cell.y])

        for length in range(1, total_pop + 1):
            # you cant make more moves than your total population
            # WARNING : this loop won't work when total pop is high (combination ftw)
            for move in itertools.combinations(legal_unit_moves, length):
                if self.is_move_legal(move):
                    legal_moves.append(move)

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
        legal_moves = []
        for cell in self.get_cells():
            legal_moves += self.get_legal_moves_for(cell)

        return list(random.choice(legal_moves))
