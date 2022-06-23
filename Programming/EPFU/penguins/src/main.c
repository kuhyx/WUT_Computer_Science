#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include "userinteraction.c"
#include "placement.c"
#include "movement.c"
#include "command_line_parameters.c"
#include "game_struct.h" // Header file for file where we store all our structures
#ifdef _WIN32
#include "windows.h"
#endif
#define INTERACTIVE
//#define AUTOMATIC

const char START_MESSAGE[] = "Hello again! Please enter the number of rows and columns \n";
const char PLACEMENT_TEXT[] = "================================\n \tPLACEMENT PHASE!\n================================\n";
const int BOTH_PLAYERS_HAVE_MOVES_FLAG = 0;
const int BOTH_PLAYERS_OUT_OF_MOVES_FLAG = 2;
const char PLAYER_ONE_WON[] = "Player ONE won!\n";
const char PLAYER_TWO_WON[] = "Player TWO won!\n";
const char TIE_MESSAGE[] = "It's a tie!\n";

void clearScreen()
{
  system("clear || cls");
}

void enterBoardWidthAndHeight(GameState *Game)
{
  printf(START_MESSAGE);
  scanf("%d", &(Game -> board_width));
  scanf("%d", &(Game  -> board_height));
}

void prepareBoard(GameState *Game)
{
  Game -> board = allocateMemory(*Game);
  Game -> board = randomizeFields(*Game);
}

const int STARTING_SCORE = 0;

GameState initializePlayerScoreVariables(GameState Game)
{
  Game.player_data[0].player_number = 1;
  Game.player_data[1].player_number = 2;
  Game.player_data[0].score = STARTING_SCORE;
  Game.player_data[1].score = STARTING_SCORE;
  return Game;
}

GameState setUpPenguinsPerPlayer(GameState Game)
{
  Game.one_fish_fields = checkPlacement(Game);
  Game.penguins_per_player = floor(Game.one_fish_fields / 2);
  return Game;
}

GameState initializeGame(GameState Game)
{
  enterBoardWidthAndHeight(&Game);
  prepareBoard(&Game);
  Game = initializePlayerScoreVariables(Game);
  printBoard(Game);
  Game = setUpPenguinsPerPlayer(Game);
  Game.current_player = 1;
  return Game;
}




GameState insidePlacePenguinsLoop(GameState Game, int i)
{
  while(!placePenguin(&Game));
  printBoard(Game);
  Game.current_player = (i + 1) % 2 + 1; // Since player numbers are 1 and 2 we need to make sure that this number is at least 1 and at max 2 as opposed to 0 and 1 if we just used i % 2
  return Game;
}

GameState placePenguins(GameState Game)
{
  int penguinsToPlace = 2 * Game.penguins_per_player;
  for(int i = 0; i < penguinsToPlace; i++)
  {
    Game = insidePlacePenguinsLoop(Game, i);
  }
  return Game;
}

GameState setUpGameBeforePlayPhase(GameState Game)
{
  clearScreen();
  printBoard(Game);
  Game.current_player = 1;
  Game.flag = BOTH_PLAYERS_HAVE_MOVES_FLAG;
  return Game;
}

GameState playPhase(GameState Game)
{
  while(Game.flag != BOTH_PLAYERS_OUT_OF_MOVES_FLAG)
  {
      movePenguin(&Game);
      clearScreen();
      /*
      if(movePenguin(&Game))
      {
          clearScreen();
      } Old code, not sure why we check if movePenguin end successfuly?
      */
      printBoard(Game);
  }
  return Game;
}

void calculateScorePhase(const GameState Game)
{
  if(Game.player_data[0].score > Game.player_data[1].score)
  {
      printf(PLAYER_ONE_WON);
  }else if(Game.player_data[0].score < Game.player_data[1].score)
  {
      printf(PLAYER_TWO_WON);
  }else printf(TIE_MESSAGE);
}

