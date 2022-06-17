#include "game_struct.h"

#ifdef _WIN32
#include "windows.h"
#endif

void welcome()
{
    printf("Hey there! Lets play ''HEY THAT'S MY FISH'' \n");
}

/* When the movement phase will be finished (There no more moves))
Check who won and who lost
Print out the score and winner
printf("Game over! %s you won, %s you suck", winner, loser)
END */
//  Each round the function will store the the starting score of the player
//  The score will be the difference between the initial amount of fish before the start of the round and the current number after it ended
//  So at the end of the round the current number of fish becomes the initial number
//  At the same time the starting score becomes the sum of previous starting score and the score of the round


int ScoreBoard(GameState Game)
{
    #ifdef _WIN32
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_SCREEN_BUFFER_INFO consoleInfo;
    WORD saved_attributes;

    /* Save current attributes */
    GetConsoleScreenBufferInfo(hConsole, &consoleInfo);
    saved_attributes = consoleInfo.wAttributes;
    SetConsoleTextAttribute(hConsole, 5);
    printf("Player number 1 score: %d\n", Game.player_data[0].score);

    SetConsoleTextAttribute(hConsole, saved_attributes);
    SetConsoleTextAttribute(hConsole, 6);
    printf("Player number 2 score: %d\n\n", Game.player_data[1].score);
    SetConsoleTextAttribute(hConsole, saved_attributes);
    #else
    printf("Player number 1 score: %d\n", Game.player_data[0].score);
    printf("Player number 2 score: %d\n\n", Game.player_data[1].score);

    #endif

    return 1;
}
