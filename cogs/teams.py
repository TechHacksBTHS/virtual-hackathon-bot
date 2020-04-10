import discord, random
from discord.ext import commands

#join teams by reacting to message
#limit role creation to one role

Colors = [ discord.Color.default(),
                 discord.Color.teal(),
                 discord.Color.dark_teal(),
                 discord.Color.green(),
                 discord.Color.dark_green(),
                 discord.Color.blue(),
                 discord.Color.purple(),
                 discord.Color.dark_purple(),
                 discord.Color.magenta(),
                 discord.Color.dark_magenta(),
                 discord.Color.gold(),
                 discord.Color.dark_gold(),
                 discord.Color.orange(),
                 discord.Color.dark_orange(),
                 discord.Color.red(),
                 discord.Color.dark_red()]

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('teams.py is active')

    @commands.command()
    async def create(self, ctx, *, role):
        guild = ctx.guild
        new_col = random.choice(Colors)
        await guild.create_role(name=role, color=new_col)
        role = discord.utils.get(ctx.guild.roles, name=role)
        user = ctx.message.author
        await user.add_roles(role)

        embed = discord.Embed(title=f'New Team {role} Created!', description='', color=new_col)
        await ctx.send(embed=embed)

    @commands.command()
    async def join(self, ctx, *, role):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role)
        user = ctx.message.author
        try:
            await user.add_roles(role)
        except discord.Forbidden:
            await ctx.send('Sorry boss, that\'s way above my pay grade')

    @commands.command()
    @commands.has_role('exec')
    async def remove(self, ctx, *, role):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role)
        if role:
            try:
                await role.delete()
                await ctx.send("The role {} has been deleted!".format(role.name))
            except discord.Forbidden:
                await ctx.send('Sorry boss, that\'s way above my pay grade')
        else:
            await ctx.send("The role doesn't exist!")


def setup(bot):
    bot.add_cog(Teams(bot))
