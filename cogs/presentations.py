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
        await ctx.send(role)
        voice_channel = ctx.guild.get_channel(697543400596963328)
        # announcements text channel under IMPORTANT 697528162954903572
        announcments = ctx.guild.get_channel(779380419153363004)
        # techhacks_role = ctx.guild.get_role('TechHacks')
        exec_role = ctx.guild.get_role(697528456744796271)
        exec_perms = discord.Permissions.voice()
        # await voice_channel.set_permissions(techhacks_role, overwrite=exec_perms)
        permissions = discord.PermissionOverwrite(speak=False, stream=False)
        presentation_perms = discord.PermissionOverwrite(speak=True, stream=True)
        for all_roles in ctx.guild.roles:
            if role != all_roles and not all_roles.permissions.change_nickname :
                await voice_channel.set_permissions(all_roles, overwrite=permissions)
            else:
                await voice_channel.set_permissions(all_roles, overwrite=presentation_perms)
        await announcments.send(f'Everyone, team {role.mention} is now presenting! Show '
                                f'some respect and join the '
                                f'#exec voice channel! ;)')
        # TODO: change #exec to #presentation
        await voice_channel.set_permissions(exec_role, overwrite=exec_perms)
        # await voice_channel.set_permissions(techhacks_role, overwrite=exec_perms)

    @commands.command()
    @commands.has_role('exec')
    async def hush(self, ctx):

        permissions = discord.PermissionOverwrite(speak=False, stream=False)
        techhacks_role = ctx.guild.get_role('TechHacks')
        exec_perms = discord.Permissions.voice()

        exec_role = ctx.guild.get_role('exec')
        # Presentations voice channel under VOICE CHANNELS 697531358318166166
        voice_channel = ctx.guild.get_channel(697531358318166166)
        # await voice_channel.set_permissions(techhacks_role, overwrite=exec_perms)
        await ctx.send(voice_channel.voice_states.keys())
        """
        for all_roles in ctx.guild.roles:
            if not all_roles.permissions.change_nickname: # or all_roles == techhacks_role):
                await ctx.send(all_roles)
                await voice_channel.set_permissions(all_roles, overwrite=permissions)

        await voice_channel.set_permissions(exec_role, overwrite=exec_perms)
        await ctx.send('All presenters have been muted')
        """

def setup(bot):
    bot.add_cog(Present(bot))
