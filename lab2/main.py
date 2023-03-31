"""
Program that plays draughts (checkers) with user on 8x8 board using min-max with alpha-beta prunning
"""

class Game:
  """Game"""

  def __init__(self, size):
    self.board_size = size
    self.white_positions = self.initialize_white()
    self.black_positions = self.initialize_black()
    print(self.white_positions)
    print(self.black_positions)
    self.check_move_piece_capable(1, 0, 1, 0, True)

  def initialize_white(self):
    white_positions = []
    for y_coordinate in range(3):
      for x_coordinate in range(self.board_size):
        if y_coordinate % 2 == 0:
          if x_coordinate % 2 == 1:
            white_positions.append((x_coordinate, y_coordinate, False))
        else:
          if x_coordinate % 2 == 0:
            white_positions.append((x_coordinate, y_coordinate, False))
    return white_positions

  def initialize_black(self):
    black_positions = []
    for y_coordinate in range(self.board_size - 3, self.board_size):
      for x_coordinate in range(self.board_size):
        if y_coordinate % 2 == 0:
          if x_coordinate % 2 == 1:
            black_positions.append((x_coordinate, y_coordinate, False))
        else:
          if x_coordinate % 2 == 0:
            black_positions.append((x_coordinate, y_coordinate, False))
    return black_positions

  def print_move_info(self, piece_x_coord, piece_y_coord, x_final, y_final):
    print("(piece_x_coordinate, piece_y_coordinate): " + (piece_x_coord, piece_y_coord))
    print("(x_final_coordinate, y_final_coordinate): " + (x_final, y_final))

  def check_move_out_of_bounds(self, piece_x_coord, piece_y_coord, x_final, y_final):
    error = False
    if x_final < 0:
      print("Illegal move! final x coordinate can't be below 0!")
      print_move_info(piece_x_coord, piece_y_coord, x_final, y_final)
      error = True
    if (x_final > self.board_size):
      print(f"Illegal move! final x coordinate can't be above board size! board_size: ${self.board_size}")
      print_move_info(piece_x_coord, piece_y_coord, x_final, y_final)
      error = True
    if y_final < 0:
      print("Illegal move! final y coordinate can't be below 0!")
      print_move_info(piece_x_coord, piece_y_coord, x_final, y_final)
      error = True
    if (y_final > self.board_size):
      print(f"Illegal move! final y coordinate can't be above board size! board_size: ${self.size}")
      print_move_info(piece_x_coord, piece_y_coord, x_final, y_final)
      error = True
    return error
    
  def check_spot_taken(self, piece_x_coord, piece_y_coord, x_final, y_final, player_color):
    error = False
    if player_color:
      if (x_final, y_final) in self.white_positions or (x_final, y_final) in self.white_positions:
        print("Illegal move! can't move into position taken by any other piece")
        print_move_info(piece_x_coord, piece_y_coord, x_final, y_final)
        error = True
    return error

  def check_piece_exists(self, piece_x_coord, piece_y_coord, player_color):
    error = False
    if player_color:
      if not (piece_x_coord, piece_y_coord) in self.white_positions:
        print("Illegal move! There is no piece on those coordinates or piece does not belong to white player")
        error = True
    elif not (piece_x_coord, piece_y_coord) in self.black_positons:
      print("Illegal move! There is no piece on those coordinates or piece does not belong to black player")
      error = True
    return error

  def check_move_diagonally(self, from, to, player_color, king):
    if not king: 
      if player_color:
        if to[0] == from[0] - 1 or to[0] == from[0] + 1:
          if to[1] == from[1] + 1:
            return False
      elif x_final == piece_x_coord - 1 or x_final == piece_x_coord + 1:
        if y_final == piece_y_coord - 1:
          return False
    if king:
      if player_color:
        if x_final == piece_x_coord - 1 or x_final == piece_x_coord + 1:
          return False
      elif x_final == piece_x_coord - 1 or x_final == piece_x_coord + 1:
        return False
    return True

  def check_piece_king(self, from, player_color):
    if player_color == "white":
      if (from[0], from[1], True) in self.white_positions:
        return True
    elif (from[0], from[1], True) in self.black_positions:
      return True
    return False

  # https://stackoverflow.com/a/2191707
  def check_move_piece_capable(self, from, to, player_color):
    error = True
    king = self.check_piece_king(from, player_color)
    error = self.check_move_diagonally(from, to, player_color, king)
    return error 

  def check_capture(self, from, to, player_color):
    capture = False 
    if player_color == "white":
      if (to[0] - 1, to[1] - 1) in self.black_positions or (t[0] + 1, to[1] - 1) in self.black_positions
        capture = True
    elif (to[0], to[1] - 1) in self.white_positions or (to[0] + 1, t0[1] - 1) in self.white_positions
        capture = True
    return capture
    
  def check_move_legal(self, from, to, player_color):
    if self.check_move_out_of_bounds(from, to):
      return False
    if self.check_piece_exists(from, to, player_color):
        return False
    if self.check_spot_taken(from, to, player_color):
      return False
    capture = self.check_capture(from, to, player_color)
    if not capture: 
      return self.check_move_piece_capable(from, to, player_color):
    
    return True

      
  
  def make_move(self, from, to, color):
    if(color == "white"):
      self.white_pieces.remove(from)
      self.white_pieces.append(to)
    else:
      self.black_pieces.remove(from)
      self.black_pieces.append(to)
   if not check_move_legal(piece_x_coord, piece_y_coord, x_final, y_final, player_color):
      return False    
    return True
    
	  
  def print_board(self):
    print("   ", end="")
    for x in range(self.board_size):
      print("  " + chr(97 + x), end=" ")
    print(" ")
    line = 0
    for y in range(self.board_size*4):
      for x in range(self.board_size):
        bg = "#" if x%2==(y//4)%2 else " "
        checker = bg
        if((x, y//4, False) in self.white_positions):
          checker = "w"
        elif((x, y//4, True) in self.white_positions):
          checker = "W"
        elif((x, y//4, False) in self.black_positions):
          checker = "b"
        elif((x, y//4, True) in self.black_positions):
          checker = "B"

        if(x==0):
          if(line%4==2):
            print('{:3d}'.format(y//4), end="")
          else:
            print("   ", end="")
        
        match line%4:
          case 0:
            print("+---", end="")
          case 1 | 3:
            print("|" + 3*bg, end="")
          case 2:
            print("|" + bg + checker + bg, end="")
      if(line%4==0):
        print("+")
      else:
        print("|", end=f"{y//4}\n" if line%4==2 else "\n")
      line+=1
    print("   ", end="")
    for x in range(self.board_size):
      print("+---", end="")
    print("+\n   ", end="")
    for x in range(self.board_size):
      print("  " + chr(97 + x), end=" ")
    print()
    
# Ran first in the code
if __name__ == "__main__":
  game = Game(8)
  game.print_board()
  