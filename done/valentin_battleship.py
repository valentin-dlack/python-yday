import random
import sqlite3
import tkinter as tk
from functools import partial

conn = sqlite3.connect("battleship_scores.db")
cursor = conn.cursor()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

SHOTS = []
BOARD = []
SHIPS = []
MAX_SHOTS = 35
NBSHOTS = 0


def build_board(cells):
    return [['0' for _ in range(cells)] for _ in range(cells)]

def print_board(board):
    for cell in board:
        print(*cell)

def build_ship(cells):
    len_ship = random.randint(2, 5)
    orientation = random.randint(0, 1)
    # horizontal = 0 // vertical = 1

    if orientation == 0:
        row_ship = [random.randint(0, cells-1)] * len_ship
        column = random.randint(0, cells - len_ship)
        column_ship = list(range(column, column + len_ship))
        coordinate = tuple(zip(row_ship, column_ship))
    else:
        column_ship = [random.randint(0, cells-1)] * len_ship
        row = random.randint(0, cells - len_ship)
        row_ship = list(range(row, row + len_ship))
        coordinate = tuple(zip(row_ship, column_ship))
    return list(coordinate), orientation

def process_ships():
    nbShip = 5
    ships = []
    boat = ()
    for i in range(nbShip):
        while True:
            flag = False
            boat, orient = build_ship(10)
            for ship in ships:
                for pos in boat:
                    if pos in ship:
                        flag = True
                        break
                if flag:
                    break  
            if not flag:
                ships.append(boat)         
                break
    print(ships)
    return ships

def user_input():
    row = int(input("Ligne: ")) - 1 #-1 pour la base 0
    col = int(input("Colonne: ")) -1
    return (row, col)

def game_engine(shot, board, ships, shots):
    if shot in shots:
        return board, 0
    shots.append(shot)
    
    for ship in ships:
        if shot in ship:
            board[shot[0]][shot[1]] = bcolors.FAIL+bcolors.BOLD+'X'+bcolors.ENDC
            ship.remove(shot)
            return board, 1
    return board, 0

def buttonPlay(label, window):
    global SHOTS
    global BOARD
    global SHIPS
    global MAX_SHOTS
    global NBSHOTS
    label.config(text = "Let's Play !")
    window.destroy()
    SHOTS = []
    BOARD = []
    SHIPS = []
    MAX_SHOTS = 35
    NBSHOTS = 0
    windowSetup()



btnList = []
def windowSetup():
    cursor.execute("SELECT * FROM scores ORDER BY score ASC LIMIT 5")
    rows = cursor.fetchall()

    global BOARD
    global SHIPS
    global SHOTS
    global descLabel
    alphab = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    root = tk.Tk()
    root.resizable(0, 0)
    root.title('Jeux de bataille navale')

    frame = tk.Frame(root, bg='#FFFFFF')
    for i in range(10):
        for j in range(10):
            index = 10*i+j
            tk.Label(frame, text=str(i+1)).grid(row=0, column=i+1)
            tk.Label(frame, text=alphab[i]).grid(row=i+1, column=0)
            tempBtn = tk.Button(frame, text=str(i)+","+str(j), fg="#FFFFFF", activeforeground="#FFFFFF", height=5, width=10, bg='#FFFFFF', borderwidth=3, relief="flat", command=partial(clickCase, index))
            tempBtn.grid(row=i+1, column=j+1)
            btnList.append(tempBtn)
    tk.Label(frame, text="Jeu de bataille navale en python", font=("Helvetica", 14), bg="#FFFFFF").grid(row=1, column=11, padx=75, pady=20)
    descLabel = tk.Label(frame, text="", font=("Helvetica", 14), bg="#FFFFFF")
    descLabel.grid(row=2, column=11)
    scoresLabel = tk.Label(frame, text="--- HIGHSCORES ---", font=("Helvetica", 14), bg="#FFFFFF")
    scoresLabel.grid(row=3, column=11)
    strScore = ""
    for row in rows:
        strScore += "" + str(row[0]) + " : " + str(row[1]) + " coups !\n"
    scoreLabel = tk.Label(frame, text=strScore, font=("Helvetica", 14), bg="#FFFFFF")
    scoreLabel.grid(row=4, column=11)
    playBtn = tk.Button(frame, text="JOUER", height=4, width=20, borderwidth=3, relief='groove', command=lambda: buttonPlay(descLabel, root)).grid(row=6, column=11)
    quitBtn = tk.Button(frame, text="QUITTER", height=4, width=20, borderwidth=3, relief='groove', foreground='red', command=quitWindow).grid(row=7, column=11)
    #debugBtn = tk.Button(frame, text="Debug", height=4, width=20, borderwidth=3, relief='groove', foreground='red', command=loadNameWindow).grid(row=8, column=11)

    frame.pack(expand=True) 

    BOARD = build_board(10)
    SHIPS = process_ships()
    root.mainloop()

def quitWindow():
    exit()
    conn.close()

def addDb(entry, window):
    global NBSHOTS
    username = entry.get()
    score=NBSHOTS
    cursor.execute("INSERT INTO scores (username, score) VALUES (?,?)", (username, score))
    conn.commit()
    window.destroy()

def loadNameWindow():
    login = tk.Tk()
    test=tk.StringVar()
    login.geometry("300x500")
    username_label = tk.Label(login, text = "Nom d'utilisateur :", font =("Helvetica", 14))
    username_entry = tk.Entry(login, font=("Helvetica", 14))
    sub_btn = tk.Button(login, text = "Submit", command= lambda: addDb(username_entry, login))

    username_label.grid(row=0, column=0)
    username_entry.grid(row=0, column=1)
    sub_btn.grid(row=1, column=1)
    login.mainloop()

def clickCase(btn):
    global NBSHOTS
    NBSHOTS +=1
    global BOARD
    global SHIPS
    global descLabel
    x, y = btnList[btn].cget("text").split(",")
    BOARD, status = game_engine((int(x), int(y)), BOARD, SHIPS, SHOTS)
    if status == 1:
        btnList[btn].config(bg="#00cc00")
        btnList[btn].config(state=tk.DISABLED)
    elif status == 0:
        btnList[btn].config(bg="#0099ff")
        btnList[btn].config(state=tk.DISABLED)
    descLabel.config(text = "Nombre de coups restant = " + str(MAX_SHOTS - NBSHOTS))
    if NBSHOTS == MAX_SHOTS:
        descLabel.config(text = "GAME OVER, VOUS AVEZ PERDU", fg="red")
        for btn in btnList:
            btn.config(state=tk.DISABLED)
        return
    if not any(SHIPS):
        descLabel.config(text = "VOUS AVEZ GAGNÉ !", fg="green")
        for btn in btnList:
            btn.config(state=tk.DISABLED)
        loadNameWindow()
        return
    

def main():
    windowSetup()

main()