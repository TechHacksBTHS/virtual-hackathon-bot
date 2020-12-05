""" presentation.py - allows the ability for teams to present, for execs
                      silence everyone, and for execs to unmute everyone
"""

import discord, random
from discord.ext import commands


class Present(commands.Cog):
    """ Contains the functions outlined in module doc string """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """ Report status of script to terminal """
        print('presentations.py online')

    @commands.command()
    @commands.has_role('exec')
    async def present(self, ctx, *, role: discord.Role):
        """ Allows execs to unmute a given team in voice channel """
        # Presentations voice channel under VOICE CHANNELS
        voice_channel = ctx.guild.get_channel(697531358318166166)
        # announcements text channel under TECHNIGHT
        announcments = ctx.guild.get_channel(779367976876507147)
        exec_role = ctx.guild.get_role(697528456744796271)
        vc_members = voice_channel.members

        # FIXME: This is unbearably slow. It takes a solid minute to get the
        #        team unmuted and the public announcement sent. I suspect it is
        #        because these loops are iterating over ALL of the members in
        #        the voice channel EVERY time it is called. This can be fixed
        #        by only iterating over members who are not muted and muting
        #        them.

        # Goes through everyone in vc and mute them UNLESS they are presenting
        for i in vc_members:
            if (exec_role not in i.roles) and (role not in i.roles):
                await i.edit(mute=True)
            else:
                await i.edit(mute=False)
        await announcments.send(f'Everyone, team {role.mention} is now '
                                f'presenting! Show '
                                f'some respect and join the '
                                f'Presentations voice channel! ;)')

    @commands.command()
    @commands.has_role('exec')
    async def hush(self, ctx):
        """ Allows execs to mute everyone in voice channel """
        exec_role = ctx.guild.get_role(697528456744796271)
        # Presentations voice channel under VOICE CHANNELS
        voice_channel = ctx.guild.get_channel(697531358318166166)
        vc_members = voice_channel.members
        # go through everybody in the vc and mute them
        for i in vc_members:
            if exec_role not in i.roles:
                await i.edit(mute=True)
        await ctx.send("Everyone is muted")

    @commands.command()
    @commands.has_role('exec')
    async def speak(self, ctx):
        """ Allows execs to unmute everyone in voice channel """

        # NOTE: This is susceptible to server raiders so avoid using this.
        #       DO NOT USE THIS BECAUSE OF RAIDERS !!!!!!!!!!!

        exec_role = ctx.guild.get_role(697528456744796271)
        # Presentations voice channel under VOICE CHANNELS
        voice_channel = ctx.guild.get_channel(697531358318166166)
        vc_members = voice_channel.members
        # go through everybody in the vc and unmute them
        for i in vc_members:
            if exec_role not in i.roles:
                await i.edit(mute=False)
        await ctx.send("Everyone is unmuted")


def setup(bot):
    """ Relays to bot.py to load this cog """
    bot.add_cog(Present(bot))
