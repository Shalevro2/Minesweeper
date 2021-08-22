"""
Program: minesweeper.py
"""

from random import randint


def is_int(strNum):
    """
    function check if variable is a integer number
    :param strNum: The variable to check
    :return: True is the variable is a integer number, otherwise False
    """
    try:  # Try to convert, if success return True, otherwise return False
        int(strNum)
        return True
    except ValueError:
        return False


def valid_index(board, row, col):
    """
    function return True if row and col in range and integers
    :param board: board of the game
    :param row: index in row
    :param col: index in column
    :return: True if row and col in range and integers, otherwise
    """
    validInt = is_int(row) and is_int(col)
    return validInt and 0 <= int(row) < len(board) and 0 <= int(col) < len(board)


def is_mine(real_board, row, col):
    """
    function return True if board[row][col] is mine
    :param real_board: game board
    :param row: index of row
    :param col: index of column
    :return: True if board[row][col] is mine, otherwise False
    """
    return real_board[row][col] == "X"


def count_neighbors(board, row, col):
    """
    function count the number of mines around cell
    :param board: game board
    :param row: index of row
    :param col: index of column
    :return: number of mines around cell
    """
    count = 0

    # for each cell around the original cell (row, cell),
    # check if the index valid and the cell is mine, if the conditions return True count++
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i != 0 or j != 0:
                if valid_index(board, row + i, col + j) and is_mine(board, row + i, col + j):
                    count += 1

    return count


def reveal_zeros(real_board, user_board, row, col):
    """
    function reveal in the user board all the cells around the user_board[row][col] that not mines.
    :param real_board: the real board
    :param user_board: the board to show the user with his choices
    :param row: index of row
    :param col: index of column
    :return: none
    """
    # if invalid index, return
    if row >= len(real_board[0]) or col >= len(real_board[0]) or row < 0 or col < 0:
        return

    # if real_board[row][col] is zero and user_board[row][col] not reveal yet,
    # reveal user_board[row][col] and check for all the neighbors of real_board[row][col] if they mine.
    if real_board[row][col] == 0 and user_board[row][col] == " ":
        user_board[row][col] = real_board[row][col]

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    reveal_zeros(real_board, user_board, row + i, col + j)

    # reveal user[row][col] if is not zero and not mine
    if real_board[row][col] != 0 and not is_mine(real_board, row, col):
        user_board[row][col] = real_board[row][col]


def create_boards(size, mine_num):
    """
    function create two boards in len(size)*len(size).
    user_board will be a list of list with spaces.
    real_board will be list of list with mine_num mines ('X') and count every cell mines neighbors.
    :param size: size of board
    :param mine_num: number of mines
    :return: real_board, user_board
    """
    real_board = [[" " for i in range(size)] for i in range(size)]
    user_board = [[" " for i in range(size)] for i in range(size)]
    i = 0
    #  insert 'X' mine_num-times randomly to real_board
    while i < mine_num:
        r1, r2 = randint(0, (size-1)), randint(0, (size-1))
        if real_board[r1][r2] != "X":
            real_board[r1][r2] = "X"
            i += 1

    # count every cell mines neighbors.
    for r in range(size):
        for c in range(size):
            if real_board[r][c] != "X":
                real_board[r][c] = count_neighbors(real_board, r, c)

    return real_board, user_board


def print_board(board):
    """
    function print board
    :param board: board of game
    :return: none
    """
    for i in range(len(board)):
        print("   +"+"---+"*len(board), end="\n")
        print(f"{i} ", " | ", end="", sep="")  # number of row
        for j in range(len(board)):
            print(board[i][j], end=" | ")
        print()
    for i in range(len(board)):
        if i == 0:
            print("     ", end="")
        print(i, end="   ")  # number of column
    print()
    print()


def player_choose(board):
    """
    The function receives from the user index of row and column and return the values
    :param board: board of the game
    :return: row, col
    """
    row, col = input('Please enter index (row col) to insert: ').split()
    while not valid_index(board, row, col):
        print('Invalid index')
        row, col = input('Please enter index (row col) to insert: ').split()
    return int(row), int(col)


def is_win(user_board, mine_num):
    """
    function return True if user win the game
    :param user_board: the board to display
    :param mine_num: num of mine in the real board
    :return: True if user win, otherwise False
    """
    spaces = 0
    for row in user_board:
        spaces += row.count(" ")
    return spaces == mine_num


def play(real_board, user_board, mine_num):
    """
    minesweeper main function
    :param real_board: the real board
    :param user_board: the board to display the user with his choice
    :param mine_num: number of mine in real board
    :return: none
    """
    endGame = False

    while not endGame:
        print_board(user_board)
        idxR, idxC = player_choose(real_board)
        if is_mine(real_board, idxR, idxC):
            endGame = True
            print_board(real_board)
            print("Oops! it's a mine.")
        elif real_board[idxR][idxC] == 0:
            reveal_zeros(real_board, user_board, idxR, idxC)
            endGame = is_win(user_board, mine_num)
            if endGame:
                print_board(user_board)
                print("You win!")
        else:
            user_board[idxR][idxC] = real_board[idxR][idxC]
            endGame = is_win(user_board, mine_num)
            if endGame:
                print_board(user_board)
                print("You win!")


def main():
    board_size = input("Enter size of board (a number, maximum 9): ")
    mine_num = input("Enter number of mines (a number, maximum board-size*2): ")

    if not is_int(board_size) or not is_int(mine_num) or \
            not 3 <= int(board_size) <= 9 or not int(mine_num) <= 2*int(board_size):
        print("Invalid input")
        return
    print("Please enter the index in format number*space*number")

    board_size = int(board_size)
    mine_num = int(mine_num)
    real_board, user_board = create_boards(board_size, mine_num)
    play(real_board, user_board, mine_num)


main()
