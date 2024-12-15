# This is Python's standard package GUI toolkit
import tkinter as visual

# Store player color
player_color = "w"

# records whether a piece has been moved in order of black king, 07 rook, 77 rook, white king, 70 rook and 00 rook (clockwise from black king)
moved = {"04":False,"00":False,"70":False,"74":False,"77":False,"07":False}

# stores last move
last_move = ["##","##"]

# Boolean: indicate if a king has been captured
king_captured = False

# dict: converts "b" and "w" to "Black" and "White"
color = {"w":"White","b":"Black"}

# 2d array: holds game state
grid_board = [["br","bp","##","##","##","##","wp","wr"],
              ["bn","bp","##","##","##","##","wp","wn"],
              ["bb","bp","##","##","##","##","wp","wb"],
              ["bq","bp","##","##","##","##","wp","wq"],
              ["bk","bp","##","##","##","##","wp","wk"],
              ["bb","bp","##","##","##","##","wp","wb"],
              ["bn","bp","##","##","##","##","wp","wn"],
              ["br","bp","##","##","##","##","wp","wr"]]

# Instantiate board visual
root = visual.Tk()
root.title("Chess Board")

# checks if given coordinate is inbounds
def inbounds(x,y):
    """ Returns either True or False for if the inputted coordinate exists in the 8x8 chess
    board grid."""
    return ((0 <= x <= 7) and (0 <= y <= 7))

# checks if square is occupied
def empty(board, x, y):
    """ Returns either True or False for if the selected square on the chess board is
    occupied by a piece. True if empty, false if the square is of any other value"""
    return board[x][y]=="##"        

# checks for returns True or False depending on whether or not a given input is valid and prints issue
def valid(input):
    """ Returns True or False depending on whether or not a given input is valid.
    Validity is defined by the following:
    Does the selected grid space represent a piece that the current player can move?
    It checks the following...
    Input is logical and valid (gridspace, ex: 18)
    Input represents a grid space in bounds
    Grid space is empty
    Piece on the grid space is the current player's """
    # checks if input is of size 2
    if len(input)!=2:
        print("User input is incorrect length")
        return False

    # checks if input is numerical and stores into respective variables, adjusting to index form
    try:
        x = int(input[0]) - 1
        y = int(input[1]) - 1
    except:
        print("User input is not numerical")
        return False

    # checks if this grid space is within bounds
    if not inbounds(x,y):
        print("This square is out of bounds")
        return False

    # Check if the grid space is empty
    if empty(grid_board, x, y):
        print("There's no piece on this grid space.")
        return False

    # Check if the grid space is of the player's color
    if player_color != grid_board[x][y][0]:
        print("This isn't your piece. You can't move it.")
        return False

    # else, returns true
    return True


