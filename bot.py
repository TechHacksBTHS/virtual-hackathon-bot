# bot.py
import os

import discord, random
from dotenv import load_dotenv
from discord import Member

load_dotenv()
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description='owo i sure do L-O-V-E programming')
TOKEN = os.environ.get('TOKEN', 3)

emojis = [bot.get_emoji(698234865576968203),
          bot.get_emoji(698239641576538205),
          bot.get_emoji(698239594981883915),
          bot.get_emoji(698239653740019833),
          bot.get_emoji(698239633040867450),
          bot.get_emoji(698239728662610030),
          bot.get_emoji(698239846560432168),
          bot.get_emoji(698239889686265996),
          bot.get_emoji(698239918346076254),
          bot.get_emoji(698239904978567238),
          bot.get_emoji(698239856899260478),
          bot.get_emoji(698239933223272518),
          bot.get_emoji(698240057911541820),
          bot.get_emoji(698240081936384132),
          bot.get_emoji(698240106150232145),
          bot.get_emoji(698240243081674894),
          bot.get_emoji(698240480525287516),
          bot.get_emoji(698240518404046878),
          bot.get_emoji(698240558757314561),
          bot.get_emoji(698240564423819274),
          bot.get_emoji(698240629511290920),
          bot.get_emoji(698240668069396560),
          bot.get_emoji(698240748520472636),
          bot.get_emoji(698240771186229329),
          bot.get_emoji(698240782813102141),
          bot.get_emoji(698240851142246453),
          bot.get_emoji(698240893358178377),
          bot.get_emoji(698240933334089888),
          bot.get_emoji(698240943794552874),
          bot.get_emoji(698240925238951938),
          bot.get_emoji(698241018700496906),
          bot.get_emoji(698241067639898124),
          bot.get_emoji(698241140167802990),
          bot.get_emoji(698241177584926880),
          bot.get_emoji(698241249781612644),
          bot.get_emoji(698241268244938935),
          bot.get_emoji(698241294765523045),
          bot.get_emoji(698241328890380372),
          bot.get_emoji(698241362964905994),
          bot.get_emoji(698241510960791633),
          bot.get_emoji(698241587708297236),
          bot.get_emoji(698241622353379388),
          bot.get_emoji(698241723205419089),
          bot.get_emoji(698241768545583154),
          bot.get_emoji(698241818025918505),
          bot.get_emoji(698241832575959120),
          bot.get_emoji(698241931481841746),
          bot.get_emoji(698242034187632722),
          bot.get_emoji(698242059781406720),
          bot.get_emoji(698242077435232346),
          bot.get_emoji(698242130761613415),
          bot.get_emoji(698242251805032488),
          bot.get_emoji(698242255307276329),
          bot.get_emoji(698242244230250497),
          bot.get_emoji(698242345711435786),
          bot.get_emoji(698242392867864646),
          bot.get_emoji(698242396940533872),
          bot.get_emoji(698242431358861343),
          bot.get_emoji(698242540658360330),
          bot.get_emoji(698242585579225139),
          bot.get_emoji(698242668362465373),
          bot.get_emoji(698242668362465373),
          bot.get_emoji(698242676990017536),
          bot.get_emoji(698242828727222273),
          bot.get_emoji(698242934000320532),
          bot.get_emoji(698243015592116224),
          bot.get_emoji(698243006674894969),
          bot.get_emoji(698243140670455899),
          bot.get_emoji(698243197033382028),
          bot.get_emoji(698243257058197586),
          bot.get_emoji(698243384476958772),
          ]


@bot.event
async def on_ready():
    bot_channel = bot.get_channel(697537529737510932)
    sunglasses = bot.get_emoji(698234865576968203)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you all code", emoji=sunglasses))
    await bot_channel.send('im awake senpai and ready to serve uwu')
    print('bot.py is active')

@bot.event
async def on_message(message):
    if random.randint(0, 100)>98:
        await message.add_reaction(random.choice(emojis))




@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='participant')
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
