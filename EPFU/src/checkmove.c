#include "game_struct.h"
// In order to check if the move is correct we need our board, in order to have
// our board we need it's height and width, that's first 3 variables inside the function
// then we need coordinates of where the penguin currently is (coordinate_1 and coordinate_2)
// and coordinates of where we want to put the penguin (coordinate_3 and coordinate_4)

int anyMovePossible(Movement_coordinates Coordinates, GameState Game)
{
    if(Coordinates.coordinate_1 > 0 && Coordinates.coordinate_1 + 1 < Game.board_height)
    {
        if(Coordinates.coordinate_2 > 0 && Coordinates.coordinate_2 < Game.board_width)
        {
            if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].player_no == 0) // LEFT
            {
                return 1;
            }else if(Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].player_no == 0) // UP
            {
                return 2;
            }else if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].player_no == 0) // DOWN
            {
                return 3;
            }else if(Game.board[Coordinates.coordinate_1 + 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 + 1][Coordinates.coordinate_2].player_no == 0) //RIGHT
            {
                return 4;
            }else return 0;
        }else if(Coordinates.coordinate_2 == 0)
        {
            if(Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].player_no == 0) // UP
            {
                return 2;
            }else if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].player_no == 0) // DOWN
            {
                return 3;
            }else if(Game.board[Coordinates.coordinate_1 + 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 + 1][Coordinates.coordinate_2].player_no == 0) //RIGHT
            {
                return 4;
            }else return 0;
        }else if(Coordinates.coordinate_2 == Game.board_width - 1)
        {
            if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].player_no == 0) // LEFT
            {
                return 1;
            }else if(Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].player_no == 0) // UP
            {
                return 2;
            }else if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].player_no == 0) // DOWN
            {
                return 3;
            }else return 0;
        }else
        {
            printf("You missed a case!\n");
            return 0;
        }
    }else if(Coordinates.coordinate_1 == 0)
    {
        if(Coordinates.coordinate_2 > 0 && Coordinates.coordinate_2 < Game.board_width)
        {
            if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].player_no == 0) // LEFT
            {
                return 1;
            }else if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].player_no == 0) // DOWN
            {
                return 3;
            }else if(Game.board[Coordinates.coordinate_1 + 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 + 1][Coordinates.coordinate_2].player_no == 0) //RIGHT
            {
                return 4;
            }else return 0;
        }else if(Coordinates.coordinate_2 == 0)
        {
            if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].player_no == 0) // DOWN
            {
                return 2;
            }else if(Game.board[Coordinates.coordinate_1 + 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 + 1][Coordinates.coordinate_2].player_no == 0) //RIGHT
            {
                return 4;
            }else return 0;
        }else if(Coordinates.coordinate_2 == Game.board_width)
        {
            if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].player_no == 0) // LEFT
            {
                return 1;
            }else if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].player_no == 0) // DOWN
            {
                return 3;
            }else return 0;
        }else
        {
            printf("You missed a case!\n");
            return 0;
        }
    }else if(Coordinates.coordinate_1 + 1 == Game.board_height)
    {
        if(Coordinates.coordinate_2 > 0 && Coordinates.coordinate_2 < Game.board_width)
        {
            if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].player_no == 0) // LEFT
            {
                return 1;
            }else if(Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].player_no == 0) // UP
            {
                return 2;
            }else if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].player_no == 0) // RIGHT
            {
                return 4;
            }else return 0;
        }else if(Coordinates.coordinate_2 == 0)
        {
            if(Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].player_no == 0) // UP
            {
                return 2;
            }else if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 + 1].player_no == 0) // RIGHT
            {
                return 4;
            }else return 0;
        }else if(Coordinates.coordinate_2 == Game.board_width)
        {
            if(Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].fish_no != 0 && Game.board[Coordinates.coordinate_1][Coordinates.coordinate_2 - 1].player_no == 0) // LEFT
            {
                return 1;
            }else if(Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].fish_no != 0 && Game.board[Coordinates.coordinate_1 - 1][Coordinates.coordinate_2].player_no == 0) // UP
            {
                return 2;
            }else return 0;
        }else
        {
            printf("You missed a case!\n");
            return 0;
        }
    }else
    {
        printf("You missed a case!\n");
        return 0;
    }
}

