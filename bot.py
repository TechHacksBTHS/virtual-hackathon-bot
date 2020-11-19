# bot.py
# this project was designed by Daniel Kogan, who can be reached at daniel@techhacks.nyc, or dkogan7191@bths.edu

import os
from firebase import firebase

import discord, random
from dotenv import load_dotenv

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
        # "myself break over & over"
        activity=discord.Activity(type=discord.ActivityType.watching, name="you all code",
                                  emoji=sunglasses))
    # 'im awake senpai and ready to serve uwu'
    # await bot_channel.send('Ah yes, I have been professionally reloaded, thank you fine gentlemen')
    print('bot.py is active')


@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='TechHacks',
                          color=discord.Color.blue())
    embed.add_field(name='```Who are we?```',
                    value='```As representatives of the nation\'s largest and most prestigious STEM '
                          'high school, TechHacks aims to expand student tech engagement in New '
                          'York City through yearly hackathons, workshops, and similar events.\n\n```',
                    inline=False)

    embed.add_field(name='```What is a hackathon?```',
                    value='```A hackathon is a programming competition where teams of one to '
                          'four students come together to solve a problem or build \n\n'
                          'software related to a theme```', inline=False)

    embed.add_field(name='```What if I don\'t know how to code?```',
                    value='```That\'s perfectly fine! Beginners are totally '
                          'welcome to all TechHacks events, and mentors '
                          'will be available throughout all of our '
                          'hackathons to ask for help. Innovation and ideas '
                          'are the most important part of a project, '
                          'and not even pros finish their prototypes '
                          'sometimes. My recommendation is for you guys to '
                          'look up P5js, and try to build something on '
                          'that \n\n```', inline=False)

    embed.add_field(name='```Do I need to be active for the full 24 hours?```',
                    value='```Nope! You can work for as much or as little as you want '
                          'throughout the day. Don\'t '
                          'forget to eat, sleep, etc etc!```')

    embed.add_field(name='```What is the theme?```',
                    value='```We try to stay away from themes in order to let everyone build '
                          'what they want. However, we do have a rubric category judging '
                          'relevance, so be sure to explain why your project is important! '
                          '\n\n```', inline=False)
    embed.add_field(name='```Is there a prize?```',value='```You betcha! The grand prize winner will receive a 25$ '
                                                         'Amazon gift card while third and second place will receive '
                                                         'a TechHacks certificate```', inline=False)
    embed.add_field(name='```How will I submit my project?```',value='```We will open submissions with a platform called '
                                                               'Devpost right before the hackathon ends```',inline=False)
    embed.add_field(name='```How will judging work?```',value='```You\'ll have to present on our Discord server. There will be '
                                                        'a 5 minute time restriction on presentations, and our rubric '
                                                        'is avilable at: '
                                                        'https://docs.google.com/presentation/d/1ptT7K'
                                                        '-pjaS53YSj_GtGqF85uk5RrsbR-UywSpjb2bIM/edit?usp=sharing  ```')
    embed.add_field(name='```I don’t have a team! Help!```',value='```Make sure to ask around on #team-formation! A team '
                                                            'should be around 3 to 4 students so someone might have '
                                                            'an empty space! Also, reach out to an organizer on the '
                                                            'Discord server.```',inline=False)
    embed.add_field(name='```Commands```', value='```css\nhelp - this command \n'
                                                 'create - creates a team (only make one 😉) \n'
                                                 'join - joins a team \n'
                                                 'leave - leaves a team \n```', inline=False)
    await ctx.channel.send(embed=embed)


@bot.command(name='ping')
async def ping(ctx):
    data = {
        "USER": 'heroku',
        'TEAM': 'online'}
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
    if filename.endswith('.py'): # and not filename.startswith('teams'):  #remove second half of and in order to load the teams file
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
