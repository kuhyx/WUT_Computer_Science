#include "game_struct.h"
#include "printing.c"
// Phase == 1 : Placement

/* In this phase we give each player a chance to put his penguin on the field
for loop executed as total amount of penguins
Inside of it a do while loop that will be executed if the player move is wrong
outside of while loop we change player to the next one */

// Defining var for placement phase

int automaticPlacePenguin(GameState *Game)
{
    int i, j;
    for(i = 0; i < Game -> board_height; i++)
    {
        for(j = 0; j < Game -> board_width; j++)
        {
            if(Game -> board[i][j].fish_no == 1 && Game -> board[i][j].player_no == 0)
            {
                Game -> board[i][j].fish_no = 0;
                Game -> board[i][j].player_no = Game -> our_player_number;
                Game -> player_data[Game -> our_player_number].score += 1;
                printf("We put a penguin at coordinates: [%d][%d]\n", i, j);
                return 1;
            }
        }
    }
    printf("You can't put any penguin!\n");
    return 0;
}

int placePenguin(GameState *Game)  // Early version for placing the penguin in placement phase for interactive mode
{
    int c1, c2;
    printf("Enter where you want to put your penguin: \n");
    scanf("%d", &c1);
    scanf("%d", &c2);
    if(c1 < 0 || c1 > Game -> board_height || c2 < 0 || c2 > Game -> board_width)
    {
        printf("One of the coordinates is out of the board!\n");
        return 0;
    }
    if(Game -> board[c1][c2].fish_no != 1)
    {
        printf("Number of fishes on this field is not 1!\n");
        return 0;
    }
    Game -> board[c1][c2].player_no = Game -> current_player;
    Game -> board[c1][c2].fish_no = 0;
    Game -> player_data[Game -> current_player - 1].score += 1;
    return 1;
}

/* How the placement phase function is gonna work
void placePenguin ( Penguin *penguin , Field *field )  {
        penguin -> field = field;

    for ( int i = 0; i < player_count; ++i) {
        for ( int j = 0; j < players[i] -> penguinsCount; ++j ) {
            if ( players[i] -> penguins[j] == penguin ){
                 players[i] -> score += penguin-> field -> fish_count;
                 penguin -> field -> fish_count = 0;
            break;
            }
        }
    }
} */
