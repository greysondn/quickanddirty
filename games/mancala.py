#!/usr/bin/python3

# change the player
# yes, I know a flag and NOT are are easier.
# I might extend this to X players later, which requires
# a generic version.
def changePlayer(player):
    ret = 0
    
    if (1 == player):
        ret = 2
    if (2 == player):
        ret = 1
        
    return ret

# perform a move on the board and return it
# requires the table of stones, starting pit, and player
def doMove(stones, pit, player):
    # basically, we're going to return
    # a copy of stones with changes and the
    # end result
    retR = -1
    retS = stones
    
    # now the trick
    handful = retS[pit]
    retS[pit] = 0
    i = pit
    
    while (handful != 0):
        # advance hand
        if ((player == 1) and (i == 12)):
            i = 0
        elif ((player !=1) and (i == 5)):
            i = 7
        elif (i == 13):
            i = 0
        else:
            i = i + 1
        
        # drop a stone
        handful = handful - 1
        retS[i] = retS[i] + 1
        
        # is our handful empty?
        if (handful == 0):
            # few conditions under which we're fine
            
            # are we in a mancala?
            if ((i == 6) or (i == 13)):
                retR = i
            # do we have at least two stones under our hand?
            elif (retS[i] >= 2):
                # pick it up so we can carry on
                handful = retS[i]
                retS[i] = 0
            # we must be at the end
            else:
                retR = i
    
    # good time to return
    return (retS, retR)

# god this is awful but it looks nice    
def printBoard(stones, pl1, pl2):

    line1 = ""
    line1 = line1 + "█    █ "
    line1 = line1 + str(stones[12]).rjust(2)
    line1 = line1 + " █ "
    line1 = line1 + str(stones[11]).rjust(2)
    line1 = line1 + " █ "
    line1 = line1 + str(stones[10]).rjust(2)
    line1 = line1 + " █ "
    line1 = line1 + str(stones[9]).rjust(2)
    line1 = line1 + " █ "
    line1 = line1 + str(stones[8]).rjust(2)
    line1 = line1 + " █ "
    line1 = line1 + str(stones[7]).rjust(2)
    line1 = line1 + " █    █"
   
    line2 = ""
    line2 = line2 + "█    █ "
    line2 = line2 + str(stones[0]).rjust(2)
    line2 = line2 + " █ "
    line2 = line2 + str(stones[1]).rjust(2)
    line2 = line2 + " █ "
    line2 = line2 + str(stones[2]).rjust(2)
    line2 = line2 + " █ "
    line2 = line2 + str(stones[3]).rjust(2)
    line2 = line2 + " █ "
    line2 = line2 + str(stones[4]).rjust(2)
    line2 = line2 + " █ "
    line2 = line2 + str(stones[5]).rjust(2)
    line2 = line2 + " █    █"
            
    lineM = "█ " +             str(stones[13]).rjust(2) +             " ███████████████████████████████ " +             str(stones[6]).rjust(2) +             " █"

    print(pl2.ljust(41))
    print("█████████████████████████████████████████")
    print("█    █    █    █    █    █    █    █    █")
    print("█    █  L █  K █  J █  I █  H █  G █    █")
    print(line1)
    print("█    █    █    █    █    █    █    █    █")
    print(lineM)
    print("█    █    █    █    █    █    █    █    █")
    print("█    █  A █  B █  C █  D █  E █  F █    █")
    print(line2)    
    print("█    █    █    █    █    █    █    █    █")
    print("█████████████████████████████████████████")
    print(pl1.rjust(41))

# actual game business logic
def main():
    stones = [4, 4, 4, 4, 4, 4, 0,
              4, 4 ,4, 4, 4, 4, 0]
              
    
    PL1_NAME    = input("What is player 1's name? ")
    PL2_NAME    = input("What is player 2's name? ")
    
    gameon = True
    player = 1
    
    while(gameon):
        print("")
        printBoard(stones, PL1_NAME, PL2_NAME)
        print("")
        
        # print player's turn
        if (1 == player):
            print("It is " + PL1_NAME + "'s turn")
        else:
            print("It is " + PL2_NAME + "'s turn")
            
        # get selection
        cell = "Z"
        cellInvalid = True
        noMove = False
        
        while(cellInvalid):
            cell = input("What cell would you like?")
            cell = cell.capitalize()
            pit = -1
            
            if (1 == player):
                if "A" == cell:
                    pit = 0
                elif "B" == cell:
                    pit = 1
                elif "C" == cell:
                    pit = 2
                elif "D" == cell:
                    pit = 3
                elif "E" == cell:
                    pit = 4
                elif "F" == cell:
                    pit = 5
                else:
                    print("")
                    print("cell selection invalid")
                    print("")
                    continue
            else:
                if "G" == cell:
                    pit = 7
                elif "H" == cell:
                    pit = 8
                elif "I" == cell:
                    pit = 9
                elif "J" == cell:
                    pit = 10
                elif "K" == cell:
                    pit = 11
                elif "L" == cell:
                    pit = 12
                else:
                    print("")
                    print("cell selection invalid")
                    print("")
                    continue
            
            # we have the intended cell, make sure it
            # isn't empty now
            if (0 == stones[pit]):
                t = 0
                
                if (1 == player):
                    for index in range(0, 6):
                        t = t + stones[index]
                else:
                    for index in range(7, 13):
                        t = t + stones[index]
                
                # if t is empty, don't hate on the player
                if (0 == t):
                    noMove = True
                else:
                    print("cell selection invalid")
                    continue
            
            # it takes some doing to get here
            cellInvalid = False
            
        # we now have pit and whether they have moves
        if noMove:
            print("It's okay. You have no move.")
            
            player = changePlayer(player)
        else:
            # so they have moves. We have a pit!
            stones, pit = doMove(stones, pit, player)
            
            print("Ended: " + str(pit))
            
            # so we evaluate where they ended
            if ((pit == 6) or (pit == 13)):
                # we don't change the player!
                pass
            else:
                # change the player!
                player = changePlayer(player)
                
            # make sure the game isn't over
            acc = 0
            
            for index in range(0, 6):
                acc = acc + stones[index]
            for index in range(7, 13):
                acc = acc + stones[index]
                
            if (acc == 0):
                # game over!
                print("GAME OVER!")
                
                printBoard(stones, PL1_NAME, PL2_NAME)
                
                gameon = False
                
if __name__ == "__main__":
    main()
