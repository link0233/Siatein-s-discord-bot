import json
from lib.ItemAndTrad.box import *

class item:
    def __init__(self):
        self.box = box()
        self.itemdata = {}
        self.moneyData = {}
        self.loadItemData()
        self.loadMoneyData()

    def loadItemData(self):
        try: 
            with open("./saves/items.json" , "r") as f:
                self.itemdata = json.load(f)
        except : pass

    def loadMoneyData(self):
        try: 
            with open("./saves/rank.json" , "r") as f:
                self.moneyData = json.load(f)
        except : pass

    def saveItemData(self):
        try: 
            with open("./saves/items.json" , "w") as f:
                json.dump(self.itemdata,f)
        except : pass

    def saveMoneyData(self):
        try: 
            with open("./saves/rank.json" , "w") as f:
                json.dump(self.moneyData,f)
        except : pass

    def openBox(self,userName,boxName,count):
        self.loadItemData()
        self.loadMoneyData()
        allOpen = {}
        for i in range(count):
            try:
                money = self.moneyData[userName][1]
            except:
                return ["not find his money"]
            out = self.box.openBox(money,boxName)
            if out == "notEnoughMoney":
                return ["not enough money" ,i]
            if out == "notFindBox":
                return ["not find box"]
            
            if userName in self.itemdata :
                if out[0] in self.itemdata[userName] :
                    self.itemdata[userName][out[0]] +=1
                else:
                    self.itemdata[userName][out[0]] =1
                if out[0] in allOpen :
                    allOpen[out[0]] += 1
                else:
                    allOpen[out[0]]  = 1
                
            else: 
                self.itemdata[userName] = {}
                if out[0] in self.itemdata[userName] :
                    self.itemdata[userName][out[0]] +=1
                else:
                    self.itemdata[userName][out[0]] =1
                if out[0] in allOpen :
                    allOpen[out[0]] += 1
                else:
                    allOpen[out[0]]  = 1
                

            money = out[1]
            self.moneyData[userName][1] = money
        self.saveItemData()
        self.saveMoneyData()

        return [allOpen,out[0],out[1]]
    