# creates a list of possible squares current selected 
def move_logic(board, piece, x, y):
    """ Given a gridspace with a piece on it, this function
    calculates all possible movement options for that piece.
    These options are returned in a list. """
    valid_moves=[]
    if piece[0]=="w":
        flip = 1
    else:
        flip = -1

    if piece[1] == "p": # if pawn (won't have to check for vertical out of bounds since pawns can't go backwards and will promote if ever on the back rank)
        if empty(board, x, y-1*flip): # if space directly in front of pawn is empty
            valid_moves.append([x,y-1*flip])
            if y == int(3.5+2.5*flip) and empty(board, x, y-2*flip): # if first move fo this pawn, move twice is option
                valid_moves.append([x,y-2*flip])
        if 0<=x-1 and not empty(board, x-1, y-1*flip) and board[x-1][y-1*flip][0] != piece[0]: # if piece is available to capture to the pawns front left
            valid_moves.append([x-1,y-1*flip])
        if 7>=x+1 and not empty(board, x+1, y-1*flip) and board[x+1][y-1*flip][0] != piece[0]: # if piece is available to capture to the pawns front right
            valid_moves.append([x+1,y-1*flip])
        if last_move[0][1] == "p" and abs(last_move[3]-last_move[2]) == 2 and y==last_move[3] and abs(x-last_move[1])==1: # if en pessant is available
            valid_moves.append([last_move[1],y-1*flip])

    if piece[1] == "k": # if king
        valid_moves=[[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]]
        for i in valid_moves: # someone double check my stuff, especially this for loop but this loop should remove all out of bound options and check for blocked spaces
            if not inbounds(i[0],i[1]): # checks if any potential moves are out of bounds
                valid_moves.remove(i)
            elif board[i[0]][i[1]][0] == piece[0]: # checks if any same color pieces are blocking any potential moves
                valid_moves.remove(i)
        if not moved[str(int(3.5+3.5*flip))+"4"]: # checks if posssible to castle
            if not moved[str(int(3.5+3.5*flip))+"7"]:
                for i in range(5,7):
                    if not empty(board,i,int(3.5+3.5*flip)):
                        break
                else:
                    valid_moves.append([6,y])
            if not moved[str(int(3.5+3.5*flip))+"0"]:
                for i in range(1,4):
                    if not empty(board,i,int(3.5+3.5*flip)):
                        break
                else:
                    valid_moves.append([2,y])

    if piece[1] == "n": # if knight
        valid_moves=[[x-2,y-1],[x-2,y+1],[x+2,y-1],[x+2,y+1],[x-1,y-2],[x+1,y-2],[x-1,y+2],[x+1,y+2]]
        for i in valid_moves[::-1]: # someone double check my stuff, especially this for loop but this loop should remove all out of bound options and check for blocked spaces
            # print(board[i[0]][i[1]][0]) # remove
            if not inbounds(i[0],i[1]): # checks if any potential moves are out of bounds
                valid_moves[valid_moves.index(i)] = ""
            elif board[i[0]][i[1]][0] == piece[0]: # checks if any same color pieces are blocking any potential moves
                valid_moves[valid_moves.index(i)] = ""
        # Remove all empty strings that may have been created here
        while True:
            if "" in valid_moves:
                valid_moves.remove("")
            else:
                break

    if piece[1] == "b" or piece[1] == "q": # if bishop or queen
        for i in range(1,8): # checks lower right diagonal
            if not inbounds(x+i,y+i):
                break
            if empty(board,x+i,y+i): # if open
                valid_moves.append([x+i,y+i])
            elif board[x+i][y+i][0] != piece[0]: # if captureable piece
                valid_moves.append([x+i,y+i])
                break
            else:
                break
        for i in range(1,8):# checks upper right diagonal
            if not inbounds(x+i,y-i):
                break
            if empty(board,x+i,y-i):
                valid_moves.append([x+i,y-i])
            elif board[x+i][y-i][0] != piece[0]:
                valid_moves.append([x+i,y-i])
                break
            else:
                break
        for i in range(1,8):# checks lower left diagonal
            if not inbounds(x-i,y+i):
                break
            if empty(board,x-i,y+i):
                valid_moves.append([x-i,y+i])
            elif board[x-i][y+i][0] != piece[0]:
                valid_moves.append([x-i,y+i])
                break
            else:
                break
        for i in range(1,8):# checks upper left diagonal
            if not inbounds(x-i,y-i):
                break
            if empty(board,x-i,y-i):
                valid_moves.append([x-i,y-i])
            elif board[x-i][y-i][0] != piece[0]:
                valid_moves.append([x-i,y-i])
                break
            else:
                break

    if piece[1] == "r" or piece[1] == "q": # if rook or queen
        for i in range(1,8): # checks down line
            if not inbounds(x,y+i):
                break
            if empty(board,x,y+i): # if open
                valid_moves.append([x,y+i])
            elif board[x][y+i][0] != piece[0]: # if captureable piece
                valid_moves.append([x,y+i])
                break
            else:
                break
        for i in range(1,8):
            if not inbounds(x,y-i):
                break
            if empty(board,x,y-i):
                valid_moves.append([x,y-i])
            elif board[x][y-i][0] != piece[0]:
                valid_moves.append([x,y-i])
                break
            else:
                break
        for i in range(1,8):
            if not inbounds(x-i,y):
                break
            if empty(board,x-i,y):
                valid_moves.append([x-i,y])
            elif board[x-i][y][0] != piece[0]:
                valid_moves.append([x-i,y])
                break
            else:
                break
        for i in range(1,8):
            if not inbounds(x+i,y):
                break
            if empty(board,x+i,y):
                valid_moves.append([x+i,y])
            elif board[x+i][y][0] != piece[0]:
                valid_moves.append([x+i,y])
                break
            else:
                break

    for i in range(len(valid_moves)): # reformats
        valid_moves[i] = str(valid_moves[i][0])+str(valid_moves[i][1])
    return valid_moves


