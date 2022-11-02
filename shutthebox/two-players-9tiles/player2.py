import itertools

class PlayerTwo:
    
    def __init__(self, name):
        self.name = name
        self.evsbycombo = {}
        self.evsref = {}
    
    def max_reward(self, unusedTiles, roll, p1score, move = False):
        possibleStates = list(self.outcomes(unusedTiles, roll)) #list of possible states
        if possibleStates == []: #if there are no possible states
            p2score = sum(unusedTiles) #sum the remaining tiles
            if p2score < p1score: #if our remaining tiles sum is less than p1's score, we won
                return 1
            if p2score == p1score: #if they are equal we tied
                return 0.5 
            if p2score > p1score: #if it is greater then we lost
                return 0
        if len(possibleStates) == 1 and possibleStates[0] == unusedTiles: #if the only possible state gives us a score of 0
            if p1score == 0:
                return 0.5 #if p1 also had a score of 0 then we tied
            else:
                return 1 #if not then we won
            
        ev = {} #dictionary of expected values
        setUnusedTiles = set(unusedTiles) #set of the unuse tiles
        for s in possibleStates: #go through eah state
            setState = set(s) #set of tiles that will be closed
            dif = setUnusedTiles - setState #set of tiles that will be open
            lstdif = list(dif) #list of tiles left open
            sort = sorted(lstdif) #sort the list of tiles that are left open
            string = ''.join(map(str, s)) #join the list of tiles that will be closed
            opensum = sum(lstdif) #sum the open tiles
            if opensum < p1score: #if our sum of the open tiles is less than p1's score, we won
                ev[string] = 1
            else: #else we have to calculate the expected value and keep playing with this policy
                ev[string] = self.expected_value(sort, p1score) #this is indexed by tiles that will be closed
        
        lstvalues = ev.values() #a list of the expected values
        
        highestev = max(lstvalues) #select the highest one
        
        if move == False: #if move is false, return the highest ev
            return highestev
        else: 
            bestmove = max(ev, key = ev.get)
            return bestmove #if not, return the best move associated with the highest ev
          
    def expected_value(self, lst, p1score):
        if sum(lst) > 6: #calculate combos for two dice
            combos = list(itertools.product(range(1,7), repeat = 2))
            total = len(combos)
        else: #calculate combos for one dice
            combos = list(itertools.product(range(1,7), repeat = 1)) 
            total = len(combos) #length of possible combos

        stringlst = ''.join(map(str, lst)) #create a new string of the open tiles
        if stringlst not in self.evsbycombo: #if we have not calculated the expected values by dice roll for this position
            self.evsbycombo[stringlst] = {} #create a dictionary in the dictionary that will have the expected value by roll
            self.evsref[stringlst] = {} #this dictionary is used for reference
            for c in combos: #iterate through thecombos
                csum = sum(c) #sum the dice roll
                if csum in self.evsbycombo[stringlst]: #if we have already calculated the expected value for this sum
                    if self.evsref[stringlst][csum] != 0: #and if it is not zero
                        self.evsbycombo[stringlst][csum] += self.evsref[stringlst][csum] #add it to itself
                else: #if not we will need to add it
                    self.evsref[stringlst][csum] = self.max_reward(lst, csum, p1score) #find the max reward and store it in the reference dictionary
                    self.evsbycombo[stringlst][csum] = self.evsref[stringlst][csum] #store it in the final expected value dictionary
        
        sumvalues = sum(self.evsbycombo[stringlst].values())
        
        ev = sumvalues * (1/total) #formula for expected values. each dice roll has a 1/36 (if it's two die) or 1/6 chance so sum the values and divide by 36 or 6
        return ev
           
    def outcomes(self, unusedTiles, roll, usedNums = [], usedNumsSum = 0): #code that returns the possible outcomes for a given state.
        if usedNumsSum == roll: #if the sum is equal to the roll
            yield usedNums #yield
        if usedNumsSum >= roll: 
            return #if it's bigger there is no point in checking anymore
        for index, num in enumerate(unusedTiles): #enumerate
            needToSum = unusedTiles[index + 1:] #remove the index positions that we are about to consider
            yield from self.outcomes(needToSum, roll, usedNums + [num], usedNumsSum + num) #call the function