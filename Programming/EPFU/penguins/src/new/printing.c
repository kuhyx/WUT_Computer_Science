#include "game_struct.h"

void print_board(GameState Game)
{
    printf(" ");

    for (int i=0;i<Game.board_width;i++)
    {
        printf(" %d",i);
    }
    printf("\n");
    for(int i = 0; i < Game.board_height; i++)
    {
        printf("%d ",i);
        for(int j = 0; j < Game.board_width; j++)
        {
            if ((Game.board[i][j].fish_no==0) && (Game.board[i][j].player_no==0))
            {
                printf("~ ");
            }
            else if(Game.board[i][j].fish_no==0)
            {
                printf("%d ",Game.board[i][j].player_no);
            }
            else
            {
                printf("%d ",Game.board[i][j].fish_no);
            }
        }
        printf("\n");
    }
}
