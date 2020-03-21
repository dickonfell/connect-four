"""
Programming with Python MATH20621
Dickon Fell              10299169
---------------------------------
Connect 4 Coursework Module:
    This module defines a number of functions which are amalgamated in the final play()
    function resulting in a playable connect 4 game, with the additional ability to load
    and save games using text files, and play against a computer opponent.
    The game is played by 2 players taking alternate turns to place pieces in a 6x7 grid
    with the win condition of placing four of your pieces in a row, horizontally, vertically
    or diagonally. A draw is when the board is full and no player has won. Comments can be
    read along the code explaining each part as necessary. Have fun playing!
"""

from copy import deepcopy

def newGame(player1, player2):  # task 1
    
    """ 
    Defines a dictionary containing the initial 
    conditions of the game.
    
    Parameters:
        player1, player2 -- string parameters
        corresponding to the player names.
        
    Returns:
        game -- a dictionary defining the state
        of the game at any given time.
    """
       
    game = {
        'player1' : 'C', #X
        'player2' : 'C', #O
        'who' : 1,
        'board' : [ [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0] ]
            }
    
    game['player1'] = player1
    game['player2'] = player2
    
    return game


def printBoard(board):      # task 2
    
    """
    Uses formatting to turn the 'board' value in our 
    game dictionary into an easy to read game board 
    which it prints.
    
    Parameters:
        board -- a list of lists with the same format
        as that seen in our game dictionary.
    """
    
    print("\n|1|2|3|4|5|6|7|\n"+
          "+-+-+-+-+-+-+-+")
    
    for i in range(6):
        args = list()
        for j in range(7):
            if board[i][j] == 0:
                args.append(" ")
            elif board[i][j] == 1:
                args.append("X")
            elif board[i][j] == 2:
                args.append("O")
        print("|{}|{}|{}|{}|{}|{}|{}|".format(*args))
        
    print("\n")
    

def getValidMoves(board):       # task 3
    
    """
    Returns a list of integers corresponding to 
    the columns left in play on the game board.
    
    Parameters:
        board -- a list of lists with the same format
        as that seen in our game dictionary.
        
    Returns:
        validc -- a list of integers between 0 and 6.
    """
        
    validc = list()     #start with an empty list ie. assume all columns are full.
        
    for i in range(7):  
        if board[0][i] == 0:    #check for each column that it is empty by checking the top row.
            validc.append(i)    #this works as we will never have empty spaces below an already full one.
                
    return validc
   
    
def makeMove(board, move, who):     # task 4
    
    """
    Transforms the player input of a turn into a 
    space on the board being filled.
    
    Parameters:
        board -- a list of lists with the same format
        as that seen in our game dictionary.
        
        move -- and integer between 0 and 6.
        
        who -- an integer with possible values 1 or 2.
        
    Returns:
        board -- the updated board variable.
    """
    
    k = 5
    
    while board[k][move] != 0:      #finds the first available row to place our turn.
        k -= 1
        
    board[k][move] = who
    
    return board


def hasWon(board, who):             # task 5
    
    """
    Checks possible win scenarios by analysing the 
    coordinates of the board in various orientations.
    
    Parameters:
        board -- a list of lists with the same format
        as that seen in our game dictionary.
        
        who -- and integer with possible value 1 or 2.
        
    Returns:
        bool -- True if the player with number 'who'
        occupies four adjacent positions forming a
        horizontal, vertical or diagonal line.
        False otherwise.
    """
    
    # the idea for the general structure of this function was formed with help from
    # https://stackoverflow.com/questions/29949169/python-connect-4-check-win-function
    
    for i in range(6):          #checks horizontally
        for j in range(4):
            if board[i][j] == who and board[i][j+1] == who and board[i][j+2] == who and board[i][j+3] == who:
                return True

    for j in range(7):          #checks vertically
        for i in range(3):
            if board[i][j] == who and board[i+1][j] == who and board[i+2][j] == who and board[i+3][j] == who:
                return True

    for i in range(5, 2, -1):   #checks upper right diagonal
        for j in range(4):
            if board[i][j] == who and board[i-1][j+1] == who and board[i-2][j+2] == who and board[i-3][j+3] == who:
                return True

    for i in range(5, 2, -1):   #checks upper left diagonal
        for j in range(6, 2, -1):
            if board[i][j] == who and board[i-1][j-1] == who and board[i-2][j-2] == who and board[i-3][j-3] == who:
                return True
    
    return False                #otherwise


