import random
import time

def printBoard(board):
    """Print the game board"""

    txt = f"""    
         |     |     
      {board[0]}  |  {board[1]}  |  {board[2]}  
    _____|_____|_____
         |     |     
      {board[3]}  |  {board[4]}  |  {board[5]}  
    _____|_____|_____
         |     |     
      {board[6]}  |  {board[7]}  |  {board[8]}  
         |     |     
    """
    print(txt)

def isWinner(player, board):
    """Return True if the player has win. False otherwise"""

    # Rows
    if board[0] == board[1] == board[2] == player:
        return True
    elif board[3] == board[4] == board[5] == player:
        return True
    elif board[6] == board[7] == board[8] == player:
        return True

    # Columns
    elif board[0] == board[3] == board[6] == player:
        return True
    elif board[1] == board[4] == board[7] == player:
        return True
    elif board[2] == board[5] == board[8] == player:
        return True

    # Diagonals
    elif board[0] == board[4] == board[8] == player:
        return True
    elif board[2] == board[4] == board[6] == player:
        return True

    return False

def checkPosition(position, board):
    """Return True if position is valid. False otherwise"""
    return True if 0 <= position <= 8 and board[position] == " " else False

def isBoardFull(board):
    """Return True if board is full. False otherwise"""

    for i in range(len(board)):
        if board[i] == " ":
            return False
    return True

def clearBoard():
    """Return an empty board"""
    return [" " for _ in range(9)]

def intro():
    """Print the intro for the TicTacToe Game"""

    print("Welcome to TicTacToe Game.\nNOTE: to chose where to play write the number of the box. As following:")
    print(f"""    
         |     |     
      1  |  2  |  3 
    _____|_____|_____
         |     |     
      4  |  5  |  6
    _____|_____|_____
         |     |     
      7  |  8  |  9  
         |     |     
    """)
    print("Game Started:")
        
def move(player, position, board):
    """Try to make the move and return True if the move success. False otherwise"""

    try:
        if checkPosition(int(position)-1, board):
            board[int(position)-1] = player
            return True
    except:
        return False
    return False
        
def isGameFinish(player, board):
    """Check if the game finish under two condition. Player wins or board is full (Tie game). If the game finish
    will return the answer of the user to continue playing or not (Answer = [yes, y, no, n])"""

    finish = True if isWinner(player, board) else False
    if finish:
        print(f"GG the Winner is {player}!")
                
    elif isBoardFull(board):
        print("Tie! no one wins :(")
        finish = True

    if finish:
        while True:
            answer = input("Want to play again? (YES/NO): ").lower()
            if not(answer == "n" or answer == "no" or answer == "y" or answer == "yes"):
                print("ERROR: Please enter a valid option. Try again")
            else:
                break
        return answer

def allPossibleMoves(board):
    """Return all possible moves that could play on the current board"""
    
    return [i for i in range(len(board)) if checkPosition(i, board)]

def easyAI(board):
    """Potato mode"""
    possibleMoves = allPossibleMoves(board)
    randomMove = random.choice(possibleMoves) + 1
    move("o", randomMove, board)
    
def impossibleAI(board):
    """Hey, you can NOT win... I'm NOT joking!!!"""
    
    bestMove = calculateAllMoves(board, True, 0) + 1
    move("o", bestMove, board)
    
def calculateAllMoves(board, isMax, depth):
    """Calculate all possible moves with path for each one using minimax. Where the O is the maximizing player and X is the minimizing player. Finally, return the best move ever"""
    
    if isWinner("o", board):
        return 10
    if isWinner("x", board):
        return -10
    if isBoardFull(board):
        return 0
        
    if isMax:
        scoresList = []
        for possibleMove in allPossibleMoves([i for i in board]):
            copyBoard = [i for i in board]
            if move("o", possibleMove+1, copyBoard):
                scoresList.append([calculateAllMoves(copyBoard, False, depth+1), possibleMove])
                
        if depth == 0:
            maxValue = [-100, -100]
            for score in scoresList:
                if score[0] > maxValue[0]:
                    maxValue[0], maxValue[1] = score[0], score[1]
            return maxValue[1]
        
        return max([score[0] for score in scoresList])

    else:
        scoresList = []
        for possibleMove in allPossibleMoves([i for i in board]):
            copyBoard = [i for i in board]
            if move("x", possibleMove+1, copyBoard):
                scoresList.append([calculateAllMoves(copyBoard, True, depth+1), possibleMove])
                
        if depth == 0:            
            minValue = [100, 100]
            for score in scoresList:
                if score[0] < minValue[0]:
                    minValue[0], minValue[1] = score[0], score[1]
            return minValue[1]

        return min([score[0] for score in scoresList])
    
def ChooseDifficlty():
    while True:
        answer = input("Choose Difficlty (Eazy/Impossible): ").lower()
        if answer == "eazy" or answer == "impossible":
            return answer
        else:
            print("ERROR: invalid option. Please try again")

def delay():
    """Delay between human turn (X) and AI turn (O)"""
    
    print("Computer is thinking", end="")
    for _ in range(3):
        print(".", flush=True, end="")
        time.sleep(0.5)
    print()
    
def main():
    board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    intro()
    difficulty = ChooseDifficlty()
    printBoard(board) 
     
    #Start the game
    while True:

        #Check X play a valid move
        print("================================================")
        while True:
            isValidMove = move("x", input("Your move (1-9): "), board)
            if isValidMove == True:
                break
            else:
                print("ERROR: Invalid. Please try again!")

        printBoard(board)

        #Check if it's the game finish or not after X turn. If it's finish ask the player if he want to play again
        answer = isGameFinish("x", board)
        if answer == "n" or answer == "no":
            print("Thanks for playing :D")
            break   
        if answer == "y" or answer == "yes":
            difficulty = ChooseDifficlty()
            board = clearBoard()
            printBoard(board)
            continue       

        delay()

        #AI turn (O player)
        if difficulty == "eazy":
            easyAI(board)
        elif difficulty == "impossible":    
            impossibleAI(board)

        printBoard(board)  

        #Check if it's the game finish or not after O turn. If it's finish ask the player if he want to play again
        answer = isGameFinish("o", board)
        if answer == "n" or answer == "no":
            print("Thanks for playing :D")
            break

        if answer == "y" or answer == "yes":
            difficulty = ChooseDifficlty()
            print("Game Started Again:")
            board = clearBoard()
            printBoard(board)
            continue  
main()
