import random
import json

class box:
    def __init__(self):
        self.boxes = {}
        self.output = []
        self.loadBox()

    def loadBox(self):
        #箱子名稱     所有物品名稱0,               1:chanse(第幾項,機率)     ,2:cost, 3:開到第幾項
        with open("./lib/ItemAndTrad/boxdata.json" , "r") as f:
            self.boxes = json.load(f)
        for i in self.boxes :
            self.boxes[i]. append(0)
            self.boxes[i][1] = self.setrollList(self.boxes[i][1])
            print(self.boxes)

    def restBox(self):
        for i in self.boxes :
            self.boxes[i][3] = 0
            self.boxes[i][1] = self.setrollList(self.boxes[i][1])

    def openBox(self,boxname) :
        try:
            boxData = self.boxes[boxname]
        except : return "notFindBox"

        get = boxData[0][ boxData[1][ boxData[3] ] ]
        boxData[3] +=1
        if boxData[3] > len(boxData[1]) -1 :
            boxData[3] = 0
            
        return get
        
    def setrollList(self,rollChanse):
        rollList = []
        for i in rollChanse:
            for j in range(i[1]):
                rollList.append(i[0])

        for i in range( len(rollList) *2):
            a  = random.randint(0 , len(rollList) -1)
            b  = random.randint(0 , len(rollList) -1)
            while a == b:#排除重複
                b  = random.randint(0 , len(rollList) -1)

            c = rollList[a]
            rollList[a] = rollList[b]
            rollList[b] = c
        print(str(rollList) + "\n")
        return rollList