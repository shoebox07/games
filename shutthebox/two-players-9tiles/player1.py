import itertools
from player2 import PlayerTwo

class PlayerOne:
    
    def __init__(self, name):
        self.name = name
        self.p2prob = {}
        self.evsbycombo = {}
        self.evsref = {}
    
    def max_reward(self, unusedTiles, roll, move = False):
        possibleStates = list(self.outcomes(unusedTiles, roll)) #Different ways that we can close the tiles subject to the constraint
        if possibleStates == []: #if there are no possible states
            opensum = sum(unusedTiles) #sum the unused tiles
            if opensum in self.p2prob: #if we already have calculated the probability of player 2 winning with this score
                return 1 - self.p2prob[opensum] #return 1 - the probabilty player 2 wins 
            else: #if we have not already calculated this probability
                p2 = PlayerTwo("two") #create a new instance using the PlayerTwo Class
                #print("about to calculate p2prob with the following open sum", opensum)
                self.p2prob[opensum] = p2.expected_value([1,2,3,4,5,6,7,8,9], opensum) #calculate the probability that player 2 wins
                p1reward = 1 - self.p2prob[opensum] #The reward is 1 minus this probability
                del p2 #delete the object in that class. I wasn't sure if I should keep it or not so I deleted it just in case
                return p1reward #return the reward
        if len(possibleStates) == 1 and possibleStates[0] == unusedTiles: #if there is only one possible state and it includes all of the unused tiles. so in other words, if our only possible move gives us a score of 0
            return 1
        ev = {} #create a dictionary with expected values
        setUnusedTiles = set(unusedTiles) #create a set of the unused tiles
        for s in possibleStates: #go through each possible state
            setState = set(s) #set of tiles that will be closed
            dif = setUnusedTiles - setState #set of tiles that will be open
            lstdif = list(dif) #list of tiles left open
            sort = sorted(lstdif) #sort the list of tiles left open
            string = ''.join(map(str, s)) #join the list of tiles that will be closed. thus it is a string instead of a list
            ev[string] = self.expected_value(sort) #the key is tiles that will be closed and the expected value is the ev of that move (closing those tiles)
        
        lstvalues = ev.values() #create a list of the values
        
        highestev = max(lstvalues) #select the highest expected value
        
        if move == False: #if we don't the move associated with this high ev
            return highestev #return the expected value
        else: 
            bestmove = max(ev, key = ev.get) #get the best move 
            return bestmove #return it
          
    def expected_value(self, lst):
        if sum(lst) > 6: #if the sum of the tiles are greater than 6
            combos = list(itertools.product(range(1,7), repeat = 2)) #we will use two dice
            total = len(combos)
        else: #if it's less than or equal to 6 we will use one dice
            combos = list(itertools.product(range(1,7), repeat = 1))
            total = len(combos)
        
        stringlst = ''.join(map(str, lst)) #create a string of the open tiles
        if stringlst not in self.evsbycombo: #if we have not calcuated the expected values by dice roll for this position
            self.evsbycombo[stringlst] = {} #create a dictionary in the dictionary that will have the expected value by roll
            self.evsref[stringlst] = {} #this dictionary is used for reference
            for c in combos: #iterate through each combo
                csum = sum(c) #sum the two dice
                if csum in self.evsbycombo[stringlst]: #if we have already calcuated the expected value for this sum
                    if self.evsref[stringlst][csum] != 0: #and if it's not zero
                        self.evsbycombo[stringlst][csum] += self.evsref[stringlst][csum] #add it to itself 
                else: #if we did not calculate it, calculate it and add it to the dictionary
                    self.evsref[stringlst][csum] = self.max_reward(lst, csum)
                    self.evsbycombo[stringlst][csum] = self.evsref[stringlst][csum]
 
        sumvalues = sum(self.evsbycombo[stringlst].values()) #sum all of the expected values by combo
        
        ev = sumvalues * (1/total) #calculate the expected value
        #print("ev", ev)
        return ev #return it
           
    def outcomes(self, unusedTiles, roll, usedNums = [], usedNumsSum = 0): #this calculates all of the possible states for a position given the constraint (it must sum to the dice roll)
        if usedNumsSum == roll: # if the sum is equal to the roll
            yield usedNums #yield
        if usedNumsSum >= roll:
            return #if it's bigger there is no point in adding the rest of the positions
        for index, num in enumerate(unusedTiles): #enumerate
            needToSum = unusedTiles[index + 1:] #remove the index positions thatt we are about to consider
            yield from self.outcomes(needToSum, roll, usedNums + [num], usedNumsSum + num) #call the functon recursively

            
        