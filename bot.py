# bot.py
import os
from boto.s3.connection import S3Connection

import discord, random
from dotenv import load_dotenv
from discord import Member

load_dotenv()
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

bot = commands.Bot(command_prefix='!', description='owo i sure do L-O-V-E programming')
TOKEN = S3Connection(os.environ['TOKEN'], os.environ['TOKEN'])

client = discord.Client()


@bot.command(name='create-team')
async def create_team(ctx, role):
    guild = ctx.guild
    await guild.create_role(name=role)
    role = discord.utils.get(ctx.guild.roles, name=role)
    user = ctx.message.author
    try:
        await user.add_roles(role)
    except discord.errors.Forbidden:
        ctx.message('Sorry, I can\'t let you do that. The execs are a far greater power than I, and I worship them as '
                    'gods')


@bot.command(name='join-team')
async def create_team(ctx, role):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role)
    user = ctx.message.author
    await user.add_roles(role)


@bot.command(name='kick', pass_context=True,)
@has_permissions(ban_members=True)
async def _kick(ctx, member: Member):
    await ctx.kick(member)
    await ctx.channel.send('{} has been kicked'.format(ctx.member))


@_kick.error
async def kick_error(error, ctx):
    if isinstance(error, MissingPermissions):
        text = "I can\'t let you do that {}".format(ctx.message.author)
        await ctx.send(ctx.message.channel, text)


@bot.command(name='ban', pass_context=True)
@has_permissions(ban_members=True)
async def _ban(ctx, member: Member):
    await ctx.ban(member)


@_ban.error
async def kick_error(error, ctx):
    if isinstance(error, MissingPermissions):
        text = "I can\'t let you do that {}".format(ctx.message.author)
        await ctx.channel.send(text)


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
