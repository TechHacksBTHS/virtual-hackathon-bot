# bot.py
import os

import discord,random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
from discord.ext import commands
bot = commands.Bot(command_prefix='!')

client = discord.Client()

@bot.command(name='create-team')
async def create_team(ctx):
    guild = ctx.guild
    await guild.create_role(name="role name")
    role = discord.utils.get(ctx.guild.roles, name="role name")
    user = ctx.message.author
    await user.add_roles(role)


@bot.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = random.choice(brooklyn_99_quotes)
    await ctx.channel.send(response)




bot.run(TOKEN)