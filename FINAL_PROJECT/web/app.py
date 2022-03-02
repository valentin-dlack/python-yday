from dotenv import load_dotenv
import os 
from quart import Quart, render_template, redirect, url_for, request, make_response
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import nextcord
from nextcord.ext import ipc
load_dotenv()

app = Quart(__name__)

app.secret_key = b'secret'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "true"
app.config["DISCORD_CLIENT_ID"] = 940948417545375784
app.config["DISCORD_CLIENT_SECRET"] = os.environ.get('BOT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = os.environ.get('BOT_TOKEN')

discord = DiscordOAuth2Session(app)
ipcClient = ipc.Client(secret_key="secret")

@app.route('/login')
async def login():
    return await discord.create_session()

@app.route('/callback')
async def callback():
    try:
        await discord.callback()
    except:
      return redirect(url_for('/login'))
  
    return redirect(url_for('dashboard'))

@app.route("/")
async def index():
    return await render_template("index.html")

@app.route('/dashboard', methods=['GET', 'POST'])
async def dashboard():
    if not await discord.authorized:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        user = await discord.fetch_user()
        guildCount = await ipcClient.request("get_guild_count")
        guildIds = await ipcClient.request("get_guild_ids")
        try:
            userGuilds = await discord.fetch_guilds()
        except:
            return await redirect(url_for('login'))
        guilds = []
        for guild in userGuilds:
            if guild.permissions.administrator:
                guild.class_color = "green" if guild.id in guildIds else "red"
                guilds.append(guild)
            
        guilds.sort(key=lambda guild: guild.class_color == "red")
    elif request.method == 'POST':
        discord.revoke()
        return redirect(url_for("index"))
    
    return await render_template("dashboard.html", user=user, gc=guildCount, guilds=guilds)

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
    if not await discord.authorized:
        return redirect(url_for('login'))
    
    guild = await ipcClient.request("get_guild", guild_id = guild_id)
    if guild is None:
        return redirect(url_for('https://discord.com/oauth2/authorize?client_id=940948417545375784&scope=bot&permissions=27648860222'))
    return guild["name"]

if __name__ == '__main__':
    app.run(debug=True)