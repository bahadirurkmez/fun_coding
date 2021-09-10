### PLAYER HOLDS A 4 DIGIT NUMBER. 0 INCLUDED
### EACH DIGIT SHOULD BE DIFFERENT
### COMPUTER TRIES TO GUESS THE NUMBER
### PLAYER TRIES TO COMPUTER NUMBER
### WHOEVER GUESSES CORRECTLY IN MIN MOVE WINS
### LET'S SAY PLAYER NUMBER IS 3456
### COMPUTER GUESSES 4396
### PLAYER GIVES THE CLUE:
### FOR EACH DIGIT IS CORRECTLY PLACED +
### FOR EACH DIGIT MISPLACED -
### I.E. PLAYER TELLS COMPUTER 1 + 2 -
### FOR THE GUESS 3876 HINT WILL BE 2 + 
#

import random, copy, sys

isFirstTurn = True
possibleNums = []
ComputerGuesses = {}
HumanGuesses = {}
ComputersChoice = 0
pluses = minuses = 0
ComputerScore = 0
PlayerScore = 0
isGameFinished = False
isHumanSucceeded = False
isComputerSucceeded = False

### CHECKS IF COMPUETER OR PLAYER HAS CHOOSEN A NUMBER
### THAT IS WITHIN THE RULES OF GAME
def CheckPlayerNumber(num, player='Human'):
    try:
        response = ''
        # Check if number is within bounds. Smaller than 1023 means 0 is at the beginning
        # or one of 1 or 2 is repeated.
        # larger than 9876 means one of 9,8,7 is repeated      
        if num >= 1023 and num <= 9876: 
            # check if there is a repeat number
            d={}
            for i in str(num):
                if i in d.keys():
                    response = False
                    if player == 'Human':
                        print(' You cannot use same number more than once!')
                    return response
                else:
                    d[i] = 1            
        else:
             response = False
             if player == 'Human':
                print('Your number should be within 1023 and 9876')
             return response

        response = True
        if player == 'Human':
            print('Your choice seems OK. Let\'s play\n')
        return response
      
    except ValueError:
       response = input(str(num) + ' doesn\'t satisfy the rules. Do you want to read the help (Y/N): ')
    finally:
        if response == 'Y':
            print ('help is on the road')

### We will need player's input on computer guesses
### this is where we get them
def AskForResponse():
    
    pluses = 0
    minuses = 0
    isCorrectResponse = False
    
    while not isCorrectResponse:
        try:
            pluses = int(input ('How many pluses? '))
            minuses = int(input ('How many minuses? '))
            isCorrectResponse = CheckResponse(pluses,minuses)                                      
        except (ValueError,TypeError):
            print('Did you enter integers? Check and reenter!')
            pass
        return (pluses,minuses)  #returns a tuple to keep track of player's responses  

### return a list of all possible numbers
### g - guess, ps - pluses, ms - minuses
### posValues - previous list of all possible numbers
def CheckPossibilities(posValues, g, ps, ms):

    dpossible = copy.deepcopy(posValues)
    
    try:
        for i in posValues:
            gplus = 0
            gminus = 0
            l = str(g)
            # check for pluses and minuses
            for j in i:
                if j in l:
                    if i.index(j) == l.index(j):
                        gplus +=1
                    else:      
                        gminus += 1   

            # remove numbers that doesn't fit to player's response
            if gplus != ps or gminus != ms:
                dpossible.remove(i)
            
    except ValueError:
             pass


    return dpossible

### function that guesses player's number
def GuessHumanNumber(computerguess, pluses, minuses):
    global isFirstTurn, possibleNums, NumberPoints
    
    dummypossible = copy.deepcopy(possibleNums)
    if isFirstTurn:               # generate first set of all possible numbers. we have 4356 options
        for i in range(1023,9877):  
            if CheckPlayerNumber(i,'Computer'):
                possibleNums.append(str(i)) 
        
    else:
        dummypossible = CheckPossibilities(possibleNums,computerguess, pluses, minuses)

         # if this hits true that means player gave wrong clues somewhere
         # we ask player to correct any mistakes
         # if user makes a mistake when answering y/n question program exists
         # needs to be improved
        if len(dummypossible) == 0:   
            print('Did you made a mistake while entering PLUSES and MINUSES?')
            print('Here are my guesses and responses:')
            for k,v in ComputerGuesses.items():
                wasCorrect = input('Is the response ' + str(k)  + ' ' + str(v) + ' correct? Y/N: ')     
                if wasCorrect.upper() == 'N':
                    print('Please correct it')
                    ComputerGuesses[k] = AskForResponse()
                elif wasCorrect.upper() == 'Y':
                    print ('OK')
                else:
                    print ('Wrong choice. Exiting')
                    sys.exit()
            
            ### populate correct possible guess list
            dummypossible = []
            for i in range(1023,9877):
                if CheckPlayerNumber(i,'Computer'):
                    dummypossible.append(str(i)) 
            
            for k,v in ComputerGuesses.items():
                dummypossible = CheckPossibilities(dummypossible,int(k),v[0],v[1])
            
            possibleNums = copy.deepcopy(dummypossible)
        
        else:
            possibleNums = copy.deepcopy(dummypossible)
    
    r = possibleNums[random.randint(0,len(possibleNums)-1)]  
    return r # new guess