def update_board(board):
    """ Updates the visual board created through the ptinker module
    On a technical level, the current visual is destroyed (if it exists)
    And a new one is made that represents the current data stored in the chess
    grid"""

    # Clear out any old boards
    for old_board in root.winfo_children():
        old_board.destroy()

    # Colors for the board
    light_square = "#F0D9B5"
    dark_square = "#B58863"

    # Chess symbols for display
    symbols = {
        "br": "♜", "bn": "♞", "bb": "♝", "bq": "♛", "bk": "♚", "bp": "♟",
        "wr": "♖", "wn": "♘", "wb": "♗", "wq": "♕", "wk": "♔", "wp": "♙"
    }

    # Canvas to draw the chessboard
    canvas = visual.Canvas(root, width=425, height=425)
    canvas.pack()

    # Draw the board
    for col in range(8):
        for row in range(8):
            if (row + col) % 2 == 0:
                square_color = light_square
            else:
                square_color = dark_square

            x1, y1 = col * 50+15, row * 50+15
            x2, y2 = x1 + 50, y1 + 50

            # Draw square
            canvas.create_rectangle(x1, y1, x2, y2, fill=square_color, outline="")

            # Draw piece if present
            # Flip the row and column indices to match the desired visual orientation
            piece = board[col][row]
            if piece != "##":
                canvas.create_text(
                    x1 + 25, y1 + 25, text=symbols[piece], font=("Arial", 24),
                    fill="black" if piece[0] == "b" else "white"
                )
    # draw the row and column labels
    for i in range(8):
        # row on left
        canvas.create_text(9, i * 50 + 40, text=str(i + 1), font=("Arial", 14), fill="black")
    for i in range(8):
        # column on top
        canvas.create_text(i * 50 + 40, 9, text=str(i+1), font=("Arial", 14), fill="black")

    
    # Display the window and process events
    root.update()


    """# DEBUG: Prints the board to the console
    # Assume (correctly) that board is a 2D rectangular array
    print()
    print("", end="  ")
    vis_row_num = 1
    # Define column length by number of columns in first row
    # Print column number guide
    for col in range(1, len(board[0]) + 1):
        print(f"{col}", end = "  ")
    print()
    for col in range(len(board[0])):
        # Iterate through all rows
        for row in range(len(board)):
            # Print row number guide
            if row == 0:
                print(f"{vis_row_num}", end=" ")
                vis_row_num += 1
            print(f"{board[row][col]}", end=" ")
        print()
    print()"""


def save_board(curr_player, board):
    """ Saves the current board in a file and the player who is currently taking a turn
    in the fun_game.sav file """
    with open("fun_game.sav", "w") as save_file:
        # Save the current player
        save_file.write(f"{curr_player}\n")
        # Save the current board so that it can later be loaded
        for itr_row in range(len(board)):
            # Join the elements in each row of the board into one string with commas
            curr_row = ",".join(board[itr_row])
            save_file.write(curr_row)
            # Only go to next line if this isn't the last row in the board
            if not (itr_row >= len(board) - 1):
                save_file.write("\n")

    # Notify of successful save
    print("Game saved to fun_game.sav")


def load_board():
    """ Loads the board as is saved in fun_game.sav.
    If this file does not exist, there is no saved data. """
    try:
        with open("fun_game.sav", "r") as save_file:
            # Update global variables for the player
            global player_color
            # Update the globally stored board
            global grid_board
            update_grid_board = []
            for line in save_file:
                # The line storing the player color is only len=1, unlike a row of the board
                if len(line.strip()) == 1:
                    # Update player color
                    player_color = line.strip()
                # Otherwise, this is a line of the grid
                else:
                    # Get a row for the grid by splitting on commas in one line
                    parse_line = line.strip()
                    update_grid_board.append(parse_line.split(","))
            # Update the board
            grid_board = update_grid_board

            # Print a message if the update was successful
            print("Game loaded from fun_game.sav")
    except FileNotFoundError:
        # Message indicating there is no save file
        print("There is no fun_game.sav. Have you saved your game before?")

#first display player rules
print("Welcome to Chess!")
print("Here are the rules and instructions for playing:")
print("1. This is a two-player game between Black and White.")
print("2. To select a piece, input its grid space as two digits (e.g., '18').")
print("3. Only your pieces can be moved. You cannot move the opponent's pieces.")
print("4. To move a piece, input the target grid space as two digits (e.g., '28').")
print("5. You can save the game by typing 'save' and load a saved game by typing 'load'.")
print("6. Special rules, like castling, pawn promotion, and en passant, are implemented.")
print("7. The game ends when one player's king is captured.")
print("8. If you want to reselect a piece during your turn, type 'back'.")
print("Enjoy the game, and may the best player win!")

