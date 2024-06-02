import random
import json

class Minesweeper:
    def __init__(self):
        self.mapSize = [10,10]
        self.mapSizeX = self.mapSize[0]
        self.mapSizeY = self.mapSize[1]
        self.mines = 20
        self.numberEmoji = [":zero:",":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"]
        self.rankadd = 0

        self.loadAll()

    def startSet(self):
        self.nowData = {
            "userDigCounts" : {},
            "userFlagCounts" : {},
            "userUnflagCounts" : {}
        }

    def CreatMap(self):
        self.map = []
        for i in range(self.mapSizeY):
            d = []
            for j in range(self.mapSizeX):
                d.append([0,0,0])
            self.map.append(d)

        #mapTypes:
        # 第一項
        # 0: none
        # 1: diged
        # 3: mine
        # 第二項 : 4周地雷數
        # 第三項 : flag

        for i in range(self.mines):
            x = random.randint(0 , self.mapSizeX - 1)
            y = random.randint(0 , self.mapSizeY - 1)
            while self.map[y][x][0] == 3:
                x = random.randint(0 , self.mapSizeX - 1)
                y = random.randint(0 , self.mapSizeY - 1)
            
            self.map[y][x][0] = 3

            if y > 0 : 
                if x > 0                and self.map[y - 1][x - 1][0] != 3 : self.map[y - 1][x - 1][1] += 1
                if x < self.mapSizeX -1 and self.map[y - 1][x + 1][0] != 3 : self.map[y - 1][x + 1][1] += 1
                if self.map[y - 1][x][0] != 3 : self.map[y - 1][x][1] += 1
            if y < self.mapSizeY -1 : 
                if x > 0                and self.map[y + 1][x - 1][0] != 3 : self.map[y + 1][x - 1][1] += 1
                if x < self.mapSizeX -1 and self.map[y + 1][x + 1][0] != 3 : self.map[y + 1][x + 1][1] += 1
                if self.map[y + 1][x][0] != 3 : self.map[y + 1][x][1] += 1
            if x > 0                and self.map[y][x - 1][0] != 3 : self.map[y][x - 1][1] += 1
            if x < self.mapSizeX -1 and self.map[y][x + 1][0] != 3 : self.map[y][x + 1][1] += 1

        self.saveMap()

    def ChangeMapToText(self):
        text = ""
        for i in self.map:
            t = ""
            for j in i :
                if j[0] == 3: t += "x"
                else:
                    t += str( j[1] )
                t += ","

            text += (t + "\n")
        return text
    
    def ChangeMapToTextAddEmojiShowMines(self):
        text = ":slight_smile::expressionless:  "
        for i in range(self.mapSizeX):#第一排數字(十位)
            text +=  self.numberEmoji[self.k(i)[0]] + "   "
        text += "\n:stuck_out_tongue::thumbsup:  "
        for i in range(self.mapSizeX):#第一排數字(各位)
            text +=  self.numberEmoji[self.k(i)[1]] + "   "
        text += "\n"
        a = 0
        for i in self.map:
            t =   self.numberEmoji[self.k(a)[0]] + self.numberEmoji[self.k(a)[1]] + "  "#內部的東東
            for j in i :
                if j[2] == 1 and j[0] != 1: t += ":triangular_flag_on_post:"
                #elif j[0] == 0 : t += "🔲"
                elif j[0] == 3: t += ":x:"
                else:
                    t += self.numberEmoji[j[1]]
                t += "   "

            text += (t + "\n")
            a +=1
        return text
    
    def ChangeMapToTextAddEmoji(self):
        text = ":slight_smile::expressionless:     "
        for i in range(self.mapSizeX):#第一排數字(十位)
            text +=  self.numberEmoji[self.k(i)[0]] + ""
        text += "\n:stuck_out_tongue::thumbsup:     "
        for i in range(self.mapSizeX):#第一排數字(各位)
            text +=  self.numberEmoji[self.k(i)[1]] + ""
        text += "\n\n"
        a = 0
        for i in self.map:
            t =   self.numberEmoji[self.k(a)[0]] + self.numberEmoji[self.k(a)[1]] + "     "#內部的東東
            for j in i :
                if j[2] == 1 and j[0] != 1: t += ":triangular_flag_on_post:"
                elif j[0] == 0 : t += "🔲"
                elif j[0] == 3: t += "🔲"
                else:
                    t += self.numberEmoji[j[1]]
                t += ""

            text += (t + "\n")
            a +=1
        return text

    def dig(self,userName,x,y,k):
        if x<0 or y<0 or x> self.mapSizeX or y > self.mapSizeY:
            return
        try:
            if self.map[y][x][0] == 1: return "digged"
            if self.map[y][x][0] == 3 :
                return "lose"
            self.map[y][x][0] = 1
            self.map[y][x][0] = 1
            print([x,y])

            #挖旁邊的
            if  self.map[y    ][x - 1][0] == 0 and self.map[y][x][1] == 0: self.dig(userName,x - 1,y - 1,True)
            if  self.map[y - 1][x - 1][0] == 0 and self.map[y][x][1] == 0: self.dig(userName,x - 1,y    ,True)
            if  self.map[y + 1][x - 1][0] == 0 and self.map[y][x][1] == 0: self.dig(userName,x - 1,y + 1,True)
            if  self.map[y - 1][x    ][0] == 0 and self.map[y][x][1] == 0: self.dig(userName,x    ,y - 1,True)
            if  self.map[y + 1][x    ][0] == 0 and self.map[y][x][1] == 0: self.dig(userName,x    ,y + 1,True)
            if  self.map[y - 1][x + 1][0] == 0 and self.map[y][x][1] == 0: self.dig(userName,x + 1,y - 1,True)
            if  self.map[y    ][x + 1][0] == 0 and self.map[y][x][1] == 0: self.dig(userName,x + 1,y    ,True)
            if  self.map[y + 1][x + 1][0] == 0 and self.map[y][x][1] == 0: self.dig(userName,x + 1,y + 1,True)

            if not k: 
                self.addNowData(userName,"userDigCounts")
                self.rankadd = self.mapSizeX * self.mapSizeY * self.mines /15 - 10

            return "fine"
        except:
            if not k:pass
              
    def flag(self,userName,x,y):
        try:
            self.map[y][x][2] = 1
            self.addNowData(userName,"userFlagCounts")
            self.rankadd = 1
            return "fine"
        except:
            return "error"
    
    def unflag(self,userName,x,y):
        try:
            self.map[y][x][2] = 0
            self.addNowData(userName,"userUnflagCounts")
            self.rankadd = 0
            return "fine"
        except:
            return "error"
    
    def k(self,number):
        a = number % 10
        b = (number - a) // 10
        return [b,a]
    
    def Enter(self,userName: str,text : str):
        print(self.allData)
        if text[0] == "/":
            try:
                text = text.strip().split(",")
                print(text)
                if   text[0] == "/dig"    : return self.dig(userName,int(text[1]) , int(text[2]),False)
                elif text[0] == "/flag"   : return self.flag(userName,int(text[1]) , int(text[2]))
                elif text[0] == "/unflag" : return self.unflag(userName,int(text[1]) , int(text[2]))
                else: return "error"
            except: return "error"
        else: return "talk"

    def testWin(self):
        self.win = True
        for i in self.map:
            for j in i:
                if j[0] == 0 :self.win  = False
        return self.win
    
    def Win(self,user):
        if user in self.allData["win"]:
            self.allData["win"][user] += 1
        else:
            self.allData["win"][user] = 1
        self.reload()

    def lose(self,user):
        if user in self.allData["lose"]:
            self.allData["lose"][user] += 1
        else:
            self.allData["lose"][user] = 1
        self.saveAllData()
        self.reload()

    def reload(self):
        self.addAllData()
        self.CreatMap()
        self.startSet()

    def loadNowData(self):
        try:
            with open("./saves/SOLM/now.json","r") as f:
                self.nowData = json.load(f)
        except: self.startSet()

    def saveNowData(self):
        try:
            with open("./saves/SOLM/now.json","w") as f:
                json.dump(self.nowData,f)
        except:pass

    def loadMap(self):
        try:
            with open("./saves/SOLM/map.json","r") as f:
                self.map = json.load(f)["map"]
        except:
            self.CreatMap()

    def saveMap(self):
        with open("./saves/SOLM/map.json","w") as f:
            json.dump({"map":self.map},f)

    def saveAll(self):
        self.saveMap()
        self.saveNowData()
        
    def loadAll(self):
        self.loadMap()
        self.loadNowData()
        self.loadAllData()
    
    def loadAllData(self):
        with open("./saves/SOLM/all.json" , "r") as f:
            self.allData = json.load(f)
            print(self.allData)
            

    def saveAllData(self):
        with open("./saves/SOLM/all.json" , "w") as f:
            print(self.allData)
            json.dump(self.allData,f)

    def addNowData(self,userName,dataName):
        if userName in self.nowData[dataName]:
            self.nowData[dataName][userName] += 1
        else: 
            self.nowData[dataName][userName] = 1

    def addAllData(self):
        for i in self.nowData:
            for j in self.nowData[i]:
                if j in self.allData[i]:
                    self.allData[i][j] += 1
                else:
                    self.allData[i][j] = 1
        self.saveAllData()

# a = stepOnLandMines()
# print(a.k(92))
# print(a.dig(a,1,3,False))
# print(a.dig(a,2,3,False))
# print(a.dig(a,4,0,False))
# print(a.flag(4,3,4))

# print(a.Enter("a","dig,10,11"))
# print(a.Enter("a","dig,10,1l1"))
# print(a.Enter("a","didg,10,1l1"))
# print(a.Enter("a","flag,10,9"))

# print(a.ChangeMapToTextAddEmoji())
# print(a.ChangeMapToText())