int checkMovement(Movement_coordinates c, GameState Game)
{
    int i = 0;
    if(c.coordinate_1 == c.coordinate_3)
    {
        if(c.coordinate_2 < c.coordinate_4)
        {
            for(i = c.coordinate_2 + 1; i <= c.coordinate_4; i++)
            {
                if(Game.board[c.coordinate_1][i].fish_no == 0 || Game.board[c.coordinate_1][i].player_no != 0)
                {
                    printf("There is another penguin or water on field Board[%d][%d]!\n", c.coordinate_1, i);
                    return 0;
                }
            }
            return 1;
        }else if(c.coordinate_2 > c.coordinate_4)
        {
            for(i = c.coordinate_2 - 1; i >= c.coordinate_4; i--)
            {
                if(Game.board[c.coordinate_1][i].fish_no == 0 || Game.board[c.coordinate_1][i].player_no != 0)
                {
                    printf("There is another penguin or water on field Board[%d][%d]!\n", c.coordinate_1, i);
                    return 0;
                }
            }
            return 1;
        }
    }else if(c.coordinate_2 == c.coordinate_4)
    {
        if(c.coordinate_1 < c.coordinate_3)
        {
            for(i = c.coordinate_1 + 1; i <= c.coordinate_3; i++)
            {
                if(Game.board[i][c.coordinate_2].fish_no == 0 || Game.board[i][c.coordinate_2].player_no != 0)
                {
                    printf("There is another penguin or water on field Board[%d][%d]!\n", i, c.coordinate_2);
                    return 0;
                }
            }
            return 1;
        }else if(c.coordinate_1 > c.coordinate_3)
        {
            for(i = c.coordinate_1 - 1; i >= c.coordinate_3; i--)
            {
                if(Game.board[i][c.coordinate_2].fish_no == 0 || Game.board[i][c.coordinate_2].player_no != 0)
                {
                    printf("There is another penguin or water on field Board[%d][%d]!\n", i, c.coordinate_2);
                    return 0;
                }
            }
            return 1;
        }
    }else
    {
        printf("You can't move the penguin diagonally!\n");
        return 0;
    }

    printf("Something went really bad in function checkMovement()");
    return 0;
}

int ourPenguins(GameState Game)
{
    int i, j;  // This function checks how many penguins we have and returns this number
    int number_of_our_penguins;
    number_of_our_penguins = 0;
    for(i = 0; i < Game.board_height; i++)
    {
        for(j = 0; j < Game.board_width; j++)
        {
            if(Game.board[i][j].player_no == Game.our_player_number)
            {
                number_of_our_penguins++;
            }
        }
    }
    return number_of_our_penguins;
}

int checkMove(GameState Game)
{
    Movement_coordinates Coordinates;
    int i, j, anymove;
    for(i = 0; i < Game.board_height; i++)  // This goes through the whole board and checks if there are any moves possible for every penguin we find
    {
        for(j = 0; j < Game.board_width; j++)
        {
            if(Game.board[i][j].player_no != 0)
            {
                Coordinates.coordinate_1 = i;
                Coordinates.coordinate_2 = j;
                printf("We check if there is any move possible at board[%d][%d]\n", Coordinates.coordinate_1, Coordinates.coordinate_2);
                anymove = anyMovePossible(Coordinates, Game);
                if(anymove != 0)
                {
                    printf("There is a possible move!\n");
                    return 1;
                }
            }
        }
    }
    printf("There are no possible moves!\n");
    return 0;
}
int checkPlayer(GameState Game)
{
    Movement_coordinates c;
    for(int i = 0; i < Game.board_height; i++)
    {
        for(int j = 0; j < Game.board_width; j++)
        {
            //printf("Player number:%d\n", Game.board[i][j].player_no);
            if(Game.board[i][j].player_no == Game.current_player)
            {
                c.coordinate_1 = i;
                c.coordinate_2 = j;
                if(anyMovePossible(c, Game) != 0)
                {
                    //printf("Player %d, has at least one move left!\n", Game.current_player);
                    return 1;
                }
            }
        }
    }
    return 0;
}

int checkPlacement(GameState Game)
{
    int one_fish = 0;
    for(int i = 0; i < Game.board_height; i++)
    {
        for(int j = 0; j < Game.board_width; j++)
        {
            if(Game.board[i][j].fish_no == 1)
            {
                one_fish++;
            }
        }
    }
    return one_fish;
}
