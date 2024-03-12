from game2dboard import Board

turn = 0
placement_mode = True
selected_piece = None  # To store the coordinates of the selected piece


def column_check(board, column):  # list is the board list, column is the number of the column
    """Checks each column for a win"""
    token = board[2][column]  # in any column case a winning match will have the same color token in the central
    # space of the column
    count = 0

    if token is None:
        return None
    # In this part it goes from top to bottom and tries to count up the number of tokens with a winning
    # possibilities, the count is reset to 0 when a break in the chain is detected

    for i in range(5):
        if board[i][column] == token:
            count += 1

        elif board[i][column] != token and count < 4:
            count = 0

    if count == 4:
        with open('winner.txt', 'w') as file:
            file.write(f'{token}')
        return True


def row_check(board, row):
    """Checks each row for a win"""
    token = board[row][2]  # Same logic an in the column check
    count = 0

    if token is None:
        return None

    for i in range(5):
        if board[row][i] == token:
            count += 1
        elif board[row][i] != token and count < 4:
            count = 0

        if count == 4:
            with open('winner.txt', 'w') as file:
                file.write(f'{token}')
            return True


def diagonal_check(board):
    """Checks each diagonal for a win"""
    # 3 different sections, the code basically does the same on each section, they are just separated by how they move

    # Checking the 4 small diagonals
    start_diag = [[0, 0], [0, 4], [1, 0], [0, 1], [0, 3], [1, 4]]

    for i in range(2):
        x, y = start_diag[i + 2]  # List is out of wack but these
        token = board[x][y]
        # Left to right diags
        if token is None:  # if even one of the spaces is blank it won't work, so we may as well choose a random one
            # for the token
            continue
        for j in range(4):  # Iterate through all 4 spaces
            if board[x][y] != token:  # If one element is wrong it is not a win so just continue into the next phase
                break
            x += 1
            y += 1
        else:  # If the for loop completes without breaking then they win
            with open('winner.txt', 'w') as file:
                file.write(f'{token}')
            return True

    # Right to left small Diags
    for k in range(2):
        x, y = start_diag[k + 4]
        token = board[x][y]
        if token is None:
            continue
        for i in range(4):
            if board[x][y] != token:
                break
            x += 1
            y -= 1
        else:
            with open('winner.txt', 'w') as file:
                file.write(f'{token}')
            return True

    # Long diags
    x, y = start_diag[0]
    z, a = start_diag[1]
    token = board[x + 2][y + 2]
    # Token in the middle of the diag, impossible to complete a win if the token in the middle of the
    # diag is not the same as the winning color
    token2 = board[z + 2][a - 2]
    count = 0
    count2 = 0

    for m in range(5):
        if board[x][y] == token and token is not None:

            count += 1
        else:  # Reset count if token != List accounts for last 4 being right
            count = 0
        if board[z][a] == token2 and token2 is not None:
            count2 += 1
        else:
            count2 = 0

        if count == 4:
            with open('winner.txt', 'w') as file:
                file.write(f'{token}')
            return True
        elif count2 == 4:
            with open('winner.txt', 'w') as file:
                file.write(f'{token2}')
            return True
        x += 1
        y += 1
        z += 1
        a -= 1


def square_checker(board):
    """Checks the entire board for a win"""
    # Just iterate over every possible square
    for i in range(4):
        for j in range(4):
            if (board[0 + i][0 + j] == board[1 + i][0 + j] == board[0 + i][1 + j] == board[1 + i][1 + j] and
                    board[0 + i][0 + j] is not None):
                with open('winner.txt', 'w') as file:
                    file.write(f'{board[0 + i][0 + j]}')
                return True


def checkwin(board) -> True:  # board is the game board
    """This function returns True if a win is present"""
    board_list = board.copy()  # Board.copy returns a list of lists where each element is the name of the png at that
    # location

    for i in range(5):
        if column_check(board_list, i):
            return True
        elif row_check(board_list, i):
            return True
    if diagonal_check(board_list):
        return True
    elif square_checker(board_list):
        return True


def mouse_fn(btn, row, col) -> None:
    """This function places and moves the pieces using input from the mouse"""
    global turn, placement_mode, selected_piece

    if placement_mode:
        # Placement mode
        if (turn < 8) and not (b[row][col]):
            if turn % 2 == 0:
                b[row][col] = 2  # Black circle
            else:
                b[row][col] = 1  # Blue circle

            turn += 1

            if checkwin(b):
                b.close()
                with open('winner.txt', 'r') as file:
                    data = file.read()
                    if data == '2':
                        print("Black wins!")
                    else:
                        print("Blue wins!")

            if turn == 8:
                placement_mode = False  # Switch to movement mode

    else:
        # Movement mode
        if selected_piece is None:
            # If no piece is selected, check if the clicked square contains the correct color
            correct_color = 2 if turn % 2 == 0 else 1  # 2 for black, 1 for blue
            if b[row][col] == correct_color:
                selected_piece = (row, col)  # Record the selected piece
                b[row][col] = 3  # Mark the selected piece on the board

        else:
            # If a piece is already selected, check if the clicked square is a valid move
            if (
                    (abs(row - selected_piece[0]) <= 1 and abs(col - selected_piece[1]) <= 1)
                    and not b[row][col]
            ):
                # Set the square the piece is leaving to None (empty)
                b[selected_piece[0]][selected_piece[1]] = None

                # Place the correct black or blue piece based on the current turn
                if turn % 2 == 0:
                    b[row][col] = 2  # Black circle
                else:
                    b[row][col] = 1  # blue circle

                selected_piece = None

                if checkwin(b):
                    b.close()
                    with open('winner.txt', 'r') as file:
                        data = file.read()
                        if data == '2':
                            print("Black wins!")
                        else:
                            print("Blue wins!")

                turn += 1


print('Rules: \n'
      'Each player has 4 pieces \n'
      'Black starts by placing a piece anywhere on the board \n'
      'Blue then places their piece in an unoccupied square \n'
      'They take turns placing their 4 pieces \n'
      'When all pieces have been placed they can move a piece to an adjacent square \n'
      'Form a line of 4 or a small square to win \n')

print('Options: \n'
      'To close the game press the blue X on the top right of the game box \n'
      'To move a piece click the piece you wish to move and then click the square you want to move it to \n'
      'The game will display a win screen after a winner is decided \n')

# Create the board
b = Board(5, 5)
b.title = "Teeko"
b.cell_size = 80
b.cell_color = "white"
b.on_mouse_click = mouse_fn

# Show the board after all setup is complete
b.show()
