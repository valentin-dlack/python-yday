# RENDU TP.1 -- Ptite game d'eurotruck ?

- [RENDU TP.1 -- Ptite game d'eurotruck ?](#rendu-tp1----ptite-game-deurotruck-)
  - [Ce que j'ai ajouté aux classes :](#ce-que-jai-ajouté-aux-classes-)
    - [Classe `Card` :](#classe-card-)

## Ce que j'ai ajouté aux classes :

---

### Classe `Card` :

Méthode `setValue()` :

```py
    def setValue(self, value):
        self.value = value
```

Comme indiqué dans le nom, `setValue` est un setter pour gérer la valeur de la classe `Card`, je l'utilise notamment pour gérer l'As (1 ou 11 selon la valeur après addition)

