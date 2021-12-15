# RENDU TP.1 -- Ydays Python

- [RENDU TP.1 -- Ydays Python](#rendu-tp1----ydays-python)
  - [Ce que j'ai ajouté aux classes :](#ce-que-jai-ajouté-aux-classes-)
    - [Classe `Card` :](#classe-card-)
    - [Classe `Cards` :](#classe-cards-)
  - [Code du jeu en lui même :](#code-du-jeu-en-lui-même-)
    - [Les Fonction (hors moteur du jeu) :](#les-fonction-hors-moteur-du-jeu-)

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

