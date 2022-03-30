import nextcord
import os
import sqlite3
import json
from nextcord.ext import commands, ipc
from dotenv import load_dotenv
load_dotenv()
default = "!"

conn = sqlite3.connect("../database/prefix.db")
cursor = conn.cursor()

async def get_prefix(client, message):
    admin_roles = [role for role in message.guild.roles if role.permissions.administrator]
    cursor.execute(f'SELECT prefix FROM guilds WHERE guild_id = {message.guild.id}')
    res = cursor.fetchone()
    if res:
        return res
    else:
        try:
            cursor.execute(f"SELECT prefix FROM guilds WHERE guild_id = {message.guild.id}")
            result = cursor.fetchone()
            if result:
                cursor.execute(f"UPDATE guilds SET prefix = '{default}', name = '{client.user.name}', adm_roles = '{admin_roles}', warn_before_ban = 0 WHERE guild_id = {message.guild.id}")
            else:
                cursor.execute(f"INSERT INTO guilds (prefix, name, adm_roles, warn_before_ban, guild_id) VALUES ('{default}','{client.user.name}','{admin_roles}',0,{message.guild.id})")
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
    cursor.execute('CREATE TABLE IF NOT EXISTS guilds (prefix TEXT NOT NULL, welcome_chan INT, log_chan INT, name TEXT NOT NULL, adm_roles TEXT NOT NULL, banword TEXT, warn_before_ban INT NOT NULL, guild_id INT NOT NULL)')
    conn.commit()
    
@my_bot.event
async def on_guild_join(guild):
    admin_roles_dict = {}
    for role in guild.roles:
        if role.permissions.administrator:
            admin_roles_dict[role.name] = role.id
    admin_roles = json.dumps(admin_roles_dict)
    cursor.execute("INSERT INTO guilds (prefix, name, adm_roles, warn_before_ban, guild_id) VALUES (?,?,?,?,?)", (default, my_bot.user.name, admin_roles, 0, guild.id))
    conn.commit()
    
@my_bot.event
async def on_guild_remove(guild):
    cursor.execute(f'SELECT prefix FROM guilds WHERE guild_id = {guild.id}')
    res = cursor.fetchone()
    if res:
        cursor.execute(f'DELETE FROM guilds WHERE guild_id = {guild.id}')
    conn.commit()
    
@my_bot.event
async def on_message(message):
    if message.author.bot:
        return
    cursor.execute(f'SELECT banword FROM guilds WHERE guild_id = {message.guild.id}')
    res = cursor.fetchone()
    banlist = json.loads(res[0])
    for banword in banlist:
        if message.content.lower().find(banword["value"].lower()) != -1:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Dis pas ça !! :(")
            return

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
    text_channel_list = {}
    for channel in guild.channels:
        if str(channel.type) == 'text':
            text_channel_list[channel.id] = channel.name
    guild_data = {
		"name": guild.name,
		"id": guild.id,
        "member_count": guild.member_count,
        "owner": guild.owner.name,
        "icon_url": guild.icon.url,
        "banner_url": guild.banner.url if guild.banner else None,
        "channels": text_channel_list,
        "nickname": my_bot.user.name,
	}
    return guild_data

if __name__ == "__main__":
    my_bot.ipc.start()  # start the IPC Server
    my_bot.run(os.environ.get("BOT_TOKEN"))