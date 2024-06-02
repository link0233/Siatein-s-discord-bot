import json
import random

class guessNumber:
    def __init__(self):
        self.load()
        self.gnt = 0
        self.guessNumber = 0

    def load(self):
        with open("./saves/guessNumber.json") as f:
            self.data = json.load(f)
            self.maxNumber = self.data["maxNumber"]
            self.mixNumber = self.data["mixNumber"]
            self.nowNumber = self.data["nowNumber"]
            self.memberData = self.data["memberData"]
            self.guessCount = self.data["guessCount"]
            self.guessmax = self.data["guessMax"]
            self.guessmix = self.data["guessMix"]

    def save(self):
        self.data={
            "maxNumber": self.maxNumber,
            "mixNumber": self.mixNumber,
            "nowNumber": self.nowNumber,
            "guessCount": self.guessCount,
            "memberData": self.memberData,
            "guessMax":self.guessmax,
            "guessMix":self.guessmix
        }
        with open("./saves/guessNumber.json","w") as f:
            json.dump(self.data,f)
    
    def EnterNumber(self,number,userName):
        #return 1: win
        #return 2: number > nowNumber
        #return 3: number < nowNumber
        number = int(number)

        self.guessNumber = number
        if self.guessmax <= self.nowNumber : self.guessmax = self.nowNumber#確定範圍
        if self.guessmix >= self.nowNumber : self.guessmix = self.nowNumber

        self.guessCount += 1
        if userName in self.memberData:
            self.memberData[userName][0] += 1
        else:
            self.memberData[userName] = [1,0]

        if number > self.nowNumber: 
            if number < self.guessmax:  self.guessmax = number
            return 2
        if number < self.nowNumber: 
            if number > self.guessmix:  self.guessmix = number
            return 3

        if number == self.nowNumber:
            self.memberData[userName][1] += 1
            return 1
    
    def setMax(self,maxNumber):
        try:
            self.maxNumber = maxNumber
        except: return "error"
    def setMix(self,minNumber):
        try:
            self.mixNumber = minNumber
        except: return "error"
    
    def restart(self):
        self.nowNumber = random.randint(self.mixNumber,self.maxNumber)
        self.guessmax = self.maxNumber
        self.guessmix = self.mixNumber
        self.guessCount = 0