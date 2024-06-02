import json

class numberCount:
    def __init__(self):
        self.number = 1
        self.reload()

    def reload(self):
        with open("./saves/numberCount.json" ,"r") as f:
            self.data = json.load(f)
        
    def add(self):
        self.number += 1
    
    def test(self,user,testNumber):
        try:
            testNumber = int(testNumber)
            if testNumber == self.number:
                self.add()
                self.V(user)
                return 1
            else:
                self.number = 1
                self.X(user)
                return 2
        except:
            return 3
        
    def X(self,userName):
        if userName not in self.data:
            self.data[userName] = [0,1]
        else:
            self.data[userName][1] += 1
        with open("./saves/numberCount.json","w") as f:
            json.dump(self.data,f)

    def V(self,userName):
        if userName not in self.data:
            self.data[userName] = [1,0]
        else:
            self.data[userName][0] += 1
        with open("./saves/numberCount.json","w") as f:
            json.dump(self.data,f)