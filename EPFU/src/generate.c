#include "game_struct.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

Field** allocateMemory(GameState Game)
{
    //This for loop assigns pointers from our array of pointer
	// to the beginning of memory blocks with size of Field struct
	// There are board_width number of smaller memory blocks
	// And board_height number of bigger memory blocks

    Game.board = (Field **)malloc(Game.board_height * sizeof(Field*));
    for(int i = 0; i < Game.board_height; i++)
    {
        Game.board[i] = (Field*)malloc(Game.board_width*sizeof(Field));
    }
    return Game.board;
}

Field** randomizeFields(GameState Game)
{
    srand(time(0));

    for(int i = 0; i < Game.board_height; i++)
    {
        for(int j = 0; j < Game.board_width; j++)
        {
            Game.board[i][j].fish_no = rand() % 3 + 1;
            //upside of this method
            // is that it does not change the way we refer to this array
            // later on in the program

            Game.board[i][j].player_no = 0;

        }
    }
    return Game.board;
}

char** generateCommandLine(GameState Game, int argc)
{
    int i;
    Game.command_line = (char **)malloc(argc * sizeof(char*));
    for(i = 0; i < argc; i++)
    {
        Game.command_line[i] = (char*)malloc(30 *sizeof(char));
    }

    return Game.command_line;
}