int interactive_mode(GameState Game)
{
    Game = initializeGame(Game);
    printf(PLACEMENT_TEXT);
    Game = placePenguins(Game);
    Game = setUpGameBeforePlayPhase(Game);
    Game = playPhase(Game);
    calculateScorePhase(Game);
    return 0;
}
int main(
  #ifdef AUTOMATIC
  int argc,
  char *argv[]
  #endif
  )
{
    GameState Game;
    #ifdef AUTOMATIC
    printf("Its automatic mode\n");

    if(argc != 1)
    {
         // Creating a Game variable that will hold informations needed to run the program
        Game.command_line = generateCommandLine(Game, argc);  // Generates 2D dynamic array of strings
        handlingParameters(argc, argv, Game);  // Stores all commands inside Game.command_line array
        Game.file_type = 0;  // We use this variable to check if the file we open is inputboardfile or outputboardfile
        Game.phase = 0;  // We use this variable to check if current game phase is placement (1) or movement(2)
        Game.penguins_from_command = 0;  // This variable checks if the user enter number of penguins in placement phase
        Game.check_for_id = 0;  // This variable checks if we got instruction to check id from the command line
        Game.our_player_number = 0;  // This variable will be used to determine our player number based on his ID

        for(int i = 0; i < argc - 1; i++)
        {
            if(checkParameterType(&Game, i) == 0)
            {
                printf("One of the parameters you entered is wrong!\n");
                return 2;
            }  // Inside this loop we run through each command and check what it does and assign proper values from those commands
        }

        if(Game.check_for_id == 0)  // Checks if the commands asked for ID
        {
            if(Game.file_type == 2)  // Checks if we got boards files from the commands
            {
                if(!handleInputFile(&Game))  // handleInputFile returns 1 if something went wrong, this function handles input file
                {
                    printf("Total number of players is %d\n", Game.total_players);
                    if(checkForStrayPenguins(Game) == 1)  // Checks if there are any penguins that don't belong to any player
                    {
                        printf("There is a stray penguin!\n");
                        return 2;
                    }
                    //printBoard(Game);
                    if(Game.phase == 1)
                    {
                        if(Game.penguins_from_command == 0)  // Checks if we got any penguins from command
                        {
                            printf("We didn't get any penguins from command!\n");
                            return 2;
                        }
                        if(Game.penguins == ourPenguins(Game))  // Checks if we put all our penguins
                        {
                            printf("All penguins have been placed");
                            return 1;
                        }else
                        {
                            if(automaticPlacePenguin(&Game) == 0)  // Tries to put penguin somewhere and if unable returns 0
                            {
                                printf("You can't put penguin anywhere!\n ");
                                handleOutPutFile(Game);
                                return 1;
                            }else
                            {
                                printf("Program placed a penguin!");
                                handleOutPutFile(Game);
                                return 0;
                            }
                        }
                    }else if(Game.phase == 2 && Game.penguins_from_command == 0)  // Checks if it is a movement phase
                    {
                        if(checkMove(Game) == 0) // This function checks if there are any moves left for any player
                        {
                            printf("All penguins are blocked! ");
                            handleOutPutFile(Game);
                            return 1;
                        }else
                        {
                            automaticMovePenguin(&Game);  // Moves our penguin automatically
                            handleOutPutFile(Game);
                            return 0;
                        }
                    }else
                    {
                        printf("You entered number of penguins even though it is a movement phase!\n");
                        return 2;
                    }
                }else
                {
                    printf("There is a mistake in board file! ");   // type of mistake is printed out in handleInputFile function
                    fclose(Game.input_board);
                    return 2;
                }
            }else if(Game.file_type == 1)
            {
                printf("You entered input board file name but did not enter output board file name!");
                return 2;
            }else if(Game.phase != 0)
            {
                printf("You did not enter input board file and output board file");
                return 2;
            }

            printf("Our player number is: %d\n", Game.our_player_number);
            printf("Everything went great");

        }else
        {
            printf("marcel");
            return 0;
        }
    }else
    {
        printf("You entered too few arguments! ");
        return 2;
    }
    return 2137;
    #endif
    #ifdef INTERACTIVE
    welcome(); // User interaction - showing communicate at the start of the program
    interactive_mode(Game);
    return 0;
    #endif // INTERACTIVE
}