def suggestMove1(board, who):       # task 6
    
    """
    Uses simple checks to win, or prevent a win by
    the other player if possible by finding which
    column to place a turn. Otherwise chooses
    the first possible move.
    
    Parameters:
        board -- a list of lists with the same format
        as that seen in our game dictionary.
        
        who -- an integer with possible values 1 or 2.
        
    Returns:
        i -- an integer belonging to the list of
        valid moves at the start of the turn.
    """
    
    
    if who == 2:
        other = 1
    else:
        other = 2
        
    validc = getValidMoves(board)       
    

    
    for i in validc:        #checks for a possible win
        board2 = deepcopy(board)        #needs to be inside the loop so we start each check with the same conditions
        boardi = makeMove(board2, i, who)
        if hasWon(boardi, who) == True:
            return i
    
        
    for i in validc:        #checks for a possible opponent win
        board2 = deepcopy(board) 
        boardi = makeMove(board2, i, other)
        if hasWon(boardi, other) == True:
            return i
        
    
    return validc[0]        #otherwise returns the first possible valid move.


def loadGame(filename):    # task 8
    
    """
    Defines a game dictionary from the specified text
    file, while checking that the file is compatible.
    
    Parameters:
        filename -- a string, the name of the file 
        desired.
        
    Returns:
        game -- a dictionary defining the state
        of the game at any given time.
    """
    
    if filename == "":
        filename = "game.txt"
    
    game = list()
    keys = ["player1", "player2", "who", "board"]
    
    try:
        
        f = open(str(filename), mode = "rt", encoding = "utf8")
        for line in f:
            line = str(line).rstrip("\n")
            game.append(line)
         
           
        gameb = game[3:]               #splits the list so the board is in its own list
        game = game[:3]
        
        
        if game[2] != '1' and game[2] != '2':
            raise ValueError("'who' value is not an integer 1 or 2.")
        else:
            game[2] = int(game[2])      #changing variable type of 'who'
            
        
        #gameb = ['0,0,0,0,0,0,0', '0,0,0,0,0,0,0', ...]
        for i in range(6):          #turns string of numbers into a list
            k = gameb[i]
            gameb[i] = k.split(",")
        
        for i in range(6):          #turns each list of strings into a list of integers
            for j in range(7):      
                if gameb[i][j] == '0' or gameb[i][j] == '1' or gameb[i][j] == '2':
                    gameb[i][j] = int(gameb[i][j])
                else:               #checking that values are all correct
                    raise ValueError("Board positions must be an integer 0, 1 or 2.")
        
        f.close()
        
    except FileNotFoundError:
        print("That file cannot be loaded.")
    except ValueError:
        print("This file is incompatible.")
    else:
        game = dict(zip(keys, game))    #entering values into game dictionary
        game['board'] = gameb
        return game
        

def saveGame(game, filename):   # task 9
    
    """
    Saves a game to the working directory in the form of a 
    text file of the format which the loadGame function
    is designed to open.
    
    Parameters:
        game -- a dictionary defining the state
        of the game at any given time.
        
        filename -- a string, the name of the file 
        desired.
    """
    
    if filename == "":
        filename = "gamesave.txt"
    else:
        filename += ".txt"
        
    
    with open(filename, mode = "wt", encoding = "utf8") as f:
        seq = [game['player1']+"\n", game['player2']+"\n", str(game['who'])+"\n"]
        board = game['board']
        for i in range(6):
            for j in range(7):
                board[i][j] = str(board[i][j])
            line = ",".join(board[i])+"\n"
            seq.append(line)
        f.writelines(seq)
    

def threeInRow(board, who):            
    
    """
    Checks possible 3 in a row scenarios by analysing the 
    coordinates of the board in various orientations.
    For use with the updated suggestMove2 function.
    
    Parameters:
        board -- a list of lists with the same format
        as that seen in our game dictionary.
        
        who -- and integer with possible value 1 or 2.
        
    Returns:
        bool -- True if the player with number 'who'
        occupies 3 adjacent positions forming a
        horizontal, vertical or diagonal line.
        False otherwise.
    """
    
    for i in range(6):          #checks horizontally
        for j in range(5):
            if board[i][j] == who and board[i][j+1] == who and board[i][j+2] == who:
                return True

    for j in range(7):          #checks vertically
        for i in range(4):
            if board[i][j] == who and board[i+1][j] == who and board[i+2][j] == who:
                return True

    for i in range(5, 1, -1):   #checks upper right diagonal
        for j in range(5):
            if board[i][j] == who and board[i-1][j+1] == who and board[i-2][j+2] == who:
                return True

    for i in range(5, 1, -1):   #checks upper left diagonal
        for j in range(6, 1, -1):
            if board[i][j] == who and board[i-1][j-1] == who and board[i-2][j-2] == who:
                return True
    
    return False                #otherwise


