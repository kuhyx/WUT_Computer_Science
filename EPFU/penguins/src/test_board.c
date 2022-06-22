#include "printing.c"
#include "generate.c"
#include "game_struct.h"

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int main()
{
    GameState Game;
    Game.board_height = 10;
    Game.board_width = 10;

    Game.board = allocateMemory(Game);

    Game.board = randomizeFields(Game);
    Game.board[5][5].player_no = 0;
    Game.board[5][5].fish_no = 0;
    printBoard(Game);
    return 0;
}
