""" bot.py - handles user interface and loads cogs """
# This project was designed by Daniel Kogan, who can be reached at
# daniel@techhacks.nyc, or daniel.kogan@stonybrook.edu

import os
from firebase import firebase

import discord, random
from dotenv import load_dotenv

load_dotenv()
from discord.ext import commands
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', description='owo i sure do L-O-V-E programming', intents=intents)
TOKEN = os.environ.get('TOKEN')
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)
firebase = firebase.FirebaseApplication(FIREBASE, None)

bot.remove_command('help')


@bot.event
async def on_ready():
    bot_channel = bot.get_channel(779380419153363004)
    sunglasses = bot.get_emoji(698234865576968203)
    await bot.change_presence(
        # "you all code"
        # "myself break over & over"
        activity=discord.Activity(type=discord.ActivityType.watching, name="you all code",
                                  emoji=sunglasses))
    await bot_channel.send('im awake senpai and ready to serve uwu')
    # await bot_channel.send('Ah yes, I have been professionally reloaded, thank you fine gentlemen')
    print('bot.py is active')
    print('bruh')

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
                          'four students come together to solve a problem or build \n'
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

    embed.add_field(name='```Do I need to be active for the full 48+ hours?```',
                    value='```Nope! You can work for as much or as little as you want '
                          'throughout the day. Don\'t '
                          'forget to eat, sleep, etc etc!```')

    embed.add_field(name='```What is the theme?```',
                    value='```The themes for this Hackathon are COVID-19 Pandemic, '
                          'racial injustice, misinformation, and climate change. You can also create non-theme projects that will not be eligible for theme prizes. '
                          'Check out the #slides for more information, or feel free to ping @exec. '
                          'In addition, we do have a rubric category judging '
                          'relevance, so be sure to explain why your project is important! '
                          '\n\n```', inline=False)
    embed.add_field(name='```Is there a prize?```',value='```You betcha! The theme prize first place will receive a $100 '
                                                         'gift card while second and third place will receive $60 to $40 dollars gift card respectively. '
                                                         'There are other prizes available as well!```', inline=False)
    embed.add_field(name='```How will I submit my project?```',value='```We will open submissions with a platform called '
                                                               'Devpost right before the hackathon ends```',inline=False)
    embed.add_field(name='```How will judging work?```',value='```You\'ll have to present on our Discord server. There will be '
                                                        'a 5 minute time restriction on presentations, and our rubric '
                                                        'is available at: '
                                                        'https://docs.google.com/presentation/d/1ptT7K'
                                                        '-pjaS53YSj_GtGqF85uk5RrsbR-UywSpjb2bIM/edit?usp=sharing  ```')
    embed.add_field(name='```I don’t have a team! Help!```',value='```Make sure to ask around on #team-formation! A team '
                                                            'should be around 3 to 4 students (max of 6) so someone might have '
                                                            'an empty space! Also, reach out to an organizer on the '
                                                            'Discord server.```',inline=False)
    embed.add_field(name='```Commands```', value='```css\nhelp - this command \n'
                                                 'create - creates a team (only make one 😉) \n'
                                                 'join - joins a team \n'
                                                 'leave - leaves a team \n```', inline=False)
    await ctx.channel.send(embed=embed)


@bot.command(name='ping')
async def ping(ctx):
    data = { "USER": 'heroku',
        'TEAM': 'online'}
    result = firebase.post(FIREBASE_NAME + '/Team', data)
    print(result)
    await ctx.send('pong')


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=697533967859187803)
    await member.add_roles(role)


@bot.event
async def on_raw_reaction_add(payload):
    # NOTE: We have to use the raw function because on the regular reaction, it
    #       only does it for cached messages, which is not ideal
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(payload.guild_id)
    message_id = 779426797044891688
    ping_message_id = 829908952430673930
    Technight2020 = guild.get_role(779364367145500702)
    announcement_role = guild.get_role(829907918383874078)
    user = guild.get_member(payload.user_id)
    if (payload.message_id == message_id) and (payload.emoji.name == "✋"):
        await user.add_roles(Technight2020)
    if (payload.message_id == ping_message_id) and (payload.emoji.name=="💃"):
        await user.add_roles(announcement_role)


@bot.event
async def on_raw_reaction_remove(payload):
    # NOTE: We have to use the raw function because on the regular reaction, it
    #       only does it for cached messages, which is not ideal
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(payload.guild_id)
    message_id = 779426797044891688
    Technight2020 = guild.get_role(779364367145500702)
    ping_message_id = 829908952430673930
    announcement_role = guild.get_role(829907918383874078)
    user = guild.get_member(payload.user_id)
    if (payload.message_id == message_id) and (payload.emoji.name == "✋"):
        await user.remove_roles(Technight2020)
    if (payload.message_id == ping_message_id) and (payload.emoji.name=="💃"):
        await user.remove_roles(announcement_role)


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
    await ctx.send('I have been professionally reloaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'): # and not filename.startswith('teams'):  #add second half of 'and' in order to lock the teams file
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