### Check player's response when she enter responses
### any exception caught when player enters the pluses and minuses
def CheckResponse(p,m):
    if p + m > 4 or p < 0 or m <0:
      return False
    return True

### Player guesses and computer responds
def HumanTurn():
    global isFirstTurn, ComputersChoice, isHumanSucceeded, isHumanPlaysFirst
    print('\n')
    print('Your Turn')
    print('\n')

    gplus = 0
    gminus = 0
    if not isFirstTurn:  # show previous guesses
        print ('Your previous guesses:')
        for k in HumanGuesses.keys():
            print(' %s has %s + and %s -' % (k,HumanGuesses[k][0],HumanGuesses[k][1]))
        print('\n')

    isGuessOK = False
    while not isGuessOK: 
        g = input('I have a number in mind? Can you guess? ')
        isGuessOK = CheckPlayerNumber(int(g)) # check if guess conforms the rules of game

    if isGuessOK:
        l = str(g)
        lcomp = str(ComputersChoice)
        for i in l:
            if i in lcomp and l.index(i) == lcomp.index(i):
                gplus += 1 
            elif i in lcomp and l.index(i) != lcomp.index(i):
                gminus += 1
        print(' %s has %s + and %s -\n' % (g,gplus,gminus))  # print to screen

        HumanGuesses[g] = (gplus,gminus)  # record the moves of player

        if gplus == 4: ## Player 
            print('Congratulations you have guessed in %s moves.' % len(HumanGuesses))
            print ('\n Here are your moves') 
            for k in HumanGuesses.keys():
                print(' %s has %s + and %s -' % (k,HumanGuesses[k][0],HumanGuesses[k][1]))
        
            if isHumanPlaysFirst:
                print('Wait for my move\n')
            
            isHumanSucceeded = True

    return True


### Computer guesses and player responds
def ComputerTurn():
    global isFirstTurn, pluses, minuses, isComputerSucceeded, isHumanPlaysFirst
    
    guess = 0 if len(ComputerGuesses)==0 else list(ComputerGuesses)[-1] # get latest guess to populate possible options
    isComputerChoiceCompleted = False
    while not isComputerChoiceCompleted:
        if isFirstTurn:
            guess = GuessHumanNumber(0,0,0)
        else:
            guess = GuessHumanNumber(guess,pluses,minuses)

        print(str(guess) + ' this is my guess')
        isComputerChoiceCompleted = True
        
    tpl = AskForResponse()
    pluses, minuses = int(tpl[0]) , int(tpl[1])
        
    isComputerChoiceCompleted = False
    ComputerGuesses[guess] = (pluses,minuses)

    if pluses == 4: ## Player 
        print('I have in %s moves.' % len(ComputerGuesses))
        print ('\n Here are my moves') 
        for k in ComputerGuesses.keys():
            print(' %s has %s + and %s -' % (k,ComputerGuesses[k][0],ComputerGuesses[k][1]))
    
        if not isHumanPlaysFirst:
            print('Waitin for your move\n')
        
        isComputerSucceeded = True

    return True

# Play game
def play():
    global PlayerScore, ComputerScore, ComputersChoice,isHumanPlaysFirst
    global isComputerSucceeded, isHumanSucceeded
    global PlayerNumber, isGameFinished, isFirstTurn

    isHumanPlaysFirst = bool(random.randint(0,2))

    ComputersChoice = GuessHumanNumber(0,0,0)  # we will use same code to generate a number for Computer

    print('I have chosen my number. Plesae choice yours')

    isPlayerNumberOK = False
    while not isPlayerNumberOK:
        try:    
            PlayerNumber = int(input('Please enter a 4 digit number: '))

            isPlayerNumberOK = CheckPlayerNumber(PlayerNumber)
        except ValueError:
            print ('Your choice should be number')

    while not isGameFinished:
        if isHumanPlaysFirst:
            HumanTurn()
            ComputerTurn()
            isFirstTurn = False
        else:
            ComputerTurn()
            HumanTurn()
            isFirstTurn = False
        PlayerScore += 1 if isHumanSucceeded and not isComputerSucceeded else 0
        ComputerScore +=1 if not isHumanSucceeded and isComputerSucceeded else 0
        isGameFinished = True if isHumanSucceeded or isComputerSucceeded else False

isContinousPlay = True
while isContinousPlay:
    play()
    print('Your Number: %s  --------------- Computer Number: %s' % (PlayerNumber,ComputersChoice))
    print('Your Score: %s  --------------- Computer Score: %s' % (PlayerScore,ComputerScore))
    isContinousPlay = True if str(input('One more! (Y/N)')).upper() == 'Y' else False
    #set game inputs to originials
    isFirstTurn = True
    possibleNums = []
    ComputerGuesses = {}
    HumanGuesses = {}
    ComputersChoice = 0
    pluses = minuses = 0
    isGameFinished = False
    isHumanSucceeded = False
    isComputerSucceeded = False