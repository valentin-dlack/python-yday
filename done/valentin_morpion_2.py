white = 255,255,255
black = 0,0,0
import os
import pygame

grid=["#","#","#","#","#","#","#","#","#"]        

def playerPion():
    while(True):
        first = input("Joueur 1 : Choisi 'X' ou 'O': ")
        if (first.upper() == 'X'):
            print("Tu as choisi 'X'")
            second = 'O'
            print("Le Joueur 2 aura donc 'O'")
            return first.upper(),second
        elif (first.upper() == 'O'):
            print("Tu as choisi 'O'")
            second = 'X'
            print("Le Joueur 2 aura donc 'X'")
            return first.upper(),second
        else: 
            print("Le charactère renvoyé est invalide.")


def displayGrid(grille):
    res = ""
    for i in range(1, len(grille)+1):
        res += grille[i-1] + "|"
        if(i%3 == 0 and not 0):
            res += "\n"
            res += "------"
            res += "\n"
    return res


def addPion(grille, pion, pos):
    grille[pos] = pion
    return grid

def checkCase(grille, i):
    return grille[i] == "#"


def getInput(grille):
    nbr_no = False
    choice = input("Choisissez une case entre 1 et 9: ")
    if int(choice) < 1 or int(choice) > 9:
        nbr_no = True
    while nbr_no:
        choice = input("Ce nombre n'est pas dans la grille, Choisissez une case entre 1 et 9: ")
        if int(choice) >= 1 or int(choice) <= 9:
            nbr_no = False
    while not checkCase(grille, int(choice)-1):
            choice = input("Cette case est déjà occupée. Choisi une autre case entre 1 et 9: ")
    return choice


def checkWin(grille, mark):
    #Win Ligne horizontale
    if grille[0] == grille[1] == grille[2] == mark:
        return True
    if grille[3] == grille[4] == grille[5] == mark:
        return True
    if grille[6] == grille[7] == grille[8] == mark:
        return True
    #Win Ligne Verticale
    if grille[0] == grille[3] == grille[6] == mark:
        return True
    if grille[1] == grille[4] == grille[7] == mark:
        return True
    if grille[2] == grille[5] == grille[8] == mark:
        return True
    #Win diagonale 
    if grille[0] == grille[4] == grille[8] == mark:
        return True
    if grille[2] == grille[4] == grille[6] == mark:
        return True
    return False
    
# [0, 1, 2]
# [3, 4, 5]
# [6, 7, 8]

def checkEquality(grille):
    if not "#" in grille:
        return True


def main():
    pion1 ,pion2 = playerPion()
    i = 1
    pion = ""
    pygame.init() # lancement de l'interface
    pygame.display.set_caption('Morpion') # Nom de l'interface
    screen = pygame.display.set_mode((300,300)) #Définition de la taille de l'interface
    smallfont = pygame.font.SysFont('Segoe UI',30)
    screen.fill(white)
    ended = False
    while not ended: # On créer une boucle infinie pour garder l'interface
        for j in range(3):
            for k in range(3):
                pygame.draw.rect(screen,black,[100*j, 100*k, 100, 100],1)
        for event in pygame.event.get(): # Fonction pour récupérer les event ( clics souris, touches du clavier)
            if event.type == pygame.QUIT: 
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if i%2 == 0:
                        pion = pion2
                    else: 
                        pion = pion1
                    posx = event.pos[0]//100
                    posy = event.pos[1]//100
                    print(posx,posy)
                    text = smallfont.render(pion , True , black)
                    pos = posy*3+posx
                    if checkCase(grid, pos):
                        addPion(grid, pion, pos)
                        screen.blit(text , (100*posx+40,100*posy+25))
                        i += 1
                    if checkWin(grid, pion):
                        print("Vous avez gagné !")
                        ended=True
                    ended=checkEquality(grid)
                    
        pygame.display.flip()

        
        
        
        # print(displayGrid(grid))

        
        
        game_over=checkEquality(grid)


main()