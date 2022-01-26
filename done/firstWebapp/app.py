from flask import Flask, render_template, request, session, redirect
import bcrypt
import sqlite3


app = Flask(__name__)
app.config["SECRET_KEY"] = "az7e89r"

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect("db_pkmn.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        if request.form.get("addPokemon"):
            btnId = request.form["addPokemon"]
            
            cursor.execute("INSERT INTO pokedex (user_id, poke_id) VALUES (?,?)", (session['uid'], btnId))
            conn.commit()
        if request.form.get("delPokemon"):
            btnId = request.form["delPokemon"]
            
            cursor.execute(f"DELETE FROM pokedex WHERE id={btnId} AND user_id={session['uid']}")
            conn.commit()
        
    cursor.execute(f"SELECT * FROM pokemon")
    rows = cursor.fetchall()
    
    cursor.execute(f"SELECT pokedex.id, name, ptype, img FROM pokemon INNER JOIN pokedex ON pokemon.id = pokedex.poke_id WHERE user_id = {session['uid']}")
    private_rows = cursor.fetchall()
        
        
    return render_template('home.html', data=rows, data2=private_rows)

@app.route('/logout')
def logout():
    session["user"] = None
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect("db_pkmn.db")
    cursor = conn.cursor()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        
        hash = ""
        cursor.execute(f"SELECT password, id FROM users WHERE name=\"{username}\"")
        rows = cursor.fetchall()
        for row in rows:
            hash = row[0]
        if bcrypt.checkpw(password.encode('UTF-8'), hash):
            session['user'] = username
            session["uid"] = row[1]
            return redirect("/")
        else: return "Le mot de passe n'est pas valide..."
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    conn = sqlite3.connect("db_pkmn.db")
    cursor = conn.cursor()
    	
    if  request.method == 'POST':
	
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass'].encode("utf-8")
        hashd = bcrypt.hashpw(password, bcrypt.gensalt())
        
        cursor.execute("INSERT INTO users (name, password) VALUES (?,?)", (username, hashd))
        conn.commit()
	
    return render_template('register.html')

if __name__ == '__main__':
    app.run()