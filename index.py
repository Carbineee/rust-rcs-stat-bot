import os
import discord
import asyncio
import requests
import datetime

from utils import default
from utils.data import Bot, HelpFormat
from discord.ext import commands, tasks

config = default.get("config.json")

print("Logging in...")

bot = Bot(
    command_prefix=config.prefix, prefix=config.prefix,
    owner_ids=config.owners, command_attrs=dict(hidden=True),
    intents=discord.Intents(  # kwargs found at https://discordpy.readthedocs.io/en/latest/api.html?highlight=intents#discord.Intents
        guilds=True, members=True, messages=True, reactions=True, voice_states = True
    )
)

statuses = ['/stats <steamid>', 'discord.gg/rcs']
status = 0

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("discord.gg/rcs")
    bot.remove_command('help')
    await bot.change_presence(status=discord.Status.online, activity=game)

    print("Guilds:" , len(bot.guilds))
    for guild in bot.guilds:
        print(guild)


@tasks.loop(seconds=5.0)
async def gameChange():
    global status
    if status == 0:
        status = 1
    else:
        status = 0
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(statuses[status]))


#Start all of our tasks
gameChange.start()

@gameChange.before_loop
async def before_gameChange():
    await bot.wait_until_ready()


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    bot.run(config.token)
except Exception as e:
    print(f'Error when logging in: {e}')
