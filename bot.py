# bot.py
import os

import discord, random
from dotenv import load_dotenv
from discord import Member

load_dotenv()
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description='owo i sure do L-O-V-E programming')
TOKEN = os.environ.get('TOKEN', 3)
AUTHOR_ID = os.environ.get('AUTHOR_ID', 3)
print(AUTHOR_ID)


@bot.event
async def on_ready():
    bot_channel = bot.get_channel(697537529737510932)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you all code"))
    await bot_channel.send('im awake senpai and ready to serve uwu')
    print('bot.py is active')


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='participant')
    await member.add_roles(role)


@bot.command()
async def load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def unload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def reload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')
            bot.load_extension(f'cogs.{filename[:-3]}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
