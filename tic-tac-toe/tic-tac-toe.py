import random, copy, time

# play board dictionary
TheBoard = {'t-L':' ','t-M':' ','t-R':' ','m-L':' ','m-M':' ','m-R':' ','b-L':' ','b-M':' ','b-R':' '}
name ='' # holds user name
playerpiece = '' # hold player's choice of piece
computerpiece = '' # mandatory computer piece. If player X computer O or vice versa
playerwins = False # boolean if player wins the game
computerwins = False # boolean if computer wins the game
isgameFinished = False # 3 Xs or 3 Os in one row, col or diagonal
playerScore = 0 # holds player's wins
computerScore = 0 # holds computer's wins

# winning rows, cols and dias
temp = list(TheBoard)
rows =[[temp[0],temp[1],temp[2]],[temp[3],temp[4],temp[5]],[temp[6],temp[7],temp[8]]] 
cols =[[temp[0],temp[3],temp[6]],[temp[1],temp[4],temp[7]],[temp[2],temp[5],temp[8]]]
dias =[[temp[0],temp[4],temp[8]],[temp[2],temp[4],temp[6]]]

### populate possible moves
### returns a list
def possiblemoves():
    r = [] 
    for k,v in TheBoard.items():
        if v == ' ':
            r.append(k)
    return r

### prints the board
def printBoard(board):
    print('\n')
    print(board['t-L'] + ' | ' + board['t-M'] + ' | ' + board['t-R'])
    print('---------')
    print(board['m-L'] + ' | ' + board['m-M'] + ' | ' + board['m-R'])
    print('---------')
    print(board['b-L'] + ' | ' + board['b-M'] + ' | ' + board['b-R'])
    print('\n')

### game setup
### name and piece questions
def startgame():
    global name, playerpiece, computerpiece # we will change values of these so need to get them here

    name = input('With who I am playing this game?: ') # ask for player's name
    
    print('\n')
    print('Dear %s, we will play game of Tic-Tac-Toe.' % name)

    while True:
        try:
            playerpiece = str(input('Please choose your piece: X or O: ')).upper()
            if playerpiece == 'X' or playerpiece == 'O':
                computerpiece = 'X' if playerpiece != 'X' else 'O'
                break
            else:
                print('Choose X or O please')
        except:
                print('Only X or O')

### asks for player move
def playermove():
    global isgameFinished, playerwins
    myMoves = possiblemoves() # get possible moves
    
    # No possible moves
    if len(myMoves) == 0:
        isgameFinished = True # so game finished
        return
    
    isCorrectMove = False # checks if player entered correct key
    # player can only play to empty squares and those should be on the board
    while not isCorrectMove:
        move = str(input('What is your move %s? %s' % (name, myMoves)))
        if move in TheBoard.keys() and TheBoard[move] == ' ': 
            TheBoard[move] = playerpiece
            isgameFinished = checkBoard(move, TheBoard)
            playerwins = isgameFinished
            isCorrectMove = True
        else:
            print('CHECK YOUR MOVE. MAKE SURE IT IS IN THE LIST')

### calculates computers move
def computermove():
    # we will change values of these so need to get them here
    global isgameFinished, computerwins
   
    # possible computer moves
    compmoves = possiblemoves()
    
    # No possible moves
    if len(compmoves) == 0:
        isgameFinished = True # so the game is finished
        return

    print('My Turn')
    time.sleep(1)  # make computer wait a bit
    willThisMoveWin = False
    isImminent = False

    # dummyBoard to analyze moves
    dummyBoard = copy.deepcopy(TheBoard)

    ## check if there is any move guarantees win right away
    for i in compmoves:
        dummyBoard[i] = computerpiece
        willThisMoveWin = checkBoard(i,dummyBoard)
        
        if willThisMoveWin:
            TheBoard[i] = computerpiece
            isgameFinished  = computerwins = willThisMoveWin
            return
        else:
            dummyBoard[i] = ' '
            
    ## check if there is an imminnet threat to lose     

    
    for i in compmoves:        
        dummyBoard[i] = playerpiece
        isImminent = checkBoard(i,dummyBoard)
        
        if isImminent:
            ## if this move is not done player will win
            TheBoard[i] = computerpiece
            return
        else:
            dummyBoard[i] = ' '
        
    ## No easy move. Just play randomly
    if not isImminent:
        TheBoard[compmoves[random.randint(0,len(compmoves)-1)]] = computerpiece

### check if has three Xs or Os in one row, col or dia
def checkBoard(move, board):
    for i in rows:
        if board[i[0]] == board[i[1]] == board[i[2]] != ' ':
            return True
    for i in cols:
        if board[i[0]] == board[i[1]] == board[i[2]] != ' ': 
            return True
    for i in dias:
        if board[i[0]] == board[i[1]] == board[i[2]] != ' ':
            return True
    return False

### prints the board to console and writes necessary messages
def output(pwins, compwins):
    global playerScore, computerScore
    msg=''
    if pwins or compwins:
        playerScore = playerScore + 1 if pwins else playerScore
        computerScore = computerScore + 1 if compwins else computerScore
       
        if pwins :
            msg='You have won!! Congrats!!' 
        elif compwins:
             msg = '%s you are a loser!! You don\'t know how to play!! HA HA HA' % name  
        
        print('\n')
        print(msg)
        printBoard(TheBoard)
        print('\n')
        print('Player: %s ----  Computer: %s' % (playerScore,computerScore))
        #return True
    else:
        printBoard(TheBoard) 
        if isgameFinished:
            print('Player: %s ----  Computer: %s' % (playerScore,computerScore))

### who goes first?
def playerStartsFirst():
    return bool(random.randint(0,1))

### cleans up the board for new game
def cleanup():
    global isgameFinished, playerwins, computerwins
    isgameFinished = playerwins = computerwins = False
    for k,v in TheBoard.items():
        v = ' '
        TheBoard[k] = v

### actual play
def play():
    global isgameFinished, turnNo
    playerStarts = playerStartsFirst()
    while not isgameFinished:
        while True:
            if playerStarts:
                try:
                    playermove()
                    output(playerwins,computerwins)
                    if isgameFinished:
                        break
                    
                    computermove()
                    output(playerwins,computerwins)
                    if isgameFinished:
                        break
                except KeyError:
                    print('An Error Occured. Starting over....')
                    cleanup()
                    continue

            else:
                computermove()
                output(playerwins,computerwins)
                if isgameFinished:
                        break
                try:
                    playermove()
                    output(playerwins,computerwins)
                    if isgameFinished:
                        break          
                except:
                    print('AnError Occured. Starting over....')
                    cleanup()
                    continue

### game starts here
startgame()

### we will continue to play until player
### says No to new game
while True:
    play()
    cleanup()
    repeat = input('One more time? (Y/N): ')
    if repeat.upper() != 'Y':
        break



