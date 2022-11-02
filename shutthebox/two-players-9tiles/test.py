import sys
import getopt
from player1 import PlayerOne
from player2 import PlayerTwo

if __name__ == "__main__":
    l = len(sys.argv)

    try:
        inputtest = sys.argv[1]
    except IndexError:
        print("Please insert command line arguments.")
        sys.exit(1)

    player = sys.argv[1]
    
    if not isinstance(player, str):
        print("The first argument must be be a string. ")
        sys.exit(1)
    
    player = player.lower()
    
    if player != "--one" and player != "--two":
        print("The first argument must be either \"--one\" or \"--two\". ")
        sys.exit(1)

    try:
        inputtest = sys.argv[2]
    except IndexError:
        print("Please include the requested calculation as the second argument.")
        sys.exit(1)
    
    calc = sys.argv[2]
    
    if not isinstance(calc, str):
        print("The second argument must be a string.")
        sys.exit(1)
    
    calc = calc.lower()
    
    if calc != "--move" and calc != "--expect":
        print("The second argument must be either \"--expect\" or \"--move\".")
        sys.exit(1)
    
    try:
        inputtest = sys.argv[3]
        inttest = int(inputtest)
    except IndexError:
        print("Please include the position as the third argument.")
        sys.exit(1)
    except ValueError:
        print("The position must only include integers.")
        sys.exit(1)

    position = sys.argv[3]
    
    if len(position) >= 10: 
        print("The position must be a string of unique integers between 1-9 in increasing order.")
        sys.exit(1)
    
    lst = list(position)
    
    lstint = [int(x) for x in lst]

    if sorted(lstint) != lstint:
        print("The position must be in increasing order.")
        sys.exit(1)
    
    if len(set(lstint)) != len(lstint):
        print("The position must be a unique list of integers.")
        sys.exit(1)
        
        
    if player == "--two":
        try:
            inputtest = sys.argv[4]
            intinput = int(inputtest)
        except IndexError:
            print("Please input player one's score as the fourth argument.")
            sys.exit(1)
        except ValueError:
            print("Player one's score must be an integer.")
            sys.exit(1)

    if calc == "--move":
        
        if player == "--two":
            try:
                inputtest = sys.argv[5]
                intinput = int(inputtest)
            except IndexError:
                print("Please include the rum of the roll as the fifth argument.")
                sys.exit(1)
            except ValueError:
                print("The sum of the roll must be an integer")
                sys.exit(1)
            
        if player == "--one":
            try:
                inputtest = sys.argv[4]
                intinput = int(inputtest)
            except IndexError:
                print("Please include the sum of the roll as your fourth argument")
                sys.exit(1)
            except ValueError:
                print("The sum of the roll must be an integer")
                sys.exit(1)
    
        if player == "--one":
            diceroll = 4
            p1score = None
        else:
            diceroll = 5
            p1score = int(sys.argv[4])
        
        sumofroll = int(sys.argv[diceroll])
        
    if calc == "--expect":
        
        if player == "--one":
            p1score = None
        else:
            p1score = int(sys.argv[4])
    
    if player == '--one':
        p = PlayerOne(player)
        if calc == '--move':
            move = True 
            best = p.max_reward(lstint, sumofroll, move)
            lstbest = list(best)
            intlistbest = [int(x) for x in lstbest]
            bestmove = sorted(intlistbest)
            print(bestmove)
            
        else:
            ev = round(p.expected_value(lstint), 6)
            fev = float(ev)
            final_ev = format(fev, '.6f')
            print(final_ev)
 
    if player == '--two':
        p = PlayerTwo(player)
        if calc == '--move':
            move = True
            best = p.max_reward(lstint, sumofroll, p1score, move)
            lstbest = list(best)
            intlistbest = [int(x) for x in lstbest]
            bestmove = sorted(intlistbest)
            print(bestmove)
            
        else:
            ev = round(p.expected_value(lstint, p1score), 6)
            fev = float(ev)
            final_ev = format(fev, '.6f')

            print(final_ev)
    