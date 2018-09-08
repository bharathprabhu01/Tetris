# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
import random
import copy

####################################
# customize these functions
####################################


####### Model ######################

def init(data):
    # initialise rows and cols
    data.rows = 15
    data.cols = 10
    # initliase margin for the board
    data.margin = 40
    # margin between black and blue cell on board
    data.cellMargin = 4
    data.cellSize = 40
    # to make the board
    data.emptyColor = "blue"
    data.board = [[data.emptyColor for col in range(data.cols)] for row in 
                  range(data.rows)]
    data.cellMargin = 5
    # set piece shapes using boolean values
    iPiece = [
              [True, True, True, True]
             ]
                   
    jPiece = [
              [True, False, False],
              [True, True, True]
             ]
    lPiece = [
              [False, False, True],
              [True, True, True]
             ]
    oPiece = [
              [True, True],
              [True, True]
             ]
    sPiece = [
              [False, True, True],
              [True, True, False]
             ]
    tPiece = [
              [False, True, False],
              [True, True, True]
             ]
    zPiece = [
              [True, True, False],
              [False, True, True]
             ]
    # initialise the tetris pieces in a list
    data.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, 
                         sPiece, tPiece, zPiece]
    # initialise tetris piece colors corresponding to tetrisPieces list
    data.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", 
                              "green", "orange"]
    # set colour, tetrisPiece, startRow, startCol using helper function
    newFallingPiece(data)
    # data.count to slow down timerFired function
    data.count = 0
    # data.score to keep track of tetrisScore
    data.score = 0
    # data.isGameOver to check if game is over
    data.isGameOver = False


