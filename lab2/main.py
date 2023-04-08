import re
"""
Program that plays draughts (checkers) with user on 8x8 board using min-max with alpha-beta prunning
"""


class Game:
    """Game"""

    def __init__(self, size):
        self.board_size = size
        self.white_positions = self.initialize_white()
        self.black_positions = self.initialize_black()
        # print(self.white_positions)
        # print(self.black_positions)

    def initialize_white(self):
        """Initialize white pieces"""
        white_positions = []
        for y_coordinate in range(3):
            for x_coordinate in range(self.board_size):
                if y_coordinate % 2 == 0:
                    if x_coordinate % 2 == 1:
                        white_positions.append(
                            (x_coordinate, y_coordinate, False))
                else:
                    if x_coordinate % 2 == 0:
                        white_positions.append(
                            (x_coordinate, y_coordinate, False))
        return white_positions

    def initialize_black(self):
        """Initialize black pieces"""
        black_positions = []
        for y_coordinate in range(self.board_size - 3, self.board_size):
            for x_coordinate in range(self.board_size):
                if y_coordinate % 2 == 0:
                    if x_coordinate % 2 == 1:
                        black_positions.append(
                            (x_coordinate, y_coordinate, False))
                else:
                    if x_coordinate % 2 == 0:
                        black_positions.append(
                            (x_coordinate, y_coordinate, False))
        return black_positions

    def check_move_out_of_bounds(self, from_, to):
        """Check if the move destination is out of the bounds of the board"""
        if to[0] < 0 or to[0] >= self.board_size:
            print(
                f"Illegal move! Final x coordinate must be between 0 and {self.board_size-1}!")
        if to[1] < 0 or to[1] >= self.board_size:
            print(
                f"Illegal move! Final y coordinate must be between 0 and {self.board_size-1}!")
            return True
        return False

    def check_piece_exists(self, coords, color):
        """Check if a piece of given color exists at a given spot"""
        if color == "white":
            if any(piece in self.white_positions for piece in ((*coords, False), (*coords, False))):
                return True
        else:
            if any(piece in self.black_positions for piece in ((*coords, False), (*coords, False))):
                return True
        return False

    def check_piece_king(self, coords, color):
        """Check if a piece of in a given spot and of a given color is a king. Return false if no piece is found"""
        if color == "white":
            return (*coords, True) in self.white_positions
        else:
            return (*coords, True) in self.black_positions

    # https://stackoverflow.com/a/2191707
    def check_move_piece_capable(self, from_, to, color):
        """Check if the move is exactly one square diagonally"""
        if abs(to[0] - from_[0]) == 1:
            if self.check_piece_king(from_, color):
                return True
            else:
                if color == "white":
                    return to[1] == from_[1] + 1
                elif color == "black":
                    return to[1] == from_[1] - 1
        return False

    def check_capture(self, from_, to, color):
        """Check if a piece was captured for a given move. Return captured piece coordinates or None"""
        # captures can only happen if the player moved twice-diagonally
        if (abs(to[0]-from_[0]) != 2 or abs(to[1]-from_[1] != 2)):
            return None

        middle = (abs(to[0]-from_[0])//2, abs(to[1]-from_[1])//2)

        if color == "white" and self.check_piece_exists(middle, "black"):
            return middle
        elif color == "black" and self.check_piece_exists(middle, "white"):
            return middle
        return None

    def check_move_legal(self, from_, to, color):
        """Check if a move is legal. Return a boolean or coordinates of captured piece"""
        if self.check_move_out_of_bounds(from_, to):
            print("Illegal move! Final position is out of the bounds of the board")
            return False
        if not self.check_piece_exists(from_, color):
            print(
                "Illegal move! There is no piece on the starting position that belongs to the player")
            return False
        if self.check_piece_exists(to, "white") or self.check_piece_exists(to, "black"):
            print("Illegal move! Cannot move to position taken by another piece")
            return False
        capture = self.check_capture(from_, to, color)
        if capture == None:
            if self.check_move_piece_capable(from_, to, color):
                return True
            else:
                print('Illegal move!')
                return False
        return capture

    def make_move(self, from_, to, color):
        """Move a piece on the board and remove any captured pieces"""
        move_legal = self.check_move_legal(from_, to, color)
        if move_legal == False:
            return False
        capture = move_legal if type(move_legal) is tuple else None
        king = self.check_piece_king(from_, color)

        if (color == "white"):
            self.white_positions.remove((*from_, king))
            self.white_positions.append((*to, king))
            if (capture):
                captured_king = self.check_piece_king(capture, "black")
                self.black_positions.remove((*move_legal, captured_king))

        else:
            self.black_positions.remove((*from_, king))
            self.black_positions.append((*to, king))
            if (capture):
                captured_king = self.check_piece_king(capture, "white")
                self.white_positions.remove((*move_legal, captured_king))
        return True

    def print_board(self):
        """Print the board in the console"""
        print("   ", end="")
        for x in range(self.board_size):
            print(f"  {chr(ord('a')+x)} ", end="")
        print(" ")
        line = 0
        for y in range(self.board_size*4):
            for x in range(self.board_size):
                bg = "#" if x % 2 == (y//4) % 2 else " "
                checker = bg
                if ((x, y//4, False) in self.white_positions):
                    checker = "w"
                elif ((x, y//4, True) in self.white_positions):
                    checker = "W"
                elif ((x, y//4, False) in self.black_positions):
                    checker = "b"
                elif ((x, y//4, True) in self.black_positions):
                    checker = "B"

                if (x == 0):
                    if (line % 4 == 2):
                        print('{:3d}'.format(y//4), end="")
                    else:
                        print("   ", end="")

                match line % 4:
                    case 0:
                        print("+---", end="")
                    case 1 | 3:
                        print(f"|{3*bg}", end="")
                    case 2:
                        print(f"|{bg}{checker}{bg}", end="")
            if (line % 4 == 0):
                print("+")
            else:
                print(f"|{y//4}" if line % 4 == 2 else "|")
            line += 1
        print("   ", end="")
        for x in range(self.board_size):
            print("+---", end="")
        print("+\n   ", end="")
        for x in range(self.board_size):
            print(f"  {chr(ord('a')+x)}", end=" ")
        print()

# Ran first in the code

    def get_possible_moves(color):
        # toDo: get possible moves for single piece, then iterate through all pieces
        # if color == "white":
        #  for s
        pass

    def evaluate(self):
        white_score = 0
        black_score = 0

        for white_position in self.white_positions:
            if white_position[2]:
                white_score += 2
            else:
                white_score += 2

        for black_position in self.black_positions:
            if black_position[2]:
                black_score += 2
            else:
                black_score += 2

        return black_score - white_score

    def input_to_coordinates(self, input):
        pos_x = ord(input[0])-ord('a')
        pos_y = int(input[1::])
        return pos_x, pos_y

    def handle_player_move(self, color):
        has_moved = False
        while not has_moved:
            user_input = input('How do you want to move? (format: d6 e5)\n')
            regex = r"^[A-Za-z]\d+\s[A-Za-z]\d+$"
            match = re.search(regex, user_input)
            if not match:
                print('Invalid input, try again')
                continue
            [move_from, move_to] = user_input.split(' ')
            from_coordinates = self.input_to_coordinates(move_from)
            to_coordinates = self.input_to_coordinates(move_to)
            has_moved = self.make_move(
                from_coordinates, to_coordinates, color)
        self.print_board()


if __name__ == "__main__":
    game = Game(8)
    game.print_board()
    game.handle_player_move('black')