"""Main game loop"""
while True:
    print()
    # Update the board, visually
    update_board(grid_board)
    # Prompt current player to input a cell of interest.
    # This is a 8x8 grid. The expectation is that the player will input some configuration of
    # {1-8}{1-8} to select a piece on the grid.
    print(f"It's {color[player_color]}'s turn. Please choose a grid space.")
    print("Grid spaces are represented as {1-8}{1-8}. For example, one valid grid space is '18'.")
    print("Additionally, either save or load your game by typing 'save' or 'load'")
    gridspace_input = input("Input your grid space: ")

    # Check if the user has indicated if they want to save
    if gridspace_input == "save":
        # If this function runs successfully, it will be printing a message indicating that.
        save_board(player_color, grid_board)
        continue

    if gridspace_input == "load":
        # If this function runs successfully, it will be printing a message indicating that.
        # All load_board does is set the board and player color to specific values...
        # So this main game loop must be restarted when that occurs with continue
        load_board()
        continue

    # Check for valid input
    if not valid(gridspace_input):
        print("Please try again.")
        continue

    # Interpret grid space
    grid_x = int(gridspace_input[0]) - 1
    grid_y = int(gridspace_input[1]) - 1



    # Parse selected grid space (we're now assuming that it is a valid, non-empty,
    # current player's color, grid space)
    gridspace_data = grid_board[grid_x][grid_y]

    # Get possible valid movement options
    valid_moves = move_logic(grid_board, gridspace_data, grid_x, grid_y)

    # Prompt user to input a space for the piece to move to
    # Check if the user inputs "back" to run another iteration of the while loop
    # check if valid_moves has elements
    move_to_gridspace_usr = input("Input the grid space where you want this piece to move: ")


    # Check for valid input... only consider if the input can be properly converted
    try:
        new_grid_x = int(move_to_gridspace_usr[0]) - 1
        new_grid_y = int(move_to_gridspace_usr[1]) - 1
    except:
        # Print differing methods based upon if invalid input was intentional ("back") or unintentional
        if move_to_gridspace_usr == "back" or move_to_gridspace_usr == "Back":
            print("Ok, go ahead and select a grid space again.")
        else:
            print("This input is invalid.")
        # Force while loop to end
        continue

    # Convert to proper form to be interpreted
    move_to_gridspace = str(f"{new_grid_x}{new_grid_y}")

    if move_to_gridspace in valid_moves:
        # Piece has moved. Set user selected position to be empty
        grid_board[grid_x][grid_y] = "##"

        # checks for castling and moves rook
        if gridspace_data[1] == "k" and abs(grid_x-new_grid_x)==2:
            # print()
            grid_board[(grid_x+new_grid_x)//2][grid_y] = player_color+"r"
            grid_board[new_grid_x//4*7][grid_y] = "##"

        # Set the flag to true if the game has been won, if the king has been felled
        if grid_board[new_grid_x][new_grid_y][1] == "k":
            king_captured = True
        # Promote a pawn if it's on the opponent's side
        # If it's a pawn...
        if gridspace_data[1] == "p":
            # checks for enpessant (change in x value [capture] and no piece in area moved)
            if new_grid_x != grid_x and grid_board[new_grid_x][new_grid_y]=="##":
                grid_board[new_grid_x][grid_y]="##"

            # Check (and possibly perform) promotion
            elif (gridspace_data[0] == "w" and new_grid_y == 0) or (gridspace_data[0] == "b" and new_grid_y == 7):
                # Promote by modifying gridspace data to have the pawn become a queen.
                # I mean, TECHNICALLY, you could promote the pawn to a rook or bishop... but who wants that?!
                gridspace_data = f"{gridspace_data[0]}q"

        # Set the grid space the user moved the piece to, to now be what the old space was
        grid_board[new_grid_x][new_grid_y] = gridspace_data

    elif move_to_gridspace == "back" or move_to_gridspace == "Back":
        print("Ok, go ahead and select a grid space again.")
        # Force another iteration of the while loop
        continue
    else:
        print("That's not a valid move.")
        # Force another iteration of the while loop
        continue

    # updates last move
    last_move = [gridspace_data,grid_x,grid_y,new_grid_y]

    # updates if a piece of interest has moved
    if str(last_move[1])+str(last_move[2]) in moved:
        moved[str(last_move[1])+str(last_move[2])] = True


    # Final check: End the game if a player won
    if king_captured:
        # Get the proper full player name from the dictionary
        player_name = color[player_color]
        print()
        print(f"{player_name} has won. From the rubble of their opponent's kingdom, they emerge.")
        print(f"For now, {player_name} is the dominant monarchy.")
        print("Who will be next to oppose their wrath...?")
        break

    # If another round is to happen, switch player color
    if player_color == "w":
        player_color = "b"
    else:
        player_color = "w"

