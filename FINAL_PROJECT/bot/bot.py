import nextcord
import os
from nextcord.ext import commands, ipc
from dotenv import load_dotenv
load_dotenv()

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="secret")  # create IPC Server

    async def on_ipc_ready(self):
        print("IPC is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)
        
    async def on_ready(self):
        print("Bot is ready.")

my_bot = MyBot(command_prefix="!", intents=nextcord.Intents.all())

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
async def get_guild(data):
    guild = my_bot.get_guild(
        data.guild_id
    )
    if guild is None: return None
    guild_data = {
		"name": guild.name,
		"id": guild.id,
		"prefix" : "?"
	}
    return guild_data

if __name__ == "__main__":
    my_bot.ipc.start()  # start the IPC Server
    my_bot.run(os.environ.get("BOT_TOKEN"))