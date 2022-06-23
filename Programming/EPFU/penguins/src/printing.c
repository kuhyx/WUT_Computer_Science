#include "game_struct.h"
#ifdef _WIN32
#include "windows.h"
#endif

int printBoard(GameState Game)
{
    #ifdef _WIN32
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_SCREEN_BUFFER_INFO consoleInfo;
    WORD saved_attributes;

    /* Save current attributes */
    GetConsoleScreenBufferInfo(hConsole, &consoleInfo);
    saved_attributes = consoleInfo.wAttributes;
    system("clear || cls");
    printf("\nCurrent board status:\n");
    printf("  ");

    for (int i = 0; i < Game.board_width; i++)
    {
        printf("%d  ", i); // Here we print the number of columns
    }
    printf("\n");
    for(int i = 0; i < Game.board_height; i++)
    {
        printf("%d ", i);  // Here we print the number of rows
        for(int j = 0; j < Game.board_width; j++)
        {
            if ((Game.board[i][j].fish_no == 0) && (Game.board[i][j].player_no == 0))
            {
                SetConsoleTextAttribute(hConsole, FOREGROUND_BLUE);
                printf("~  ");  // If there are no penguins and fish on the field we print the 'wave'
                SetConsoleTextAttribute(hConsole, saved_attributes);
            }
            else if(Game.board[i][j].fish_no == 0)
            {
                SetConsoleTextAttribute(hConsole, FOREGROUND_RED);
                printf("P%d ",Game.board[i][j].player_no);
                SetConsoleTextAttribute(hConsole, saved_attributes);
            }
            else
            {
                SetConsoleTextAttribute(hConsole, FOREGROUND_GREEN);
                printf("F%d ",Game.board[i][j].fish_no);
                SetConsoleTextAttribute(hConsole, saved_attributes);
            }
        }
        printf("\n");
    }
    printf("\n");
    #else
    system("clear || cls");
    printf("\nCurrent board status:\n");
    printf("  ");

    for (int i = 0; i < Game.board_width; i++)
    {
        printf("%d  ", i); // Here we print the number of columns
    }
    printf("\n");
    for(int i = 0; i < Game.board_height; i++)
    {
        printf("%d ", i);  // Here we print the number of rows
        for(int j = 0; j < Game.board_width; j++)
        {
            if ((Game.board[i][j].fish_no == 0) && (Game.board[i][j].player_no == 0))
            {
                printf("~  ");  // If there are no penguins and fish on the field we print the 'wave'
            }
            else if(Game.board[i][j].fish_no == 0)
            {
                printf("P%d ",Game.board[i][j].player_no);
            }
            else
            {
                printf("F%d ",Game.board[i][j].fish_no);
            }
        }
        printf("\n");
    }
    printf("\n");

    #endif
    ScoreBoard(Game);
    return 0;
}
