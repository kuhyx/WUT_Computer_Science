#ifndef STRUCT_H_
#define STRUCT_H_
#include <stdio.h>

typedef struct // Struct for our board
{
	int fish_no;
	int player_no;
}Field;

typedef struct Coordinates
{
    int coordinate_1;   // Coordinate of penguin's location.
    int coordinate_2;   // Coordinate of penguin's location.
    int coordinate_3;   // Coordinate of where we want to put the penguin.
    int coordinate_4;   // Coordinate of where we want to put the penguin.
}Movement_coordinates;

struct Player
{
    char playerID[500];
    int player_number;
    int score;
};

typedef struct Game   // Struct containing all of the variables that the program needs.
{
    char** command_line;
    Field** board;
    FILE *input_board;
    FILE *output_board;
    int board_height;   // The height of the board.
    int board_width;    // The width of the board.
    int total_players;  // Total number of players.
    int one_fish_fields;
    int current_player; // Player.
    int penguins;
    int penguins_per_player;
    int file_type; // Flag that checks if the file from command line parameter is inputboardfile (0) or outputboardfile (1)
    int phase; //decides the phase of the game 1 - placement; 2 - movement
    int our_player_number;
    int lines_number;
    int input_board_command_number;
    int penguins_from_command;
    int check_for_id;
    struct Player player_data[10];
    int flag;
}GameState;


#endif


