import random

class box:
    def __init__(self):
                        #箱子名稱     所有物品名稱0,               1:chanse(第幾項,機率)     ,2:cost, 3:開到第幾項
        self.boxes = {"box1"            : [ ["textItem","teem"]      , self.setrollList([[ 0 , 5],[ 1 , 2 ]]) ,10, 0],
                      "money bouns box" : [["x1.1","x1.2","x1,5","x2"], self.setrollList([[0,10],[1,6],[2,4],[3,1]]) , 100 ,0]}
        self.output = []

    def openBox(self,usermoney,boxname) :
        try:
            boxData = self.boxes[boxname]
        except : return "notFindBox"

        if usermoney >= boxData[2] :
            get = boxData[0][ boxData[1][ boxData[3] ] ]
            boxData[3] +=1
            if boxData[3] > len(boxData[1]) -1 :
                boxData[3] = 0
        else:
            return "notEnoughMoney"
        
        usermoney -= boxData[2]
        return [get , usermoney]
        
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