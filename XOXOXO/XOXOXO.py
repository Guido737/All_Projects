"""
XOXOXO
Created by: Creator/Eversor
Date: 30 Dec 2024
"""

import random
import os

def clear_screen():
    """
    function: clear_screen
    brief: Clears terminal screen.
    """
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except Exception as e:
        print(f"Error while clearing the screen: {e}")

def print_board(board):
    """
    function: print_board
    params: board (2D list)
    brief: Prints the Tic-Tac-Toe board.
    """
    try:
        for i in range(3):
            print(" | ".join(board[i]))
            if i < 2:
                print("-" * 5)
    except Exception as e:
        print(f"An error occurred while printing the board: {e}")

def check_win(board, player):
    """
    function: check_win
    params: board (2D list), player (str)
    brief: Check winner
    """
    try:
        for row in board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([board[row][col] == player for row in range(3)]):
                return True
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True
        return False
    except Exception as e:
        print(f"An error occurred while checking for a win: {e}")
        return False

def check_draw(board):
    """
    function: check_draw
    params: board (2D list)
    brief: Check draw
    """
    try:
        for row in board:
            if ' ' in row:
                return False
        return True
    except Exception as e:
        print(f"An error occurred while checking for a draw: {e}")
        return False

def player_move(board, player):
    """
    function: player_move
    params: board (2D list), player (str)
    brief: Handles the player's move.
    """
    while True:
        try:
            move = int(input(f"Player {player}, choose a cell (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid move. Choose a number between 1 and 9.")
                continue
            row, col = divmod(move, 3)
            if board[row][col] == ' ':
                board[row][col] = player
                break
            else:
                print("This cell is already taken, try another one.")
        except ValueError:
            print("Invalid input. Enter a number between 1 and 9.")
        except IndexError:
            print("Invalid input. Please enter a number between 1 and 9.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def computer_move(board, player):
    """
    function: computer_move
    params: board (2D list), player (str)
    brief: Handles the computer's move.
    """
    while True:
        try:
            move = random.randint(0, 8)
            row, col = divmod(move, 3)
            if board[row][col] == ' ':
                board[row][col] = player
                print(f"Computer chose cell {move + 1}")
                break
        except Exception as e:
            print(f"An error occurred during the computer's move: {e}")

def switch_player(current_player):
    """
    function: switch_player
    params: current_player (str)
    brief: Switches the current player.
    """
    return 'O' if current_player == 'X' else 'X'

def handle_game_mode(mode, current_player, board):
    """
    function: handle_game_mode
    params: mode (str), current_player (str), board (2D list)
    brief: Handles gameplay for different modes.
    """
    if mode == 'player_vs_player' or (mode == 'player_vs_computer' and current_player == 'X'):
        player_move(board, current_player)
    else:
        computer_move(board, current_player)

def play_game(mode):
    """
    function: play_game
    params: mode (str)
    brief: Main game loop.
    """
    try:
        board = [[' ' for i in range(3)] for i in range(3)]
        current_player = 'X'

        while True:
            clear_screen()
            print_board(board)
            handle_game_mode(mode, current_player, board)
            if check_win(board, current_player):
                clear_screen()
                print_board(board)
                print(f"Player {current_player} wins!")
                break
            elif check_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break
            current_player = switch_player(current_player)
    except Exception as e:
        print(f"An error occurred during the game: {e}")

def main():
    """
    function: main
    brief: Starts the game by asking for player input.
    """
    try:
        mode = input("With whom you want to play \n1) with another player \n2) With computer.\nEnter your choice: ")

        if mode == '1':
            play_game(mode='player_vs_player')
        elif mode == '2':
            play_game(mode='player_vs_computer')
        else:
            print("Invalid input. Try again.")
            main()
    except Exception as e:
        print(f"An error occurred in the main function: {e}")
        main()

if __name__ == "__main__":
    main()