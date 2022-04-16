# Chess
A Slightly Incomplete Version of Chess.

## Scripts and Files
There are seven scripts, structured as follows:
* "Chess.py" contains the main game loop
* "Gameclasses.py" defines the player and piece classes
* "Gamedata.py" contains the initial positions of pieces, and the allowed moves for each piece. It also assigns values to each piece, which can be used in case an AI is integrated.
* "Gamefunctions.py" contains all functions which are reused often
* "Gameplay.py" defines the two games: against a real opponent, or an AI. The AI game has not been integrated yet.
* "Endscreen.py" shows the winner after a game
* "Main_menu.py" defines the function for the opening menu

## Incorporated
* Prevention of illegal moves (except king sacrifice detection)
* Visualisation of allowed moves, including visualisation for possible captures
* Castling, including all its rules
* Pawn promotion to queen

## Not Incorporated (Yet)
* Prevent king sacrifice
* En passant
* Stalemate
* Pawn promotion to other pieces than queen (knight, bishop, rook)
* Customise game looks: colours, whether possible moves are visible or not
* Playing against an AI