def suggestMove2(board, who):       # task 11
    
    """
    An updated verson of the previously defined suggestMove1
    (which returns a suggested move for a computer opponent
    to make given a board state as input), with a somewhat 
    more advanced playing strategy.

    Parameters:
        board -- a list of lists with the same format
        as that seen in our game dictionary.
        
        who -- an integer with possible values 1 or 2.
        
    Returns:
        i -- an integer belonging to the list of
        valid moves at the start of the turn.
    """
    
    #the playing strategy I have gone for also tries to make 3 in a row
    #using an updated version of the hasWon function, and also tries to
    #block 3 in a row by the opponent. When possible it also places its
    #pieces as close to the centre as possible as this gives it a better
    #chance of winning in the long run.
    
    
    if who == 2:
        other = 1
    else:
        other = 2
        
    validc = getValidMoves(board)       
    

    
    for i in validc:        #checks for a possible win
        board2 = deepcopy(board)        #needs to be inside the loop so we start each check with the same conditions
        boardi = makeMove(board2, i, who)
        if hasWon(boardi, who) == True:
            return i
    
        
    for i in validc:        #checks for a possible opponent win
        board2 = deepcopy(board) 
        boardi = makeMove(board2, i, other)
        if hasWon(boardi, other) == True:
            return i
        
        
    for i in validc:        #check for possible 3 in a row
        board2 = deepcopy(board)
        boardi = makeMove(board2, i, who)
        if threeInRow(boardi, who) == True:
            return i
        
        
    for i in validc:        #checks for a possible opponent 3 in a row
        board2 = deepcopy(board) 
        boardi = makeMove(board2, i, other)
        if threeInRow(boardi, other) == True:
            return i
        
        
    try:                    #if none of above have returned, it tries to place a piece in the centre
        mid = float(len(validc))/2
        if mid % 2 != 0:
            return validc[int(mid - 0.5)]
        else:
            return validc[int(mid-1)]
    except IndexError:
        return validc[0]    #otherwise returns the first possible valid move.

    
# ------------------- Main function --------------------
def play():
    
    """ 
    This function has no input/returns. It controls 
    the flow of the game using loops and user inputs.
    """
    
    #formatting the game start to look nice
    print("*" * 39)
    print(" " + "-"*3 + "="*4 + " Dickon's Connect Four " + "="*4 + "-"*3)
    print("*" * 39)
    
    #asking player names
    p1 = input("Input your name for Player 1. \n('C' for computer, 'L' to load a game). \n\n--> ").strip().capitalize()
    while p1 == "":
        print("An empty string is an invalid name. Please try again.\n")
        p1 = input("Input your name for Player 1. \n('C' for computer, 'L' to load a game). \n\n--> ").strip().capitalize()
    
    if p1 == 'L':
            game = loadGame(input("What is the file name of the game you want to load? "))
    else:
        p2 = input("Input your name for Player 2. \n('C' for computer). \n\n--> ").strip().capitalize()
        while p2 == "":
            print("An empty string is an invalid name. Please try again.\n")
            p2 = input("Input your name for Player 2. \n('C' for computer). \n\n--> ").strip().capitalize()
        
        game = newGame(p1, p2)
    
    #game start
        
    try:
        
        while hasWon(game['board'], 1) == False and hasWon(game['board'], 2) == False:
            
            board = game['board']
            who = game['who']
            validc = getValidMoves(board)
            
            printBoard(board)
            
            #input if user is a human
            if game['player'+str(who)] != 'C':
                
                while True:
                    try:                    #making move on board, accounts for exceptions        
                        move = input(game['player'+str(who)] + ": Which column to place your turn? ")
                        if move.isdigit():
                            move = int(move) - 1
                            game['board'] = makeMove(board, move, who)
                        elif move == "S" or move == "s":
                            game2 = deepcopy(game)
                            saveGame(game2, input("Name the file: "))
                        else:
                            raise ValueError
                    except ValueError:
                        print("\n... I said which column?")
                    except IndexError:
                        print("\nThat column is invalid.")
                    else:     
                        if game['who'] == 1:
                            game['who'] += 1
                        else:
                            game['who'] -= 1
                        break
                    
            if validc == list():
                break
            
            #move if user is a computer
            elif game['player'+str(who)] == 'C':
                
                print("Computer is taking a turn... \n")
                move = suggestMove2(board, who)
                game['board'] = makeMove(board, move, who)
                
                if game['who'] == 1:
                    game['who'] += 1
                else:
                    game['who'] -= 1
                    
            if validc == list():
                break
         #play loop ends
        
        #final game state messages
        if validc == list() and hasWon(game['board'], 1) == False and hasWon(game['board'], 2) == False:
            print("It's a draw!")
            printBoard(game['board'])
        else:
            if hasWon(game['board'], 1) == True and game['player1'] != 'C':
                print(game['player1'] + " has won!")
                printBoard(game['board'])
            elif hasWon(game['board'], 1) == True:
                print("Computer has won!")
                printBoard(game['board'])
                
            if hasWon(game['board'], 2) == True and game['player2'] != 'C':
                print(game['player2'] + " has won!")
                printBoard(game['board'])
            elif hasWon(game['board'], 2) == True:
                print("Computer has won!")
                printBoard(game['board'])
                #print("Congratulations, you've lost to a program that is (and I quote), 'at best at the playing level of a small child.'")
                
            
    except TypeError:
        print("Failed to initiate game.")
            
    
# ---------------- END -----------------------
    

# the following allows your module to be run as a program
if __name__ == '__main__' or __name__ == 'builtins':
    play()

