import json
import math

class Rank:
    def __init__ (self,item):
        self.data = {}
        self.moneyBonus = {}
        self.load()
        try:
            for i in self.data:
                self.addMoneyBonus(i,item[i])
        except: pass

    def addMoneyBonus(self,userName,userItem):
        self.moneyBonus[userName] = 0
        if "money +1" in userItem:
            self.moneyBonus[userName] += userItem["money +1"] *1
        if "money +2" in userItem:
            self.moneyBonus[userName] += userItem["money +1"] *1
        if "money +5" in userItem:
            self.moneyBonus[userName] += userItem["money +1"] *1
        if "money +10" in userItem:
            self.moneyBonus[userName] += userItem["money +1"] *1

        print(self.moneyBonus)

    def numberCountTrue(self,userName,data):
        score = data[0] / (data[1]+data[0])*100
        a = self.addScore(score,userName)
        self.save()
        return a
    
    def numberCountFalse(self,userName,data):
        score = data[0] / (data[1]+data[0])*100
        a = self.addScore(-score,userName)
        self.save()
        return a

    def GuessNumberTrue(self,userName,MaxNumber,testCount):
        score = math.log10(MaxNumber) * 185 / testCount
        a = self.addScore(score,userName);self.save()
        return a
    
    def GuessNumberFalse(self,userName,nowNumber,MaxNumber,guessNumber):
        score = (1 /abs(nowNumber - guessNumber) ) * MaxNumber / 10
        a = self.addScore(score,userName);self.save()
        return a

    def save(self):
        with open("./saves/rank.json","w") as f:
            json.dump(self.data,f)
    
    def load(self):
        with open("./saves/rank.json","r") as f:
            self.data = json.load(f)

    def addScore(self,score,userName):
        if userName in self.data:
            self.data[userName][0] += score
            self.data[userName][1] += score/10 * math.log10(self.data[userName][0]) + self.moneyBonus[userName]
            addrank = score
            addmoney = score/10 * math.log10(self.data[userName][0]) + self.moneyBonus[userName]
        else:
            self.data[userName] = [1,1]
            self.data[userName][0] = score
            self.data[userName][1] = score//10 + self.moneyBonus[userName]
            addrank = score
            addmoney = score/10 * math.log10(self.data[userName][0]) + self.moneyBonus[userName]
        return [addrank,addmoney]
        self.save()