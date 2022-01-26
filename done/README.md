# RENDU TP.1 -- Ydays Python

- [RENDU TP.1 -- Ydays Python](#rendu-tp1----ydays-python)
  - [Ce que j'ai ajouté aux classes :](#ce-que-jai-ajouté-aux-classes-)
    - [Classe `Card` :](#classe-card-)
    - [Classe `Cards` :](#classe-cards-)
  - [Code du jeu en lui même :](#code-du-jeu-en-lui-même-)
    - [Les Fonction (hors moteur du jeu) :](#les-fonction-hors-moteur-du-jeu-)
    - [Moteur de jeu :](#moteur-de-jeu-)
    - [Boucle while principale :](#boucle-while-principale-)
    - [Si le jeu est gagné](#si-le-jeu-est-gagné)
    - [Si le jeu est perdu](#si-le-jeu-est-perdu)
    - [Si le joueur passe -> croupier](#si-le-joueur-passe---croupier)

## Ce que j'ai ajouté aux classes :

---

### Classe `Card` :

Méthode `setValue()` :

```py
    def setValue(self, value):
        self.value = value
```

Comme indiqué dans le nom, `setValue` est un setter pour gérer la valeur de la classe `Card`, je l'utilise notamment pour gérer l'As (1 ou 11 selon la valeur après addition)

---

### Classe `Cards` : 

**Getters et Setters de `Cards` :**

Méthode `getList()` :

```py
 def getList(self):
        return self.cardList
```

C'est une simple méthode pour récupérer la liste de cartes.

Méthode `setList()` : 

```py
def setList(self, listArg):
        self.cardList = listArg
```

Pareil ici mais pour ajouter des valeurs à la liste, on l'utilise aussi avec le `makePack()` qu'on verras ensuite.  

Méthode `setCount()`

```py
def setCount(self, count):
        self.count = count
```

Ce setter permet d'ajouter une valeure au compteur.

Dernière méthode de `Class`, c'est `makePack()` :

```py
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
```

Cette méthode permet de génerer un paquet de carte, dans l'ordre. Le résultat est ensuite mélangé aléatoirement. Aussi, on remplace la valeur de 11, 12, 13 (Valet, Dame, Roi) par la valeur 10 pour être adapté au BlackJack.

---

## Code du jeu en lui même :

### Les Fonction (hors moteur du jeu) :

**`isWin(liste de carte)`**

```py
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
```

On check si le resultat de l'addition de toutes les cartes est supérieur ou égal à 21, si c'est égal à 21, alors le jeu est gagné, si c'est en dessous, on continue. Sinon c'est perdu !  

**`stopCroupier(liste de carte)`**

```py 
def stopCroupier(cardList): 
    res = 0
    for i in range(len(cardList)):
        res += int(cardList[i].getValue())
    if res <= 16:
        return False
    else:
        return True
```

Cette méthode est la même que pour le win mais avec le croupier, il pioche tant que la somme reste en dessous de 16

### Moteur de jeu :

- Initialisation des variables et du paquet de carte :

```py
lot = Cards([], 0)
lot.setList(lot.makePack())
lot.setCount(len(lot.getList()))
```

> On initialise d'abord le paquet de carte qui sera déjà mélangé par le `.makePack()`

```py
def game_engine():
    tourCount = 0
    passed = False
    mainCards = []
    croupierMain = []
```

> On défini ensuite les variables qui seront nécessaires au fonctionnement du jeu  
>
-> tourCount : nombre de tours  
-> passed : si le joueur a passé le tour au croupier  
-> mainCards : les cartes dans la main du joueur  
-> croupierMain : main du croupier.  

- Distribution des premières cartes :

```py
    #dans la fonction game_engine()
    mainCards.append(lot.getList()[0])
    lot.takeout()
    croupierMain.append(lot.getList()[0])
    lot.takeout()
    mainCards.append(lot.getList()[0])
    lot.takeout()
```

> On distribu 2 cartes au joueur et une carte au croupier dans l'ordre Player - Croupier - Player

Le `takeout()` permet de retirer la carte que l'on vient d'ajouter à la main du joueur ou du croupier.

> Amélioration possible : Faire une méthode `pioche` qui retire a la pioche et ajoute dans la main automatiquement.

On passe ensuite a la boucle while principale...

---

### Boucle while principale :

**Code :**

```py
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
```

L'affichage ne sera pas pris en compte.  
On demande au joueur si il veut piocher ou si il veut passer (tour du croupier)
- Piocher :
    - Une carte sera ajoutée à sa main, si la somme des cartes est inférieur a 21 (`isWin()` on continue le while, sinon on break)
    - l'As a une particularité, de base il vaut 11, mais si la somme des cartes + 11 est supérieur à 21, alors il vaudra 1 (`if ((res+11) > 21):`)
- Passer :
  - Le tour du joueur est fini et il passe au tour du croupier.

---

### Si le jeu est gagné

**Code :**

```py
    #Gestion res == 21 (win)
    if (isWin(mainCards) == 1):
        res = 0
        for i in range(len(mainCards)):
            res += int(mainCards[i].getValue())
        print("Vous avez gagné !! Vos cartes : ")
        for i in range(len(mainCards)):
            print(mainCards[i].toString() + " - ", end="")
        print("\n constituent un total de : " + str(res) + " points")
```

> On affiche que le joueur a gagné et on lui dis avec quel cartes il a gagné et quel est le total de points (somme de toutes ses cartes), ici c'est forcément 21.

---

### Si le jeu est perdu

**Code :**

```py
    #Gestion res > 21 (perdu)
    if (isWin(mainCards) == 2):
        res = 0
        for i in range(len(mainCards)):
            res += int(mainCards[i].getValue())
        print("Perdu :'(  Vos cartes : ")
        for i in range(len(mainCards)):
            print(mainCards[i].toString() + " - ", end="")
        print("\n constituent un total de : " + str(res) + " points")
```

> On affiche que le joueur a perdu, on lui dis avec quel cartes il a perdu et quel est le total de points (somme de toutes ses cartes), ici c'est forcément plus que 21.

---

### Si le joueur passe -> croupier

**Code :**

```py
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
            print("vous avez gagné")
        else:
            print("Le croupier a gagné")
```

> Dans ce cas de figure, le joueur a passé son tour donc c'est au croupier de jouer.  
> On vérifie au début que `isWin()` soit bien sur 0 (*Inférieur à 21*)  
> Ensuite le croupier pioche des cartes tant que le total de la valeur des ses cartes sont inférieur à 16.  
> Si la valeur totale des cartes du croupier est supérieur à la votre, alors vous avez perdu, sinon, vous avez gagné !