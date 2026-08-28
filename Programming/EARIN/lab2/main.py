#!/usr/bin/env python3
"""Play draughts against a min-max bot with alpha-beta pruning, on 8x8."""

import copy
import logging
import math
import re
import sys

# A capture jumps exactly two squares, and the board is drawn four text rows
# per board row, with the rank label on the third of them.
CAPTURE_DISTANCE = 2
ROWS_PER_SQUARE = 4
LABEL_ROW = 2
ARGV_WITH_COLOUR = 2
ARGV_WITH_DEPTH = 3
logger = logging.getLogger(__name__)


class Game:
    """Game."""

    def __init__(self, size: int) -> None:
        """Set up an empty board of the given size and place both armies."""
        self.board_size = size
        self.white_positions = self.initialize_white()
        self.black_positions = self.initialize_black()

    def initialize_white(self) -> set[tuple[int, int, bool]]:
        """Initialize white pieces."""
        white_positions = []
        for y_coordinate in range(math.floor((self.board_size - 2) / 2)):
            for x_coordinate in range(self.board_size):
                if y_coordinate % 2 == 0:
                    if x_coordinate % 2 == 1:
                        white_positions.append((x_coordinate, y_coordinate, False))
                elif x_coordinate % 2 == 0:
                    white_positions.append((x_coordinate, y_coordinate, False))
        return white_positions

    def initialize_black(self) -> set[tuple[int, int, bool]]:
        """Initialize black pieces."""
        black_positions = []
        for y_coordinate in range(
            self.board_size - math.floor((self.board_size - 2) / 2), self.board_size
        ):
            for x_coordinate in range(self.board_size):
                if y_coordinate % 2 == 0:
                    if x_coordinate % 2 == 1:
                        black_positions.append((x_coordinate, y_coordinate, False))
                elif x_coordinate % 2 == 0:
                    black_positions.append((x_coordinate, y_coordinate, False))
        return black_positions

    def check_move_out_of_bounds(self, to_: tuple[int, int]) -> bool:
        """Check if the move destination is out of the bounds of the board."""
        if to_[0] < 0 or to_[0] > self.board_size - 1:
            return True
        return bool(to_[1] < 0 or to_[1] > self.board_size - 1)

    def check_piece_exists(self, coords: tuple[int, int], color: str) -> bool:
        """Check if a piece of given color exists at a given spot."""
        if color == "white":
            if any(
                piece in self.white_positions
                for piece in ((*coords, False), (*coords, True))
            ):
                return True
        elif any(
            piece in self.black_positions
            for piece in ((*coords, False), (*coords, True))
        ):
            return True
        return False

    def check_piece_king(self, coords: tuple[int, int], color: str) -> bool:
        """Check if a piece of in a given spot and of a given color is a king.

        Return false if no piece is found.
        """
        if color == "white":
            return (*coords, True) in self.white_positions
        if color == "black":
            return (*coords, True) in self.black_positions
        return False

    # https://stackoverflow.com/a/2191707
    def check_move_piece_capable(
        self, from_: tuple[int, int], to_: tuple[int, int], color: str
    ) -> bool:
        """Check if the move is exactly one square diagonally."""
        if abs(to_[0] - from_[0]) == 1:
            if self.check_piece_king(from_, color):
                return True
            if color == "white":
                return to_[1] == from_[1] + 1
            if color == "black":
                return to_[1] == from_[1] - 1
        return False

    def check_capture(
        self, from_: tuple[int, int], to_: tuple[int, int], color: str
    ) -> tuple[int, int] | None:
        """Check if a piece was captured for a given move.

        Return captured piece coordinates or None.
        """
        # captures can only happen if the player moved twice-diagonally

        if (
            abs(to_[0] - from_[0]) != CAPTURE_DISTANCE
            or abs(to_[1] - from_[1]) != CAPTURE_DISTANCE
        ):
            return None

        middle = (abs(to_[0] + from_[0]) // 2, abs(to_[1] + from_[1]) // 2)

        if color == "white" and self.check_piece_exists(middle, "black"):
            return middle
        if color == "black" and self.check_piece_exists(middle, "white"):
            return middle
        return None

    def check_move_legal(
        self,
        from_: tuple[int, int],
        to_: tuple[int, int],
        color: str,
        *,
        give_feedback: bool = False,
    ) -> bool | tuple[int, int]:
        """Check whether a move is legal.

        Returns False when it is not, True when it is a plain move, and the
        coordinates of the captured piece when it is a capture.
        """
        if self.check_move_out_of_bounds(to_):
            if give_feedback:
                logger.info(
                    "Illegal move! Final position is out of the bounds of the board"
                )
            return False
        if not self.check_piece_exists(from_, color):
            if give_feedback:
                logger.info(
                    "Illegal move! There is no piece on the starting position "
                    "that belongs to the player"
                )
            return False
        if self.check_piece_exists(to_, "white") or self.check_piece_exists(
            to_, "black"
        ):
            if give_feedback:
                logger.info(
                    "Illegal move! Cannot move to position taken by another piece"
                )
            return False
        capture = self.check_capture(from_, to_, color)
        if capture is None:
            if self.check_move_piece_capable(from_, to_, color):
                return True
            if give_feedback:
                logger.info("Illegal move! You can only move diagonally")
            return False
        return capture

    def make_move(
        self, from_: tuple[int, int], to_: tuple[int, int], color: str
    ) -> bool:
        """Move a piece on the board and remove any captured pieces."""
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
            if to_[1] == self.board_size - 1:
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

    def _print_letters(self, *, rotate: bool) -> None:
        """Write the file letters that run above and below the board."""
        sys.stdout.write("   ")
        for col in range(self.board_size):
            letter = self.board_size - 1 - col if rotate else col
            sys.stdout.write(f"  {chr(ord('a') + letter)} ")

    def _square_code(self, pos: tuple[int, int], background: str) -> str:
        """Return the one-character code of a square: piece, king, or empty."""
        if (*pos, False) in self.white_positions:
            return "w"
        if (*pos, True) in self.white_positions:
            return "W"
        if (*pos, False) in self.black_positions:
            return "b"
        if (*pos, True) in self.black_positions:
            return "B"
        return background

    def _print_cell(self, row: int, col: int, line: int, *, rotate: bool) -> None:
        """Write the one text row of one square."""
        background = "#" if (col % 2 == (row // 4) % 2) != rotate else " "
        pos = (self.board_size - 1 - col, row // 4) if rotate else (col, row // 4)
        checker = self._square_code(pos, background)

        if col == 0:
            sys.stdout.write(
                f"{row // 4:3d}" if line % ROWS_PER_SQUARE == LABEL_ROW else "   "
            )

        match line % ROWS_PER_SQUARE:
            case 0:
                sys.stdout.write("+---")
            case 1 | 3:
                sys.stdout.write(f"|{3 * background}")
            case 2:
                sys.stdout.write(f"|{background}{checker}{background}")

    def print_board(self, *, rotate: bool = False) -> None:
        """Print the board in the console.

        The three helpers below used to be nested functions here, which is
        what put this method at C901 17.
        """
        self._print_letters(rotate=rotate)
        sys.stdout.write(" \n")

        row_range = (
            range(self.board_size * 4)
            if not rotate
            else reversed(range(self.board_size * 4))
        )

        for line, row in enumerate(row_range):
            for col in range(self.board_size):
                self._print_cell(row, col, line, rotate=rotate)
            if line % ROWS_PER_SQUARE == 0:
                sys.stdout.write("+\n")
            else:
                sys.stdout.write(
                    f"|{row // ROWS_PER_SQUARE}\n"
                    if line % ROWS_PER_SQUARE == LABEL_ROW
                    else "|\n"
                )
        sys.stdout.write("   ")
        for _col in range(self.board_size):
            sys.stdout.write("+---")
        sys.stdout.write("+\n")
        self._print_letters(rotate=rotate)
        sys.stdout.write("\n")

    # Ran first in the code
    def get_possible_moves_capture(
        self, from_: tuple[int, int], color: str
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Return all possible captures for a piece."""
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

    def get_possible_moves_non_capture(
        self, from_: tuple[int, int], color: str
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Return all possible moves that are not captures for a piece."""
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

    def get_possible_moves(
        self, color: str
    ) -> tuple[list[tuple[tuple[int, int], tuple[int, int]]], bool]:
        """Return all possible moves for a given piece color."""
        legal_moves = []
        captures = []
        if color == "white":
            for white_position in self.white_positions:
                legal_moves += self.get_possible_moves_non_capture(
                    (white_position[0], white_position[1]), color
                )
                captures += self.get_possible_moves_capture(
                    (white_position[0], white_position[1]), color
                )
        elif color == "black":
            for black_position in self.black_positions:
                legal_moves += self.get_possible_moves_non_capture(
                    (black_position[0], black_position[1]), color
                )
                captures += self.get_possible_moves_capture(
                    (black_position[0], black_position[1]), color
                )

        if len(captures) > 0:
            return (captures, True)
        return (legal_moves + captures, False)

    def _search_branch(
        self,
        depth: int,
        alpha_beta: tuple[float, float],
        color: str,
        current_color: str,
        *,
        maximising: bool,
    ) -> tuple[float, tuple[tuple[int, int], tuple[int, int]] | None]:
        """One half of the alpha-beta search.

        The maximising and minimising halves were byte-for-byte mirror images
        of each other, which is what made alpha_beta too complex to pass C901.
        """
        alpha, beta = alpha_beta
        opposite_color = "white" if current_color == "black" else "black"
        best_eval = float("-inf") if maximising else float("inf")
        best_move = None

        for move in self.get_possible_moves(current_color)[0]:
            new_state = copy.deepcopy(self)
            new_state.make_move(*move, current_color)
            eval_, _ = new_state.alpha_beta(
                depth - 1, alpha_beta, color, opposite_color
            )

            if (eval_ > best_eval) if maximising else (eval_ < best_eval):
                best_eval = eval_
                best_move = move

            if maximising:
                alpha = max(alpha, eval_)
            else:
                beta = min(beta, eval_)

            if alpha >= beta:
                break

        return best_eval, best_move

    def alpha_beta(
        self,
        depth: int,
        alpha_beta: tuple[float, float],
        color: str,
        current_color: str | None = None,
    ) -> tuple[float, tuple[tuple[int, int], tuple[int, int]] | None]:
        """Search with alpha-beta pruning; return the best move and its score."""
        if current_color is None:
            current_color = color
        if depth == 0:
            return self.evaluate(color), None
        return self._search_branch(
            depth,
            alpha_beta,
            color,
            current_color,
            maximising=current_color == color,
        )

    def evaluate(self, color: str) -> float:
        """Score the board from the given colour's point of view."""
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

        return (
            white_score - black_score if color == "white" else black_score - white_score
        )

    def input_to_coordinates(self, user_input: str) -> tuple[int, int]:
        """Change input from a1 form to tuple form."""
        pos_x = ord(user_input[0]) - ord("a")
        pos_y = int(user_input[1::])
        return pos_x, pos_y

    def handle_player_move(self, color: str) -> None:
        """Prompt player to move, validate their input and make move."""
        has_moved = False
        possible_moves = self.get_possible_moves(color)[0]
        while not has_moved:
            user_input = input(
                f"You are {color}. How do you want to move? (format: d6 e5)\n"
            )
            regex = r"^[a-z]\d+\s[a-z]\d+$"
            match = re.search(regex, user_input)
            if not match:
                logger.info("Invalid input, try again")
                continue
            [move_from, move_to] = user_input.split(" ")
            from_coordinates = self.input_to_coordinates(move_from)
            to_coordinates = self.input_to_coordinates(move_to)

            if (from_coordinates, to_coordinates) not in possible_moves:
                legal_no_captures = self.check_move_legal(
                    from_coordinates, to_coordinates, color, give_feedback=True
                )
                if legal_no_captures:
                    logger.info("Invalid move! You can capture a piece")
                continue

            has_moved = self.make_move(from_coordinates, to_coordinates, color)
        self.print_board(rotate=color == "white")

    def start_game(self, player_color: str = "black", algorithm_depth: int = 5) -> None:
        """Start the main loop of the game."""
        if player_color not in ("black", "white"):
            logger.info("Invalid color! Color can be black or white")
            return
        ai_color = "black" if player_color == "white" else "white"

        game.print_board(rotate=player_color == "white")
        if player_color == "white":
            game.handle_player_move("white")
        while True:
            ai_turn = True
            while ai_turn:
                possible_moves_ai = game.get_possible_moves(ai_color)
                if len(possible_moves_ai[0]) == 0:
                    logger.info("Game over, %s wins", player_color)
                    return
                _, ai_move = game.alpha_beta(algorithm_depth, (5, 10), ai_color)
                if ai_move is None:
                    logger.info("Game over, %s wins", player_color)
                    return
                game.make_move(ai_move[0], ai_move[1], ai_color)
                logger.info(
                    "AI's move: %s%s %s%s",
                    chr(ord("a") + ai_move[0][0]),
                    ai_move[0][1],
                    chr(ord("a") + ai_move[1][0]),
                    ai_move[1][1],
                )
                game.print_board(rotate=player_color == "white")
                ai_turn = game.get_possible_moves(ai_color)[1] and possible_moves_ai[1]
            player_turn = True
            while player_turn:
                possible_moves_player = game.get_possible_moves(player_color)
                if len(possible_moves_player[0]) == 0:
                    logger.info("Game over, %s wins", ai_color)
                    return
                game.handle_player_move(player_color)
                player_turn = (
                    game.get_possible_moves(player_color)[1]
                    and possible_moves_player[1]
                )

    def ai_turn(
        self,
        ai_color: str,
        algorithm_depth: int,
        possible_moves_ai: list[object],
        *,
        print_info: bool = True,
    ) -> bool:
        """Calculate ai move and makes it."""
        if len(possible_moves_ai) == 0:
            if print_info:
                logger.info("Game over, %s loses", ai_color)
            return True
        _, ai_move = game.alpha_beta(algorithm_depth, (5, 10), ai_color)
        if ai_move is None:
            ai_move = possible_moves_ai[0]
        game.make_move(ai_move[0], ai_move[1], ai_color)
        if print_info:
            logger.info(
                "AI's move: %s%s %s%s",
                chr(ord("a") + ai_move[0][0]),
                ai_move[0][1],
                chr(ord("a") + ai_move[1][0]),
                ai_move[1][1],
            )
            game.print_board(rotate=True)
        return False

    def auto_game(self, white_depth: int, black_depth: int) -> str:
        """Auto game mode between two bots."""
        game_turn = 0
        max_turns = 250
        while game_turn < max_turns:
            bot_white_turn = True
            while bot_white_turn:
                possible_moves_ai = game.get_possible_moves("white")
                if self.ai_turn(
                    "white", white_depth, possible_moves_ai[0], print_info=False
                ):
                    return "white"
                bot_white_turn = (
                    game.get_possible_moves("white")[1] and possible_moves_ai[1]
                )
            bot_black_turn = True
            while bot_black_turn:
                possible_moves_ai = game.get_possible_moves("black")
                if self.ai_turn(
                    "black", black_depth, possible_moves_ai[0], print_info=False
                ):
                    return "black"
                bot_black_turn = (
                    game.get_possible_moves("black")[1] and possible_moves_ai[1]
                )
            game_turn += 1
        if game_turn >= max_turns:
            logger.info("Game ended after %s turns!", max_turns)
            return ""
        return ""


def auto_simulation(white_depth: int, black_depth: int, iterations: int) -> None:
    """Run iterations amount of simulations."""
    logger.info(
        "Running %s simulations with\n        white depth = %s,black depth = %s",
        iterations,
        white_depth,
        black_depth,
    )
    white_wins = 0
    black_wins = 0
    white_pieces_captured = 0
    black_pieces_captured = 0
    current_iteration = 0
    while current_iteration < iterations:
        result = game.auto_game(white_depth, black_depth)
        if result == "white":
            black_wins += 1
        if result == "black":
            white_wins += 1
        if result == "":
            break
        white_pieces_captured += 16 - len(game.white_positions)
        black_pieces_captured += 16 - len(game.black_positions)
        current_iteration += 1
    logger.info(
        "White wins = %s, Black wins = %s,\n        white pieces captured in "
        "total = %s,\n        black pieces captured in total = %s",
        white_wins,
        black_wins,
        white_pieces_captured,
        black_pieces_captured,
    )
    logger.info("")


def print_help() -> None:
    """Print help."""
    logger.info(
        "python main.py [algorithm_depth] - play the game against the bot as "
        "black,\n        if no algorithm depth is specified the default (5) will "
        "be set\n\npython main.py -h --help print this prompt\npython main.py -t "
        "--test [max_white_depth] [max_black_depth] non interactive\n(does not "
        "print moves) for testing how different bot depth play against eachother,"
        "\nif depths are not provided default value of 5 is set\ncompares "
        "heuristic speed and path length\npython main.py -w --white "
        "[algorithm_depth] play as white pieces,\nif no algorithm depth is "
        "specified the default (5) will be set\npython main.py -b --black "
        "[algorithm_depth] play as black pieces,\nif no algorithm depth is "
        "specified the default (5) will be set\n"
    )


def default(color: str = "black", algorithm_depth: int = 5) -> None:
    """Play one game against the bot, as black by default."""
    game.start_game(color, algorithm_depth)


# Ran first in the code
if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    game = Game(8)
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
            sys.exit()
        if sys.argv[1] == "-t" or sys.argv[1] == "--test":
            MAX_WHITE_DEPTH = 4
            MAX_BLACK_DEPTH = 4
            if len(sys.argv) > ARGV_WITH_COLOUR:
                MAX_WHITE_DEPTH = int(sys.argv[2])
            if len(sys.argv) > ARGV_WITH_DEPTH:
                MAX_BLACK_DEPTH = int(sys.argv[3])
            for i in range(MAX_WHITE_DEPTH + 1):
                for j in range(MAX_BLACK_DEPTH + 1):
                    game = Game(8)
                    auto_simulation(i, j, 10)
            sys.exit()
        if sys.argv[1] == "-w" or sys.argv[1] == "--white":
            ALGORITHM_DEPTH = 5
            if len(sys.argv) > ARGV_WITH_COLOUR:
                ALGORITHM_DEPTH = int(sys.argv[2])
            default("white", ALGORITHM_DEPTH)
            sys.exit()
        if sys.argv[1] == "-b" or sys.argv[1] == "--black":
            ALGORITHM_DEPTH = 5
            if len(sys.argv) > ARGV_WITH_COLOUR:
                ALGORITHM_DEPTH = int(sys.argv[2])
            default("black", ALGORITHM_DEPTH)
            sys.exit()
        if len(sys.argv) > 1:
            default("black", int(sys.argv[1]))
    default()
