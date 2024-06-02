import json
import math

class Rank:
    def __init__ (self):
        self.data = {}
        self.load()

    def numberCountTrue(self,userName,data):
        score = data[0] / (data[1]+data[0])*100
        self.addScore(score,userName)
        self.save()
        return score
    
    def numberCountFalse(self,userName,data):
        score = data[0] / (data[1]+data[0])*100
        self.addScore(-score,userName)
        self.save()
        return score

    def GuessNumberTrue(self,userName,MaxNumber,testCount):
        score = math.log10(MaxNumber) * 185 / testCount
        self.addScore(score,userName);self.save()
        return score
    
    def GuessNumberFalse(self,userName,nowNumber,MaxNumber,guessNumber):
        score = (1 /abs(nowNumber - guessNumber) ) * MaxNumber / 10
        self.addScore(score,userName);self.save()
        return score

    def save(self):
        with open("./saves/rank.json","w") as f:
            json.dump(self.data,f)
    
    def load(self):
        with open("./saves/rank.json","r") as f:
            self.data = json.load(f)

    def addScore(self,score,userName):
        if userName in self.data:
            self.data[userName][0] += score
            self.data[userName][1] += score/10 * math.log10(self.data[userName][0])
        else:
            self.data[userName] = [1,1]
            self.data[userName][0] = score
            self.data[userName][1] = score//10
        self.save()