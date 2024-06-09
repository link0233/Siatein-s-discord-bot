import json
from lib.ItemAndTrad.box import *

class item:
    def __init__(self):
        self.box = box()
        self.itemdata = {}
        self.moneyData = {}
        self.loadItemData()
        self.loadMoneyData()
        self.loadBox()

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

    def loadBox(self):
        #箱子名稱     所有物品名稱0,               1:chanse(第幾項,機率)     ,2:cost, 3:開到第幾項
        with open("./lib/ItemAndTrad/boxdata.json" , "r") as f:
            self.boxdata = json.load(f)
        self.AllBoxCount = {}
        for i in self.boxdata:
            self.AllBoxCount[i] = 0
            for j in self.boxdata[i][1]:
                self.AllBoxCount[i] += j[1]

    def openBox(self,userName,boxName,count):
        self.loadItemData()
        self.loadMoneyData()
        allOpen = {}

        try:
            money = self.moneyData[userName][1]
        except:
            return ["not find his money"]
        try:
            openbox = self.box.boxes[boxName]
        except:
            return ["not find box"]
        boxCost = openbox[2] * count
        if boxCost > money:
            return ["not enough money" ]
        else:
            money -= boxCost#扣錢
            self.moneyData[userName][1] = money
        
        boxAllItemCount = len(self.box.boxes[boxName][1])# 大量開
        if count > boxAllItemCount:
            a = count % boxAllItemCount
            b = (count -a) // boxAllItemCount
            print(self.boxdata[boxName][2])

            for i in self.boxdata[boxName][1]:
                itemName = self.boxdata[boxName][0] [i[0]]

                if not userName in self.itemdata :
                    self.itemdata[userName] = {}
                if itemName in self.itemdata[userName]:
                    self.itemdata[userName][self.boxdata[boxName][0] [i[0]] ] += b * i[1]
                else:
                    self.itemdata[userName][self.boxdata[boxName][0] [i[0]] ] = b * i[1]
                allOpen [itemName ] = b * i[1]
            count = a

        out = ""
        for i in range(count):# 一個一個開
            # try:
            #     money = self.moneyData[userName][1]
            # except:
            #     return ["not find his money"]
            out = self.box.openBox(money,boxName)
            # if out == "notEnoughMoney":
            #     return ["not enough money" ]
            # if out == "notFindBox":
            #     return ["not find box"]
            
            if userName in self.itemdata :
                if out in self.itemdata[userName] :
                    self.itemdata[userName][out] +=1
                else:
                    self.itemdata[userName][out] =1
                if out in allOpen :
                    allOpen[out] += 1
                else:
                    allOpen[out]  = 1
                
            else: 
                self.itemdata[userName] = {}
                if out[0] in self.itemdata[userName] :
                    self.itemdata[userName][out] +=1
                else:
                    self.itemdata[userName][out] =1
                if out[0] in allOpen :
                    allOpen[out] += 1
                else:
                    allOpen[out]  = 1

        self.saveItemData()
        self.saveMoneyData()
        print(out)

        return [allOpen,out,self.moneyData[userName][1]]
    