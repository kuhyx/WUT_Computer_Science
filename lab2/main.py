"""
Program that plays draughts (checkers) with user on 8x8 board using min-max with alpha-beta pruning
"""
import re
import copy
import math


class Game:
    """Game"""

    def __init__(self, size):
        self.board_size = size
        self.white_positions = self.initialize_white()
        self.black_positions = self.initialize_black()

    def initialize_white(self):
        """Initialize white pieces"""
        white_positions = []
        for y_coordinate in range(math.floor((self.board_size - 2) / 2)):
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
        for y_coordinate in range(self.board_size - math.floor((self.board_size - 2) / 2), self.board_size):
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

    def check_move_out_of_bounds(self, to_):
        """Check if the move destination is out of the bounds of the board"""
        if to_[0] < 0 or to_[0] > self.board_size - 1:
            # print(f"Illegal move! Final x coordinate must be between 0 and {self.board_size-1}!")
            return True
        if to_[1] < 0 or to_[1] > self.board_size - 1:
            # print(f"Illegal move! Final y coordinate must be between 0 and {self.board_size-1}!")
            return True
        return False

    def check_piece_exists(self, coords, color):
        """Check if a piece of given color exists at a given spot"""
        if color == "white":
            if any(piece in self.white_positions for piece in ((*coords, False), (*coords, True))):
                return True
        else:
            if any(piece in self.black_positions for piece in ((*coords, False), (*coords, True))):
                return True
        return False

    def check_piece_king(self, coords, color):
        """Check if a piece of in a given spot and of a given color is a king.
        Return false if no piece is found"""
        if color == "white":
            return (*coords, True) in self.white_positions
        if color == "black":
            return (*coords, True) in self.black_positions
        return False

    # https://stackoverflow.com/a/2191707
    def check_move_piece_capable(self, from_, to_, color):
        """Check if the move is exactly one square diagonally"""
        if abs(to_[0] - from_[0]) == 1:
            if self.check_piece_king(from_, color):
                return True
            if color == "white":
                return to_[1] == from_[1] + 1
            if color == "black":
                return to_[1] == from_[1] - 1
        return False

    def check_capture(self, from_, to_, color):
        """Check if a piece was captured for a given move.
        Return captured piece coordinates or None"""
        # captures can only happen if the player moved twice-diagonally

        if (abs(to_[0]-from_[0]) != 2 or abs(to_[1]-from_[1]) != 2):
            return None

        middle = (abs(to_[0]+from_[0])//2, abs(to_[1]+from_[1])//2)

        if color == "white" and self.check_piece_exists(middle, "black"):
            return middle
        if color == "black" and self.check_piece_exists(middle, "white"):
            return middle
        return None

    def check_move_legal(self, from_, to_, color, give_feedback=False):
        """Check if a move is legal. Return a boolean or coordinates of captured piece"""
        if self.check_move_out_of_bounds(to_):
            if give_feedback:
                print("Illegal move! Final position is out of the bounds of the board")
            return False
        if not self.check_piece_exists(from_, color):
            if give_feedback:
                print(
                    "Illegal move! There is no piece on the "
                    "starting position that belongs to the player")
            return False
        if self.check_piece_exists(to_, "white") or self.check_piece_exists(to_, "black"):
            if give_feedback:
                print("Illegal move! Cannot move to position taken by another piece")
            return False
        capture = self.check_capture(from_, to_, color)
        if capture is None:
            if self.check_move_piece_capable(from_, to_, color):
                return True
            if give_feedback:
                print('Illegal move! You can only move diagonally')
            return False
        return capture

    def make_move(self, from_, to_, color):
        """Move a piece on the board and remove any captured pieces"""
        move_legal = self.check_move_legal(from_, to_, color)
        if move_legal is False:
            return False
        capture = move_legal if isinstance(move_legal, tuple) else None
        king = self.check_piece_king(from_, color)

        if color == "white":
            self.white_positions.remove((*from_, king))
            if capture:
                captured_king = self.check_piece_king(capture, "black")
                self.black_positions.remove((*move_legal, captured_king))
            if to_[1] == self.board_size-1:
                self.white_positions.append((*to_, True))
            else:
                self.white_positions.append((*to_, king))

        else:
            self.black_positions.remove((*from_, king))
            if capture:
                captured_king = self.check_piece_king(capture, "white")
                self.white_positions.remove((*move_legal, captured_king))
            if to_[1] == 0:
                self.black_positions.append((*to_, True))
            else:
                self.black_positions.append((*to_, king))

        return True

    def print_board(self, rotate=False):
        """Print the board in the console"""

        def print_letters():
            """Print the letters above or under the board"""
            print("   ", end="")
            for col in range(self.board_size):
                if rotate:
                    print(f"  {chr(ord('a')+self.board_size-1-col)}", end=" ")
                else:
                    print(f"  {chr(ord('a')+col)}", end=" ")

        def get_square_code(pos, background):
            """Return the code of a given square on the board"""
            if (*pos, False) in self.white_positions:
                return "w"
            if (*pos, True) in self.white_positions:
                return "W"
            if (*pos, False) in self.black_positions:
                return "b"
            if (*pos, True) in self.black_positions:
                return "B"
            return background

        print_letters()
        print(" ")

        row_range = range(
            self.board_size*4) if not rotate else reversed(range(self.board_size*4))
        line = 0
        for row in row_range:
            for col in range(self.board_size):
                background = "#" if (col % 2 == (row//4) % 2) != rotate\
                    else " "
                checker = get_square_code((col, row//4), background)\
                    if not rotate else get_square_code((self.board_size-1-col, row//4), background)

                if col == 0:
                    if line % 4 == 2:
                        print(f"{row//4:3d}", end="")
                    else:
                        print("   ", end="")

                match line % 4:
                    case 0:
                        print("+---", end="")
                    case 1 | 3:
                        print(f"|{3*background}", end="")
                    case 2:
                        print(f"|{background}{checker}{background}", end="")
            if line % 4 == 0:
                print("+")
            else:
                print(f"|{row//4}" if line % 4 == 2 else "|")
            line += 1
        print("   ", end="")
        for col in range(self.board_size):
            print("+---", end="")
        print("+")
        print_letters()
        print()

# Ran first in the code
    def get_possible_moves_capture(self, from_, color):
        """Return all possible captures for a piece"""
        # all capturing moves:
        legal_moves = []
        move_down_left_two = (from_[0] + 2, from_[1] - 2)
        move_down_right_two = (from_[0] + 2, from_[1] + 2)
        move_up_left_two = (from_[0] - 2, from_[1] - 2)
        move_up_right_two = (from_[0] - 2, from_[1] + 2)
        if self.check_move_legal(from_, move_down_left_two, color) is not False:
            legal_moves.append((from_, move_down_left_two))
        if self.check_move_legal(from_, move_down_right_two, color) is not False:
            legal_moves.append((from_, move_down_right_two))
        if self.check_move_legal(from_, move_up_left_two, color) is not False:
            legal_moves.append((from_, move_up_left_two))
        if self.check_move_legal(from_, move_up_right_two, color) is not False:
            legal_moves.append((from_, move_up_right_two))
        return legal_moves

    def get_possible_moves_non_capture(self, from_, color):
        """Return all possible moves that are not captures for a piece"""
        # all non-capturing moves
        legal_moves = []
        move_down_left_one = (from_[0] + 1, from_[1] - 1)
        move_down_right_one = (from_[0] + 1, from_[1] + 1)
        move_up_left_one = (from_[0] - 1, from_[1] - 1)
        move_up_right_one = (from_[0] - 1, from_[1] + 1)
        if self.check_move_legal(from_, move_down_left_one, color) is not False:
            legal_moves.append((from_, move_down_left_one))
        if self.check_move_legal(from_, move_down_right_one, color) is not False:
            legal_moves.append((from_, move_down_right_one))
        if self.check_move_legal(from_, move_up_left_one, color) is not False:
            legal_moves.append((from_, move_up_left_one))
        if self.check_move_legal(from_, move_up_right_one, color) is not False:
            legal_moves.append((from_, move_up_right_one))
        return legal_moves

    def get_possible_moves(self, color):
        """Return all possible moves for a given piece color"""
        legal_moves = []
        captures = []
        if color == "white":
            for white_position in self.white_positions:
                # print((white_position[0], white_position[1]))
                legal_moves += self.get_possible_moves_non_capture(
                    (white_position[0], white_position[1]), color)
                captures += self.get_possible_moves_capture(
                    (white_position[0], white_position[1]), color)
        elif color == "black":
            for black_position in self.black_positions:
                legal_moves += self.get_possible_moves_non_capture(
                    (black_position[0], black_position[1]), color)
                captures += self.get_possible_moves_capture(
                    (black_position[0], black_position[1]), color)

        if len(captures) > 0:
            return (captures, True)
        return (legal_moves + captures, False)

    def alpha_beta(self, depth, alpha_beta, color, current_color=None):
        """Do alpha beta pruning for given parameters
        and return the best move and its evaluated points"""
        if current_color is None:
            current_color = color

        if depth == 0:
            return self.evaluate(color), None

        alpha, beta = alpha_beta
        opposite_color = 'white' if current_color == 'black' else 'black'
        if current_color == color:
            max_eval = float('-inf')
            best_move = None

            for move in self.get_possible_moves(current_color)[0]:
                new_state = copy.deepcopy(self)
                new_state.make_move(*move, current_color)
                eval_, _ = new_state.alpha_beta(
                    depth-1, alpha_beta, color, opposite_color)

                if eval_ > max_eval:
                    max_eval = eval_
                    best_move = move

                alpha = max(alpha, eval_)

                if alpha >= beta:
                    break

            return max_eval, best_move

        if opposite_color == color:
            min_eval = float('inf')
            best_move = None

            for move in self.get_possible_moves(current_color)[0]:
                new_state = copy.deepcopy(self)
                new_state.make_move(*move, current_color)
                eval_, _ = new_state.alpha_beta(
                    depth-1, alpha_beta, color, opposite_color)

                if eval_ < min_eval:
                    min_eval = eval_
                    best_move = move

                beta = min(beta, eval_)

                if beta <= alpha:
                    break

            return min_eval, best_move
        return None

    def evaluate(self, color):
        """Evaluates the state of the board for a given color"""
        white_score = 0
        black_score = 0

        for white_position in self.white_positions:
            if white_position[2]:
                white_score += 10
            else:
                white_score += 5

        for black_position in self.black_positions:
            if black_position[2]:
                black_score += 10
            else:
                black_score += 5

        return white_score - black_score if color == 'white' else black_score - white_score

    def input_to_coordinates(self, user_input):
        """Change input from a1 form to tuple form"""
        pos_x = ord(user_input[0])-ord('a')
        pos_y = int(user_input[1::])
        return pos_x, pos_y

    def handle_player_move(self, color):
        """Prompt player to move, validate their input and make move"""
        has_moved = False
        possible_moves = self.get_possible_moves(color)[0]
        while not has_moved:
            user_input = input(
                f'You are {color}. How do you want to move? (format: d6 e5)\n')
            regex = r"^[a-z]\d+\s[a-z]\d+$"
            match = re.search(regex, user_input)
            if not match:
                print('Invalid input, try again')
                continue
            [move_from, move_to] = user_input.split(' ')
            from_coordinates = self.input_to_coordinates(move_from)
            to_coordinates = self.input_to_coordinates(move_to)

            if not (from_coordinates, to_coordinates) in possible_moves:
                legal_no_captures = self.check_move_legal(
                    from_coordinates, to_coordinates, color, True)
                if legal_no_captures:
                    print("Invalid move! You can capture a piece")
                continue

            has_moved = self.make_move(from_coordinates, to_coordinates, color)
        self.print_board(color == 'white')

    def start_game(self, player_color='black'):
        """Start the main loop of the game"""
        if player_color not in ('black', 'white'):
            print('Invalid color! Color can be black or white')
            return
        ai_color = 'black' if player_color == 'white' else 'white'

        game.print_board(player_color == 'white')
        if player_color == 'white':
            game.handle_player_move('white')
        algorithm_depth = 5
        while True:
            ai_turn = True
            while ai_turn:
                possible_moves_ai = game.get_possible_moves(ai_color)
                if len(possible_moves_ai[0]) == 0:
                    print(f'Game over, {player_color} wins')
                    return
                _, ai_move = game.alpha_beta(algorithm_depth, (5, 10), ai_color)
                game.make_move(*ai_move, ai_color)
                print(
                    "AI's move: "
                    f"{chr(ord('a')+ai_move[0][0])}{ai_move[0][1]} "
                    f"{chr(ord('a')+ai_move[1][0])}{ai_move[1][1]}")
                game.print_board(player_color == 'white')
                ai_turn = game.get_possible_moves(ai_color)[1] and possible_moves_ai[1]
            player_turn = True
            while player_turn:
                possible_moves_player = game.get_possible_moves(player_color)
                if len(possible_moves_player[0]) == 0:
                    print(f'Game over, {ai_color} wins')
                    return
                game.handle_player_move(player_color)
                player_turn = game.get_possible_moves(player_color)[1] and possible_moves_player[1]


# Ran first in the code
if __name__ == "__main__":
    game = Game(8)
    game.start_game('black')
