# presentations.py
import discord, random
from discord.ext import commands


class Present(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('presentations.py online')

    @commands.command()
    @commands.has_role('exec')
    async def present(self, ctx, *, role: discord.Role):
        # Presentations voice channel under VOICE CHANNELS 697531358318166166
        voice_channel = ctx.guild.get_channel(697531358318166166)
        # announcements text channel under IMPORTANT 697528162954903572
        announcments = ctx.guild.get_channel(779367976876507147)
        exec_role = ctx.guild.get_role(697528456744796271)
        vc_members = voice_channel.members 
        for i in vc_members: # go through everyone in vc and mute them UNLESS they are presenting
            if (exec_role not in i.roles) and (role not in i.roles):
                await i.edit(mute=True)
            else: 
                await i.edit(mute=False)
        await announcments.send(f'Everyone, team {role.mention} is now presenting! Show '
                                f'some respect and join the '
                                f'Presentations voice channel! ;)')
        

    @commands.command()
    @commands.has_role('exec')
    async def hush(self, ctx):
        exec_role = ctx.guild.get_role(697528456744796271)
        # Presentations voice channel under VOICE CHANNELS 697531358318166166
        voice_channel = ctx.guild.get_channel(697531358318166166)
        vc_members = voice_channel.members  
        for i in vc_members: # go through everybody in the vc and mute them
            if exec_role not in i.roles:
                await i.edit(mute=True)
        await ctx.send("Everyone is muted")


def setup(bot):
    bot.add_cog(Present(bot))