def newFallingPiece(data):
    # length of data.tetrisPieces
    piecesLength = len(data.tetrisPieces)
    # get a random index for a tetrisPiece
    pieceIndex = random.randint(0, piecesLength-1)
    # get the tetris piece and the corresponding colour
    data.fallingPiece = data.tetrisPieces[pieceIndex]
    data.fallingPieceColour = data.tetrisPieceColors[pieceIndex]
    # initial start position of every piece is row 0
    data.fallingPieceRow = 0
    # number of cols in a tetrisPiece
    fallingPieceCols = len(data.fallingPiece[0])
    # startingCol of the tetrisPiece
    data.fallingPieceCol = (data.cols//2) - (fallingPieceCols//2)
    

####### Controller ##################
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # if your game is not over
    if(data.isGameOver == False):
        # change drow, dcol based on direction
        # you want to move the tetrisPiece
        if(event.keysym == "Left"):
            drow, dcol = 0, -1
        elif(event.keysym == "Right"):
            drow, dcol = 0, 1
        elif(event.keysym == "Down"):
            drow, dcol = 1, 0
        # if you move up, the rotation changes
        elif(event.keysym == "Up"):
            drow, dcol = 0, 0
            rotateFallingPiece(data)
        # any other key will call a new falling piece
        else:
            drow, dcol = 0, 0
            # initialise and create newFallingPiece
            newFallingPiece(data)
        # based on drow, dcol : call moveFallingPiece
        moveFallingPiece(data, drow, dcol)
    else:
        if(event.keysym == "r"):
            init(data)
    
def timerFired(data):
    # increment data.count by 1
    data.count += 1
    # new piece will be called only every half sec
    if(data.count % 5 == 0):
        # if fallingPiece cannot move down
        if(moveFallingPiece(data, 1, 0) == False):
            # place the piece on the board and call a new one
            placeFallingPiece(data)
            newFallingPiece(data)
            # if piece touches another piece or out of the board
            # and cannot move any further down : game is over
            if(fallingPieceIsLegal(data) == False):
                data.isGameOver = True
    # otherwise remove fullrows 
    removeFullRows(data)

def moveFallingPiece(data, drow, dcol):
    # take drow and dcol and move the piece
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    # if the piece cannot be moved
    if(fallingPieceIsLegal(data) == False):
        # reset to last version 
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True

def fallingPieceIsLegal(data):
    # get rows and cols of the fallingPiece
    rows, cols = len(data.fallingPiece), len(data.fallingPiece[0])
    # iterate through it
    for row in range(rows):
        for col in range(cols):
            # if the value in the 2D list is True
            if(data.fallingPiece[row][col] == True):
                # and fallingPiece within bounds
                if((data.fallingPieceRow < 0) or 
                   (data.fallingPieceRow + (rows -1) >= data.rows) or
                   (data.fallingPieceCol < 0) or 
                   (data.fallingPieceCol + (cols -1) >= data.cols) or 
                   # you dont hit the next piece 
                   data.board[row + data.fallingPieceRow][col + 
                              data.fallingPieceCol] 
                            != data.emptyColor):
                      return False
    return True
        
def placeFallingPiece(data):
    # iterate through rows and cols of the board
    rows, cols = len(data.board), len(data.board[0])
    for row in range(rows):
        for col in range(cols):
            # if dims of board match dims of fallingPiece
            if((row == data.fallingPieceRow) and
               (col == data.fallingPieceCol)):
                   # set colour of piece on the board
                   setColourOnBoard(data)
                   
def removeFullRows(data):
    #set old and newRows to bottom of board
    oldRow = data.rows -1
    newRow = data.rows -1
    # set fullRows to 0
    fullRows = 0
    # iterate from bottom to top of board
    for i in range(len(data.board)-1, 0, -1):
        # set currRow
        currRow = data.board[i]
        # if the row is full increment counter by 1
        # move to the next row
        if(isFull(data, currRow)):
            oldRow -=1
            fullRows += 1
        # if its not full
        else:
            # create a copy of the row
            copyOldRow = copy.deepcopy(data.board[oldRow])
            # set the newRow to the oldRow
            data.board[newRow] = copyOldRow
            # move both old and newRows up
            oldRow -=1
            newRow -=1
    # increment score by square of fullRows
    data.score += (fullRows ** 2)
    # reset fullRows to 0 after done iterating
    fullRows = 0
                   
def setColourOnBoard(data):
    pieceRows = len(data.fallingPiece)
    pieceCols = len(data.fallingPiece[0])
    # iterate through the dims of the fallingPiece
    for i in range(pieceRows):
        for j in range(pieceCols):
            if(data.fallingPiece[i][j] == True):
                #offset by starting pos and set colour
                newI = i + data.fallingPieceRow
                newJ = j + data.fallingPieceCol
                data.board[newI][newJ] = data.fallingPieceColour
        
def rotateFallingPiece(data):
    # set oldFallingPiece as the curr fallingPiece
    oldFallingPiece = data.fallingPiece
    # get the centreRow of the oldPiece
    oldCentreRow = data.fallingPieceRow + (len(data.fallingPiece)//2)
    # get the new startingRow of the newPiece
    newRow = oldCentreRow - (len(data.fallingPiece[0])//2)
    # get the centreCol of the oldPiece
    oldCentreCol = data.fallingPieceCol + (len(data.fallingPiece[0])//2)
    # get the new startingCol of the newPiece
    newCol = oldCentreCol - (len(data.fallingPiece)//2)
    # store oldStarting row and col
    oldRow, oldCol = data.fallingPieceRow, data.fallingPieceCol
    # rotate the fallingPiece
    data.fallingPiece = rotatedFallingPiece(data) 
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    # if the fallingPiece is not Legal
    if(fallingPieceIsLegal(data) == False):
        # reset the fallingPieceRow and col to old dims
        data.fallingPiece = oldFallingPiece
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol

def rotatedFallingPiece(data):
    # do a deepcopy of the fallingPiece
    L = copy.deepcopy(data.fallingPiece)
    rows, cols = len(data.fallingPiece), len(data.fallingPiece[0])
    # iterate through each list and reverse it
    for elem in L:
        elem.reverse()
    # initiate a newPiece empty list
    newPiece = []
    # iterate through cols and append reversed
    # row into newPiece
    for col in range(cols):
        rowList = []
        for row in range(rows):
            rowList.append(L[row][col])
        newPiece.append(rowList)
    return newPiece

def isFull(data, currRow):
    # checks if any row is full
    for elem in currRow:
        if(elem == data.emptyColor):
            return False
    return True
            
####### View ###############
def redrawAll(canvas, data):
    # if the game is not over drawGame
    if(data.isGameOver == False):
        drawGame(canvas, data)
    # else drawGameOver
    else:
        drawGameOver(canvas, data)

def drawGameOver(canvas, data):
    # get the centre dimensions of canvas
    # to draw gameOver text
    centreX = data.width//2
    centreY = data.height//2
    text = "    GAME OVER!! \nPress 'r' to Restart"
    canvas.create_text(centreX, centreY, text = text, fill = "dark Green", font = "Arial 26 bold")
    
def drawGame(canvas, data):
    # create the orange background
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "orange")
    # draw the game, board and the score
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)

def drawScore(canvas, data):
    # intiate the text
    text = "Score : " + str(data.score)
    # get the score dims
    scoreX = data.width//5
    scoreY = data.margin//2
    # create the score text
    canvas.create_text(scoreX, scoreY, text = text, fill = "black", font = "Arial 14 bold")
    
def drawFallingPiece(canvas, data):
    # iterate through the fallingPiece
    rows, cols = len(data.fallingPiece), len(data.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            if(data.fallingPiece[row][col] == True):
                # set row and col on board by offset
                # of starting position of fallingPiece
                newRow = row + data.fallingPieceRow
                newCol = col + data.fallingPieceCol
                colour = data.fallingPieceColour
                # draw the cell with the respective colour
                drawCell(canvas, data, newRow, newCol, colour)
    
def drawBoard(canvas, data):
    rows, cols = data.rows, data.cols
    for row in range(rows):
        for col in range(cols):
            colour = data.board[row][col]
            drawCell(canvas, data, row, col, colour)
            
def drawCell(canvas, data, row, col, colour):
    # create black cells
    cellLeft = data.margin + (col*data.cellSize)
    cellTop = data.margin + (row*data.cellSize)
    cellRight = cellLeft + (data.cellSize)
    cellBottom = cellTop + (data.cellSize)
    canvas.create_rectangle(cellLeft, cellTop, cellRight, cellBottom, fill="black")
    # create blue cells
    newCellLeft = cellLeft + data.cellMargin
    newCellTop = cellTop + data.cellMargin
    newCellRight = cellRight - data.cellMargin
    newCellBottom = cellBottom - data.cellMargin
    canvas.create_rectangle(newCellLeft, newCellTop, newCellRight, newCellBottom, fill=colour)
    
######### Test Functions ###########
def testisFull():
    print("Testing isFull()...", end="")
    class Struct(object) : pass
    data = Struct()
    data.emptyColor = "blue"
    currRow = ["blue", "red", "green", "red", "blue"]
    assert(isFull(data, currRow) == False)
    currRow = ["yellow", "red", "green", "red", "green"]
    assert(isFull(data, currRow) == True)
    print('Passed.')

testisFull()

def testrotatedFallingPiece():
    print("Testing rotatedFallingPiece()...", end="")
    class Struct(object) : pass
    data = Struct()
    data.fallingPiece = [[False, True, True], [True, True, False]]
    newPiece = [[True, False], [True, True], [False, True]]
    assert(rotatedFallingPiece(data) == newPiece)
    print('Passed.')

testrotatedFallingPiece()

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
####################

def playTetris():
    # each cell in the grid is of size 40
    cellSize = 40
    # set rows and cols to 15 and 10
    rows = 15
    cols = 10
    # margin of the grid from the canvas
    margin = 40
    # calculating width and height of canvas
    width = (2*margin) + (cellSize * cols) 
    height = (2*margin) + (cellSize * rows)
    run(width, height)
    
playTetris()