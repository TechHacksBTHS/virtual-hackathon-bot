""" exec.py - Allows execs to clear messages, kick users, ban users and unban
              users """
import discord, time, random
from discord.ext import commands
from discord import Member


class Exec(commands.Cog):
    """ Handles functions listed in module doc string """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """ reports status of script to terminal """
        print('exec.py is active')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5, current_channel=''):
        """ Clears messages """
        await self.bot.wait_until_ready()
        if current_channel == '':
            current_channel = ctx.channel
        else:
            current_channel = self.bot.get_channel(current_channel)

        await current_channel.purge(limit=amount)
        await current_channel.send(f'Cleared by {ctx.author.mention}')

    @commands.command()
    @commands.has_role('exec')
    async def kick(self, ctx, member: Member, *, reason=None):
        """ Kicks a user """
        await self.bot.wait_until_ready()
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for: {reason}')

    @commands.command()
    @commands.has_role('exec')
    async def ban(self, ctx, member: Member, *, reason=None):
        """ Bans a user """
        await self.bot.wait_until_ready()
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for: {reason}')

    @commands.command()
    @commands.has_role('exec')
    async def unban(self, ctx, *, member):
        """ Unbans a user """
        await self.bot.wait_until_ready()
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name,
                                                   member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """ Handles error messages """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument')
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'The execs are a far greater power than I, '
                           f'{ctx.message.author}, and I am afraid'
                           f' they will not allow me to do that')
            return
        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("😳")
            await ctx.send('404 Command Not Found')
        elif isinstance(error, commands.MissingRole):
            await ctx.send('You already have a team silly!')
        else:
            await ctx.send(f'{error} error occured')


def setup(bot):
    """ Relays to bot.py to load this cog """
    bot.add_cog(Exec(bot))
