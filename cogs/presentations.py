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
    @commands.has_role('exec')
    async def present(self, ctx, role: discord.Role):
        voice_channel = ctx.guild.get_channel(697531358318166166)
        announcments = ctx.guild.get_channel(697528162954903572)
        exec_role = ctx.guild.get_role('exec')
        permissions = discord.PermissionOverwrite(speak=False,stream=False)
        pres_perms = discord.PermissionOverwrite(speak=True,stream=True)
        for all_roles in ctx.guild.roles:

            if not (all_roles == exec_role or all_roles == role):
                await self.bot.edit_channel_permissions(voice_channel.set_permissions, all_roles,permissions)
            else:
                await self.bot.edit_channel_permissions(voice_channel.set_permissions, all_roles,pres_perms)
        await announcments.send(f'@everyone, team {role.mention} is now presenting! Show some respect and join the '
                                f'#presentations voice channel! ;)')


def setup(bot):
    bot.add_cog(Present(bot))
