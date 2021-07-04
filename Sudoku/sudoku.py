board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

def solve(board):

    vacant_box = find_vacant(board) 
    if vacant_box == (-1, -1):
        return True
    else:
        row, col = vacant_box

    for val in range(1, 10):
        if is_valid(board, val, (row, col)):
            board[row][col] = val

            if solve(board):
                return True
            
            board[row][col] = 0
        
    return False


def is_valid(board, val, pos):
    row, col = pos
    #row
    for i in range(len(board[0])):
        if board[row][i] == val and col != i:
            return False
        
    #column
    for i in range(len(board)):
        if board[i][col] == val and row != i:
            return False
    
    #current box
    box_x = 3 * (col // 3)
    box_y = 3 * (row // 3)

    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] == val and (i, j) != pos:
                return False
    
    return True

def find_vacant(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    
    #no empty box
    return (-1, -1)


def print_board(board):
    print("- - - - - - - - - - - - - - -")
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0:
                print(" | ",end="")

            if j == len(board[0])-1:
                print(str(board[i][j]) + " | ", end="\n")
            else:
                print(str(board[i][j]) + " ", end="")
    print("- - - - - - - - - - - - - - -")
    
print("Original Board")
print_board(board)
solve(board)
print("Solved Board")
print_board(board)