# bot.py
import os, json, base64
from firebase import firebase

import discord, random
from dotenv import load_dotenv
from discord import Member

load_dotenv()
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description='owo i sure do L-O-V-E programming')
TOKEN = os.environ.get('TOKEN')
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)
firebase = firebase.FirebaseApplication(FIREBASE, None)

bot.remove_command('help')


@bot.event
async def on_ready():
    bot_channel = bot.get_channel(697537529737510932)
    sunglasses = bot.get_emoji(698234865576968203)
    await bot.change_presence(
        # "you all code"
        activity=discord.Activity(type=discord.ActivityType.watching, name="myself break over & over",
                                  emoji=sunglasses))
    await bot_channel.send('im awake senpai and ready to serve uwu')
    print('bot.py is active')


@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='TechHacks',
                          color=discord.Color.blue())
    embed.add_field(name='Who are we?', value='As representatives of the nation\'s largest and most prestigious STEM '
                                              'high school, TechHacks aims to expand student tech engagement in New '
                                              'York City through yearly hackathons, workshops, and similar events.\n',
                    inline=False)
    embed.add_field(name='What is a hackathon?', value='A hackathon is a programming competition where teams of two to '
                                                       'five students come together to solve a problem or build \n'
                                                       'software related to a theme', inline=False)
    embed.add_field(name='Commands', value='help - this command \n'
                                           'create - creates a team (only make one 😉)  \n '
                                           'join - joins a team \n'
                                           'leave - leaves a team \n', inline=False)
    await ctx.channel.send(embed=embed)


@bot.command(name='ping')
async def ping(ctx):
    data = {
        "USER": 'pong',
        'TEAM': 'ping'}
    result = firebase.post(FIREBASE_NAME + '/Team', data)
    print(result)
    await ctx.send('pong')


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='participant')
    await member.add_roles(role)


@bot.command(hidden=True)
@commands.has_role('exec')
async def load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command(hidden=True)
@commands.has_role('exec')
async def unload(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')


@bot.command(hidden=True)
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
