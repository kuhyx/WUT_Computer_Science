#include<stdlib.h>
#include<stdio.h>
#include<time.h>

//Defining struct Board 
typedef struct
{
	int penguin_no;
	int player_no;
}Board;

//Board Dimensions
int board_width = 6;
int board_height =6;

int main()
{
	srand(time(NULL));
	Board board[board_height][board_width]; // Creating 2D array of type Board

	for (int i = 0; i < board_height ; ++i) // Populating our board with penguins and players (player_no set to 0 as no player is present on the board)
	{
		for (int j = 0; j < board_width ; ++j)
		{
			board[i][j].player_no = 0;
			board[i][j].penguin_no = rand() % 4; // Randomizing no of penguins on each cell ( Between 0 and 3 )

		}
	}

	for (int i = 0; i < board_height ; ++i) // Printing our board
	{
		for (int j = 0; j < board_width ; ++j)
		{
			printf("[Penguins = %d][PLayer no = %d] ",board[i][j].penguin_no,board[i][j].player_no );


		}
		printf("\n");
		
	}


	return 0;
}