#include "game_struct.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "generate.c"

int samePlayerID(GameState Game, int k)
{

    for(int i = 1; i < k; i++)
    {
        if(!strcmp(Game.player_data[i].playerID, Game.player_data[k].playerID))
        {
            return 1;
        }
    }
    return 0;
}

int handleInputFile(GameState *Game)
{
    Game -> lines_number = 0;
    char rows[30], columns[30];  // Stores rows number and columns number from the board file
    char c;  // Gets all the characters from the file
    int rows_number, columns_number;  // Stores int values of rows and columns number from the board file
    int i = 0, j;
    while((c = getc(Game -> input_board)) != ' ')  // Getting rows number
    {
        if(c >= '0' && c <= '9' && c != ' ') // Checks if rows number is a number
        {
            rows[i] = c;
            i++;
            if(i >= 30)
            {
                printf("Row number is too big! \n");
                return 1;
            }
        }else
        {
            printf("row number is not a number! \n");
            return 1;
        }
    }

    i = 0;
    while((c = getc(Game -> input_board)) != ' ' && c != '\n')  // Gets columns number
    {
        if(c >= '0' && c <= '9' && c != ' ')  // Checks if columns number is a number
        {
        columns[i] = c;
        i++;
        if(i >= 30)
        {
            printf("Columns number is too big! \n");
            return 1;
        }
        }else
        {
            printf("row number is not a number! \n");
            return 1;
        }
    }

    rows_number = atoi(rows);  // Changes rows number from a string to an integer
    printf("Rows number is: %d\n", rows_number);
    columns_number = atoi(columns);
    printf("Columns number is: %d\n", columns_number);

    Game -> board_height = rows_number;
    Game -> board_width = columns_number;

    if(rows_number == 0 || columns_number == 0)  // Checks if rows or columns number is equal to 0
    {
        if(rows_number == 0)
        {
            printf("Number of rows is equal to 0!\n");
            return 1;
        }else
        {
            printf("Number of columns is equal to 0!\n");
            return 1;
        }
    }
    Game -> board = allocateMemory(*Game);  // Allocates memory for our board
    int check = 0;  // flag that is either 0 if we get fish number of 1 if we get player number
    int value = 0;  // temporary value for fish number and player number
    int three = 1; // Used to check if there are any extra characters in file between board files
    int current_columns = 0;  // Used to check is there are any extra columns

    for(int i = 0; i < Game -> board_height; i++)  // This for loop gets fields from the board file
    {
        int j = 0;
        while((c = getc(Game -> input_board)) != '\n')
        {
            if(three % 3 != 0 || (i == 0 && j == 0))
            {
                if(c != ' ' && check == 0)
                {
                    if(c >= '0' && c <= '3' && c != ' ')
                    {
                        value = c - '0';  // According to Stack Overflow it works and is valid with all standards
                        Game -> board[i][j].fish_no = value;
                        check = 1;
                        three++;
                    }else if(c > '3' && c <= '9')
                    {
                        printf("Number of fishes on field: [%d][%d] is too big!\n", i ,j);
                        return 1;
                    }else
                    {
                        printf("Number of fishes on field: [%d][%d] is not a number!\n", i, j);
                        return 1;
                    }
                }else if(c != ' ' && check == 1)
                {
                    if(c >= '0' && c <= '9')
                    {
                        value = c - '0';
                        Game -> board[i][j].player_no = value;
                        check = 0;
                        j++;
                        three++;
                        current_columns++;
                    }else
                    {
                        printf("Number of players on field: [%d][%d] is not a number!\n", i, j);
                        return 1;
                    }
                }
            }else if(c == ' ')
            {
                three++;
            }else
            {
                printf("There are more than two elements on field: [%d][%d]", i, j);
                return 1;
            }
        }
        if(current_columns != columns_number)
        {
            printf("There is different number of columns than there should be!\n");
            return 1;
        }else current_columns = 0;
    }

    i = 0;
    int expected_player = 1;  // Used to put player ID, score and number into right array and checks if player numbers are in order
    // We use 1 because it is much simpler
    while((c = getc(Game -> input_board)) != EOF)  // Checks last m+2 and consecutive rows
    {
        j = 0;
        do   // checks player id
        {
            if(c != ' ' && c != '"' && c != '\n' && c != EOF)
            {
                if(j < 500)
                {
                Game -> player_data[expected_player].playerID[j] = c;
                j++;
                }else
                {
                    printf("Id of this player is too long!\n");
                    return 1;
                }
            }else if(c == ' ')
            {
                printf("Player ID contains a space! ");
                return 1;
            }else if(c == '"')
            {
                printf("Player ID contains a quotation mark! ");
                return 1;
            }else if(c == '\n')
            {
                while((c = getc(Game -> input_board)) != EOF)
                {
                    if(c != ' ' && c != '\n' && c != EOF)
                    {
                        printf(":<");
                        return 1;
                    }
                }
                Game -> total_players = expected_player - 1;
                return 0;
            }else
            {
                printf("Player ID contains end of file character!");
                return 1;
            }

        }while((c = getc(Game -> input_board)) != ' ');


        for(i = strlen(Game -> player_data[expected_player].playerID); i >= j; i--)  // We clear playerID string characters after the characters we get from the file
        {
            Game -> player_data[expected_player].playerID[i] = 0;
        }

        if(samePlayerID(*Game, expected_player) && expected_player != 1)  // Checks if the players ID's are the same
        {
            printf("Two player ID's are the same!\n");
            return 1;
        }

        c = getc(Game -> input_board);
        if(c >= '1' && c <= '9')
        {
            Game -> player_data[expected_player].player_number = c - '0';  // Gets player number from the file
            if(expected_player != Game -> player_data[expected_player].player_number)
            {
                printf("Player numbers from the file is not in order!");
                return 1;
            }

            if(!strcmp(Game -> player_data[expected_player].playerID, "marcel"))  // Checks if the player ID is our's player ID
            {
                Game -> our_player_number = Game -> player_data[expected_player].player_number;
            }

            if( getc(Game -> input_board) == ' ')
            {
            char score[100];
            i = 0;
            while((c = getc(Game -> input_board)) != '\n' && c != EOF)  // Gets player score from the file
            {
                if(c >= '0' && c <= '9' && i < 100)
                {
                    score[i] = c;
                    i++;
                }else
                {
                    printf("Player score is not a number!\n");
                    return 1;
                }

            }

            Game -> player_data[expected_player].score = atoi(score);
            printf("Player ID is: %s\n", Game -> player_data[expected_player].playerID);
            printf("Player number is: %d\n", Game -> player_data[expected_player].player_number);
            printf("Player score is: %d\n", Game -> player_data[expected_player].score);
            Game -> lines_number++;
            expected_player++;
            }else
            {
                printf("Player number is longer than 1 character! ");
                return 1;
            }
        }else
        {
            printf("Player number is not a number or is equal to 0 \n");
            return 1;
        }

    }
    if (Game -> our_player_number == 0)
    {
        printf("There is no id for our player!\n");
        return 1;
    }
    Game -> total_players = expected_player - 1;
    fclose(Game -> input_board);
    return 0;
}

int checkForStrayPenguins(GameState Game)
{
    printf("%d\n", Game.total_players);
    for(int i = 0; i < Game.board_height; i++)
    {
        for(int j = 0; j < Game.board_width; j++)
        {
            if(Game.board[i][j].player_no > Game.total_players)
            {
                printf("There is a stray penguin on field [%d][%d]\n", i, j);
                printf("%d\n", Game.board[i][j].player_no);
                return 1;
            }
        }
    }
    return 0;
}

int handleOutPutFile(GameState Game)
{
    int i, j;
    fprintf(Game.output_board, "%d %d\n", Game.board_height, Game.board_width);
    for(i = 0; i < Game.board_height; i++)
    {
        for(j = 0; j < Game.board_width; j++)
        {
            fprintf(Game.output_board, "%d%d ", Game.board[i][j].fish_no, Game.board[i][j].player_no);
        }
        fprintf(Game.output_board, "\n");
    }
    printf("%d", Game.lines_number);
    for(i = 1; i < Game.lines_number + 1; i++)
    {
        fprintf(Game.output_board, "%s %d %d\n", Game.player_data[i].playerID, Game.player_data[i].player_number, Game.player_data[i].score);
    }
    fclose(Game.output_board);
    return 0;
}
