# bot.py
import os
from firebase import firebase

import discord, random
from dotenv import load_dotenv
from discord import Member


import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

load_dotenv()
from discord.ext import commands


data = {
    "USER":'username',
    'TEAM':'team',

}

bot = commands.Bot(command_prefix='!', description='owo i sure do L-O-V-E programming')
TOKEN = os.environ.get('TOKEN', 3)
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)

firebase = firebase.FirebaseApplication(FIREBASE, None)

@bot.event
async def on_ready():
    bot_channel = bot.get_channel(697537529737510932)
    sunglasses = bot.get_emoji(698234865576968203)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you all code", emoji=sunglasses))
    await bot_channel.send('im awake senpai and ready to serve uwu')
    print('bot.py is active')



@bot.command(name='ping')
async def ping(ctx):
    data = {
        "USER": 'pong',
        'TEAM': 'ping',
    }
    result = firebase.post(FIREBASE_NAME+'/Team', data)
    print(result)
    await ctx.send('pong')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='participant')
    await member.add_roles(role)


@bot.command()
@commands.has_role('exec')
async def load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
@commands.has_role('exec')
async def unload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')


@bot.command()
@commands.has_role('exec')
async def reload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')
            bot.load_extension(f'cogs.{filename[:-3]}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(TOKEN)
