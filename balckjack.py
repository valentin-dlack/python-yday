import random

cardDict = {1: "1", 2: "2", 3 : "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
    10: "10", 11: "11", 12: "12", 13: "13"}
colors = ["Piques", "Carreaux", "Coeurs", "Trèfles"]

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value

    def getColor(self):
        return self.color

    def toString(self):
        keys = list(cardDict.keys())
        if keys[int(self.value)] == 11:
            stres = "Valet"
        elif self.value == 12:
            stres = "Dame"
        elif self.value == 13:
            stres = "Roi"
        else:
            stres = self.value
        return str(stres) + " de " + self.color

class Cards:

    def __init__(self,cardList,count):
        self.cardList = cardList
        self.count = count
        
    def getList(self):
        return self.cardList
        
    def setList(self, listArg):
        self.cardList = listArg
        
    def setCount(self, count):
        self.count = count

    def makePack(self):
        result = []
        for j in range(4):
            for k, v in cardDict.items():
                if (k == 11 or k == 12 or k == 13):
                    value = 10
                else:
                    value = v
                new = Card(value, colors[j])
                result.append(new)
        random.shuffle(result)
        return result
    
    def takeout(self):
            self.cardList.pop(0)
            self.count -= 1

def isWin(cardList): 
    res = 0
    for i in range(len(cardList)):
        res += int(cardList[i].getValue())
    if res == 21:
        return 1 ##win
    elif (res < 21):
        return 0 ##continue
    else:
        return 2 ##lose
    
def stopCroupier(cardList): 
    res = 0
    for i in range(len(cardList)):
        res += int(cardList[i].getValue())
    if res <= 16:
        return False
    else:
        return True
    
lot = Cards([], 0)
lot.setList(lot.makePack())
lot.setCount(len(lot.getList()))

def game_engine():
    tourCount = 0
    passed = False
    mainCards = []
    croupierMain = []
    mainCards.append(lot.getList()[0])
    lot.takeout()
    croupierMain.append(lot.getList()[0])
    lot.takeout()
    mainCards.append(lot.getList()[0])
    lot.takeout()
    
    # Gestion joueur
    while (passed == False and isWin(mainCards) == 0):
        print("Tour numéro (Joueur) : " + str(tourCount+1))
        print("Vous avez les cartes :")
        strres = 0
        for i in range(len(mainCards)):
                    strres += int(mainCards[i].getValue())
        for i in range(len(mainCards)):
            print(mainCards[i].toString() + " - ", end="")
        print(strres)
        val = input("\nQue voulez vous faire (pioche | pass) : ")
        if (val == "pioche"):
            if (lot.getList()[0].getValue() == "1"):
                res = 0
                for i in range(len(mainCards)):
                    res += int(mainCards[i].getValue())
                if ((res + 11) > 21):
                    lot.getList()[0].setValue(1)
                else:
                    lot.getList()[0].setValue(11)
            mainCards.append(lot.getList()[0])
            lot.takeout()
            tourCount += 1
            print(isWin(mainCards))
        elif (val == "pass"):
            passed = True
            break
        else:
            print("Argument invalide... Veuillez réessayer")
    #Gestion res == 21 (win)
    if (isWin(mainCards) == 1):
        res = 0
        for i in range(len(mainCards)):
            res += int(mainCards[i].getValue())
        print("Vous avez gagné !! Vos cartes : ")
        for i in range(len(mainCards)):
            print(mainCards[i].toString() + " - ", end="")
        print("\n constituent un total de : " + str(res) + " points")
    
    #Gestion res > 21 (perdu)
    if (isWin(mainCards) == 2):
        res = 0
        for i in range(len(mainCards)):
            res += int(mainCards[i].getValue())
        print("Perdu :'(  Vos cartes : ")
        for i in range(len(mainCards)):
            print(mainCards[i].toString() + " - ", end="")
        print("\n constituent un total de : " + str(res) + " points")
    
    #Gestion croupier
    if (isWin(mainCards) == 0):
        print("Le croupier pioche...")
        while(stopCroupier(croupierMain) == False):
            croupierMain.append(lot.getList()[0])
            lot.takeout()
        
        resMain = 0
        for i in range(len(mainCards)):
                resMain += int(mainCards[i].getValue())
        resCroup = 0
        for i in range(len(croupierMain)):
                resCroup += int(croupierMain[i].getValue())
                
        if (resMain > resCroup):
            print("Vous avez gagné")
        else:
            print("Le croupier a gagné")
        
game_engine()