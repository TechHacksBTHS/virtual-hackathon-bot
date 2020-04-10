import discord, random
from discord.ext import commands


class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create')
    async def create_team(self, ctx, role):
        guild = ctx.guild
        await guild.create_role(name=role)
        role = discord.utils.get(ctx.guild.roles, name=role)
        user = ctx.message.author
        try:
            await user.add_roles(role)
        except discord.errors.Forbidden:
            ctx.channel.send(
                'Sorry, I can\'t let you do that. The execs are a far greater power than I, and I worship them as '
                'gods')

    @commands.command(name='join')
    async def create_team(self, ctx, role):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role)
        user = ctx.message.author
        try:
            await user.add_roles(role)
        except discord.ext.commands.errors:
            ctx.channel.send(
                'Sorry, I can\'t let you do that. The execs are a far greater power than I, and I worship them as '
                'gods')


def setup(bot):
    bot.add_cog(Teams(bot))
