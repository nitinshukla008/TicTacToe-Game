import random
from typing import List, Tuple, Optional

class TicTacToe:
    def __init__(self):
        # Starting with an empty board - using a list of 9 spaces
        # We use spaces instead of empty strings to make the board look nicer when printed
        self.board = [" " for _ in range(9)]
        # X always starts first - this is traditional tic-tac-toe rules
        self.current_player = "X"
    
    def display_board(self):
        """Display the current state of the board"""
        # Adding extra newlines for cleaner output in the terminal
        print("\n")
        # Loop through board indices in steps of 3 to print each row
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            # Don't print the divider line after the last row
            if i < 6:
                print("-----------")
        print("\n")
    
    def is_valid_move(self, position: int) -> bool:
        """
        Make sure the move is legal:
        - Position must be on the board (0-8)
        - The chosen spot must be empty
        """
        return 0 <= position <= 8 and self.board[position] == " "
    
    def make_move(self, position: int) -> bool:
        """Try to make a move at the given position"""
        # First check if we can make the move
        if self.is_valid_move(position):
            # If valid, place the player's symbol and return True
            self.board[position] = self.current_player
            return True
        return False
    
    def check_winner(self) -> Optional[str]:
        """Look for a winner on the board"""
        # First check all rows - they start at indices 0, 3, and 6
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != " ":
                return self.board[i]
        
        # Then check all columns - they start at indices 0, 1, and 2
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return self.board[i]
        
        # Finally check both diagonals
        # Main diagonal: top-left to bottom-right
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]
        # Other diagonal: top-right to bottom-left
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]
        
        # No winner found
        return None
    
    def is_board_full(self) -> bool:
        """Check if we've hit a draw - no more empty spaces"""
        return " " not in self.board
    
    def get_ai_move(self) -> int:
        """
        Figure out the AI's next move. The AI follows these priorities:
        1. Win if there's a winning move
        2. Block the player if they're about to win
        3. Take the center if it's free (it's usually the best spot)
        4. Take a corner if available (corners are strong positions)
        5. Take any edge as a last resort
        """
        # First: Look for a winning move
        for i in range(9):
            if self.is_valid_move(i):
                # Try the move
                self.board[i] = "O"
                # See if it would win
                if self.check_winner() == "O":
                    # Undo our test move
                    self.board[i] = " "
                    return i
                # Undo our test move if it wasn't a winner
                self.board[i] = " "
        
        # Second: Block any player winning moves
        for i in range(9):
            if self.is_valid_move(i):
                # Try the player's potential move
                self.board[i] = "X"
                # See if it would be a win for them
                if self.check_winner() == "X":
                    # If it would, we need to block it
                    self.board[i] = " "
                    return i
                # Undo our test move
                self.board[i] = " "
        
        # Third: Take center if free - it's usually the best move
        if self.is_valid_move(4):
            return 4
        
        # Fourth: Try to take a corner - they're strong positions
        corners = [0, 2, 6, 8]
        # Get list of empty corners
        available_corners = [i for i in corners if self.is_valid_move(i)]
        if available_corners:
            # Pick a random corner to be less predictable
            return random.choice(available_corners)
        
        # Finally: Take any edge we can get
        edges = [1, 3, 5, 7]
        available_edges = [i for i in edges if self.is_valid_move(i)]
        if available_edges:
            return random.choice(available_edges)
        
        return -1  # Should never actually get here

def play_game():
    # Create our game board
    game = TicTacToe()
    
    # Let player pick game mode
    print("Welcome to Tic-Tac-Toe!")
    print("1. Two Players")
    print("2. Play against AI")
    
    # Keep asking until we get a valid choice
    while True:
        mode = input("Select mode (1 or 2): ").strip()
        if mode in ["1", "2"]:
            break
        print("Invalid input! Please enter 1 or 2.")
    
    # Main game loop
    while True:
        # Show current board state
        game.display_board()
        
        # Handle player moves
        if game.current_player == "X" or mode == "1":
            print(f"Player {game.current_player}'s turn")
            # Show the position numbers for reference
            print("Enter position (0-8):")
            print("0 | 1 | 2")
            print("---------")
            print("3 | 4 | 5")
            print("---------")
            print("6 | 7 | 8")
            
            # Keep trying until we get a valid move
            while True:
                try:
                    position = int(input("Position: "))
                    if game.make_move(position):
                        break
                    print("Invalid move! Try again.")
                except ValueError:
                    print("Please enter a number between 0 and 8!")
        else:
            # AI's turn
            print("AI's turn...")
            position = game.get_ai_move()
            game.make_move(position)
        
        # Check if game is over
        winner = game.check_winner()
        if winner:
            game.display_board()
            print(f"Player {winner} wins!")
            break
        
        # Check for a draw
        if game.is_board_full():
            game.display_board()
            print("It's a draw!")
            break
        
        # Switch to next player
        game.current_player = "O" if game.current_player == "X" else "X"
    
    # See if they want to play again
    play_again = input("Would you like to play again? (yes/no): ").lower().strip()
    if play_again.startswith('y'):
        play_game()

if __name__ == "__main__":
    play_game()
