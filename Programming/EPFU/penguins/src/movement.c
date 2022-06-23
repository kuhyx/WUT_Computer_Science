#include "game_struct.h"
#include "checkmove.c"

// Phase == 2 : Movement
/* In this phase we give each player a chance to move his penguin
    1. Inside of it we will have a do while loop that will execute until there would be no more moves
    2. First player chooses the penguin (For user interaction we print out his name and tell him to choose a penguin)
    printf("%s choose a penguin", player_name[player_number][];
    scanf("%d %d", &coordinate_1, &coordinate_2) coordinate_1 - coordinate one, coordinate_2 - coordinate two
    Now we check if the penguin he has chosen has a valid move
    3. Placing the penguin (For user interaction we print out his name and tell him to place a penguin)
    printf("%s choose a penguin", player_name[player_number][];
    scanf("%d %d", &coordinate_3, &coordinate_4) coordinate_3 - coordinate three, coordinate_4 - coordinate four
    Now we check if the move is valid
    The move is made
    We update the scoreboard */

int automaticMovePenguin(GameState *Game)
{
    Movement_coordinates Coordinates;
    for(int i = 0; i < Game -> board_height; i++)
        for(int j = 0; j < Game -> board_width; j++)
        {
            if(Game -> board[i][j].player_no == Game -> our_player_number)
            {
                Coordinates.coordinate_1 = i;
                Coordinates.coordinate_2 = j;
                if(anyMovePossible(Coordinates, *Game) == 1)
                {
                    Game -> board[i][j].player_no = 0;
                    Game -> board[i][j].fish_no = 0;
                    Game -> player_data[Game -> our_player_number].score += Game -> board[i][j - 1].fish_no;
                    Game -> board[i][j - 1].player_no = Game -> our_player_number;
                    Game -> board[i][j - 1].fish_no = 0;
                    return 1;
                }else if(anyMovePossible(Coordinates, *Game) == 2)
                {
                    Game -> board[i][j].player_no = 0;
                    Game -> board[i][j].fish_no = 0;
                    Game -> player_data[Game -> our_player_number].score += Game -> board[i - 1][j].fish_no;
                    Game -> board[i - 1][j].player_no = Game -> our_player_number;
                    Game -> board[i - 1][j].fish_no = 0;
                    return 1;
                }else if(anyMovePossible(Coordinates, *Game) == 3)
                {
                    Game -> board[i][j].player_no = 0;
                    Game -> board[i][j].fish_no = 0;
                    Game -> player_data[Game -> our_player_number].score += Game -> board[i + 1][j].fish_no;
                    Game -> board[i + 1][j].player_no = Game -> our_player_number;
                    Game -> board[i + 1][j].fish_no = 0;
                    return 1;
                }else if(anyMovePossible(Coordinates, *Game) == 4)
                {
                    Game -> board[i][j].player_no = 0;
                    Game -> board[i][j].fish_no = 0;
                    Game -> player_data[Game -> our_player_number].score += Game -> board[i][j].fish_no;
                    Game -> board[i][j + 1].player_no = Game -> our_player_number;
                    Game -> board[i][j + 1].fish_no = 0;
                    return 1;
                }
            }
        }
    printf("We didn't manage to put penguin anywhere! \n");
    return 0;
}

int movePenguin(GameState *Game)  // Early version of moving the Penguin for interaction Phase
{
    int check = checkPlayer(*Game);
    if(!check)
    {
        printf("You don't have any more moves left!\n");
        Game -> flag += 1;
        return 0;
    }
    Movement_coordinates c;
    printf("Player %d choose the coordinates of the penguin you want to move:\n", Game -> current_player);
    scanf("%d", &c.coordinate_1);
    scanf("%d", &c.coordinate_2);
    if(Game -> board[c.coordinate_1][c.coordinate_2].player_no != Game -> current_player)
    {
        printf("This is not your penguin!\n");
        return 0;
    }

    if(anyMovePossible(c, *Game) == 0)
    {
        printf("This penguin can't move anywhere!\n");
        Game -> board[c.coordinate_1][c.coordinate_2].fish_no = 0;
        Game -> board[c.coordinate_1][c.coordinate_2].player_no = 0;
        return 0;
    }

    printf("Player %d, choose the coordinates of the place you want to put your penguin:\n", Game -> current_player);
    scanf("%d", &c.coordinate_3);
    scanf("%d", &c.coordinate_4);
    if(c.coordinate_1 == c.coordinate_3 && c.coordinate_2 == c.coordinate_4)
    {
        printf("Coordinates of the move is the same as the coordinates of the penguin!\n");
        return 0;
    }
    if(checkMovement(c, *Game) == 0)
    {
        printf("You can't move this penguin there!\n");
        return 0;
    }
    Game -> board[c.coordinate_1][c.coordinate_2].fish_no = 0;
    Game -> board[c.coordinate_1][c.coordinate_2].player_no = 0;

    Game -> board[c.coordinate_3][c.coordinate_4].player_no = Game -> current_player;
    Game -> player_data[Game -> current_player - 1].score += Game -> board[c.coordinate_3][c.coordinate_4].fish_no;
    Game -> board[c.coordinate_3][c.coordinate_4].fish_no = 0;
    if(Game -> current_player == 2)
    {
        Game -> current_player = 1;
    }else Game -> current_player = 2;
    return 1;
}

