import discord, random
from discord.ext import commands


# presentations.py

class Present(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('presentations.py online')

    @commands.command()
    async def present(self, ctx, role: discord.Role):
        voice_channel = ctx.get_channel(697531358318166166)
        announcments = ctx.get_channel(697528162954903572)
        exec_role = ctx.get_role('exec')
        permissions = discord.Permissions(speak=False)
        pres_perms = discord.Permissions(speak=True)
        for all_roles in ctx.guild.roles:

            if not (all_roles == exec_role or all_roles == role):
                voice_channel.set_permissions(permissions)
            else:
                voice_channel.set_permissions(pres_perms)
        await announcments.send(f'@everyone, team {role.mention} is now presenting! Show some respect and join the '
                                f'#presentations voice channel! ;)')


def setup(bot):
    bot.add_cog(Present(bot))
