# bot.py
import os

import discord, random
from dotenv import load_dotenv
from discord import Member

load_dotenv()
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description='owo i sure do L-O-V-E programming')
TOKEN = os.environ.get('TOKEN', 3)
CHANNEL = os.environ.get('CHANNEL', 3)
AUTHOR_ID = os.environ.get('AUTHOR_ID', 3)
print(AUTHOR_ID)






def is_it_me(ctx):
    return ctx.author.id == AUTHOR_ID



@bot.event
async def on_ready():
    all_channels = bot.get_all_channels()
    bot_channel = None
    for chans in all_channels:
        if chans.id == CHANNEL:
            bot_channel = chans
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you all code"))
    await bot_channel.send('im ready senpai uwu')
    print('yo was poppin ;)')


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
