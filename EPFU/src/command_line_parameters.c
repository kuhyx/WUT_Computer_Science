#include "game_struct.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include "handling_files.c"

int numberOfPenguins(GameState Game, int command_number)
{
    char number[10];
    int len = strlen(Game.command_line[command_number]);
    int j = 0;
    for(int i = 9; i < len; i++)
    {
        number[j] = Game.command_line[command_number][i];
        j++;
    }
    Game.penguins = atoi(number);
    return Game.penguins;
}

int isItBoardParameter(GameState Game, int command_number)
{
    int len = strlen(Game.command_line[command_number]);
    int j = 0, i;
    char extension[4] = "";
    int answer = 0;
    memset(extension, 0, strlen(extension));
    for(i = len - 4; i < len; i++)
    {
        extension[j] = Game.command_line[command_number][i];
        j++;
    }
    if(!strcmp(extension, ".txt"))
    {
        answer = 1;
    }else answer = 0;
    return answer;
}

char** handlingParameters(int argc, char *argv[], GameState Game)
{
    int i;
    for(i = 1; i < argc; i++)
    {
         strcpy(Game.command_line[i - 1], argv[i]);
    }
    for(i = 0; i < argc - 1; i++)
    {
          printf("%s\n", Game.command_line[i]);
    }
    return Game.command_line;
}

int checkParameterType(GameState *Game, int command_number)
{
    if(!strcmp(Game -> command_line[command_number], "phase=placement"))  // Checks if the command line parameters says phase=placement
    {
        Game -> phase = 1;
        printf("Game phase is placement!\n");
        return 1;
    }else if(!strcmp(Game -> command_line[command_number], "phase=movement")) // Checks if the command line parameters says phase=movement
    {
        Game -> phase = 2;
        printf("Game phase is movement!\n");
        return 1;
    }else if(!strncmp(Game -> command_line[command_number], "penguins=", 9)) // Checks if the command line parameters says penguins
    {
        Game -> penguins = numberOfPenguins(*Game, command_number);
        Game -> penguins_from_command = 1;
        printf("There are %d penguins\n", Game -> penguins);
        return 2;
    }else if(isItBoardParameter(*Game, command_number))  // // Checks if the command line parameters gives us board file name
    {
        printf("It is a board file!\n");
        if(Game -> file_type == 0)  // First file is input board file
        {
            printf("It is an input board file!\n");
            Game -> file_type = Game -> file_type + 1;
            printf("%s", Game -> command_line[command_number]);
            Game -> input_board_command_number = command_number;
            Game -> input_board = fopen(Game -> command_line[command_number], "r+");
            return 3;
        }else if(Game -> file_type == 1) // Second file is output board file
        {
            printf("It is an output board file!\n");
            if(!strcmp(Game -> command_line[Game -> input_board_command_number], Game -> command_line[command_number]))  // If the input and board file are the same
                // then we open it in r+ mode
            {
                Game -> output_board = fopen(Game -> command_line[command_number], "r+");
            }  // Else we open it in w mode
            else
            {
                Game -> output_board = fopen(Game -> command_line[command_number], "w");
            }
            Game -> file_type = Game -> file_type + 1;
            return 4;
        }else if(Game -> file_type == 2)
        {
            printf("There are too many files!\n");
            return 0;
        }
    }else if(!strcmp(Game -> command_line[command_number], "id"))
    {
        printf("It asks for id!\n");
        Game -> check_for_id = 1;
        return 5;
    }else
    {
        printf("This: '%s' command line parameter is wrong!\n", Game -> command_line[command_number]);
        return 0;
    }
    return 2137;
}
