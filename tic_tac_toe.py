from collections import deque
from pyfiglet import Figlet

SIZE = 3
turns = 0


def ask_for_another_game():
    player_choice = input("Would you like to play again? (y/n): ")

    if player_choice == 'y':
        main()
    else:
        print("\nThanks for playing!")
        raise SystemExit


def check_for_win(players, play_board):
    player_name, player_symbol = players[0].values()

    is_first_diagonal_win = all([play_board[i][i] == player_symbol for i in range(SIZE)])
    is_second_diagonal_win = all([play_board[i][SIZE - i - 1] == player_symbol for i in range(SIZE)])

    is_row_win = any([all([el == player_symbol for el in row]) for row in play_board])
    is_col_win = any([all([play_board[r][c] == player_symbol for r in range(SIZE)]) for c in range(SIZE)])

    if any([is_first_diagonal_win, is_second_diagonal_win, is_row_win, is_col_win]):
        print_board(play_board)
        print(f"\n{player_name} wins!")

        ask_for_another_game()


def place_symbol(players, play_board, row, col):
    play_board[row][col] = players[0]["symbol"]

    check_for_win(players, play_board)
    print_board(play_board)

    if turns == SIZE * SIZE:
        print("Draw!")
        ask_for_another_game()

    players.rotate()


def choose_position(players, play_board):
    global turns

    while True:
        try:
            position = int(input(f"{players[0]['name']} choose a position between 1 and {SIZE * SIZE}: "))
            row, col = (position - 1) // SIZE, (position - 1) % SIZE
        except ValueError:
            enter_valid_position_msg(players)
            continue

        if 0 <= position <= SIZE * SIZE and play_board[row][col] == " ":
            turns += 1
            place_symbol(players, play_board, row, col)
        else:
            enter_valid_position_msg(players)
            continue


def enter_valid_position_msg(players):
    print(f"{players[0]['name']}, please enter a valid position!")


def print_board(play_board):
    [print(f"| {' | '.join(row)} |") for row in play_board]


def print_game_state(play_board, is_begin=False):
    if is_begin:
        print("\nThis is the numeration of the board:")
        print_board(play_board)

        for r in range(SIZE):
            for c in range(SIZE):
                play_board[r][c] = " "
    else:
        print_board(play_board)


def start(players, play_board):
    f = Figlet(font='slant')
    print(f.renderText("Tic Tac Toe"))

    player_one_name = input("Player one please enter your name: ")
    player_two_name = input("Player two please enter your name: ")

    while True:
        player_one_symbol = input(f"{player_one_name}, would you like to play with 'X' or 'O': ").upper()

        if player_one_symbol not in ["X", "O"]:
            print("Please enter either 'X' or 'O'")
        else:
            break

    player_two_symbol = "O" if player_one_symbol == "X" else "X"

    players.append({"name": player_one_name, "symbol": player_one_symbol})
    players.append({"name": player_two_name, "symbol": player_two_symbol})

    print_game_state(play_board, is_begin=True)
    choose_position(players, play_board)


def main():
    play_board = [[str(r + c) for c in range(SIZE)] for r in range(1, SIZE ** 2 + 1, SIZE)]
    players = deque()

    start(players, play_board)


if __name__ == "__main__":
    main()
