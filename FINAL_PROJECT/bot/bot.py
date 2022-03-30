import nextcord
import os
import sqlite3
from nextcord.ext import commands, ipc
from dotenv import load_dotenv
load_dotenv()
default = "!"

conn = sqlite3.connect("../database/prefix.db")
cursor = conn.cursor()

async def get_prefix(client, message):
    cursor.execute(f'SELECT prefix FROM guilds WHERE guild_id = {message.guild.id}')
    res = cursor.fetchone()
    if res:
        return res
    else:
        try:
            cursor.execute(f"SELECT prefix FROM guilds WHERE guild_id = {message.guild.id}")
            result = cursor.fetchone()
            if result:
                cursor.execute(f"UPDATE guilds SET prefix = '{default}' WHERE guild_id = {message.guild.id}")
            else:
                cursor.execute(f"INSERT INTO guilds (prefix, guild_id) VALUES ('{default}',{message.guild.id})")
            conn.commit()
            cursor.execute(f"SELECT prefix FROM guilds WHERE guild_id = {message.guild.id}")
            result = cursor.fetchone()
            return result
        except Exception:
            return "d!"

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="secret")  # create IPC Server

    async def on_ipc_ready(self):
        print("IPC is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

my_bot = MyBot(command_prefix=get_prefix, intents=nextcord.Intents.all())

@my_bot.event
async def on_ready():
    print("Bot is up and Ready to go !")
    cursor.execute('CREATE TABLE IF NOT EXISTS guilds (prefix TEXT NOT NULL, guild_id INT NOT NULL)')
    conn.commit()
    
@my_bot.event
async def on_guild_join(guild):
    cursor.execute(f"INSERT INTO guilds (prefix, guild_id) VALUES ('{default}',{guild.id})")
    conn.commit()
    
@my_bot.event
async def on_guild_remove(guild):
    cursor.execute(f'SELECT prefix FROM guilds WHERE guild_id = {guild.id}')
    res = cursor.fetchone()
    if res:
        cursor.execute(f'DELETE FROM guilds WHERE guild_id = {guild.id}')
    conn.commit()

@my_bot.command()
async def ping(ctx):
    await ctx.reply('Pong!')

@my_bot.ipc.route()
async def get_member_count(data):
    guild = my_bot.get_guild(
        data.guild_id
    )  # get the guild object using parsed guild_id
    return guild.member_count  # return the member count to the client

@my_bot.ipc.route()
async def get_guild_count(data):
    return len(my_bot.guilds)

@my_bot.ipc.route()
async def get_guild_ids(data):
    res = []
    for guild in my_bot.guilds:
        res.append(guild.id)
    return res

@my_bot.ipc.route()
async def set_prefix(prefix, g_id):
    cursor.execute('SELECT')

@my_bot.ipc.route()
async def get_guild(data):
    guild = my_bot.get_guild(data.guild_id)
    if guild is None: return None
    guild_data = {
		"name": guild.name,
		"id": guild.id,
        "member_count": guild.member_count,
        "owner": guild.owner.name,
        "icon_url": guild.icon.url,
        "banner_url": guild.banner.url if guild.banner else None
	}
    return guild_data

if __name__ == "__main__":
    my_bot.ipc.start()  # start the IPC Server
    my_bot.run(os.environ.get("BOT_TOKEN"))