import discord, random,time
from discord.ext import commands

#join teams by reacting to message
#limit role creation to one role

def unpack(s):
    return "\n".join(map(str, s))

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
                 discord.Color.dark_red()
           ]

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('teams.py is active')


    @commands.command(hidden=True)
    async def all_teams(self,ctx):
        channel = self.bot.get_channel(698146745258999948)
        created_teams = []
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                created_teams.append(role)

        await channel.purge(limit=100)
        if created_teams == []:
            created_teams.append('No teams yet, use !create <teamname> to create one!')
        embed = discord.Embed(title='All Teams, use !join to join one! ', description=f'{unpack(created_teams)}', color=random.choice(Colors))
        await channel.send(embed=embed)


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

        await self.all_teams(ctx)


    @commands.command()
    async def join(self, ctx, *, role):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role)
        user = ctx.message.author
        try:
            await user.add_roles(role)
            await ctx.send(f'{ctx.author.mention} has joined {role}')
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
                await self.all_teams(ctx)
            except discord.Forbidden:
                await ctx.send('Sorry boss, that\'s way above my pay grade')
        else:
            await ctx.send("The role doesn't exist!")


    @commands.command()
    @commands.has_role('exec')
    async def purge(self, ctx):
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                await role.delete()
        await self.all_teams(ctx)





def setup(bot):
    bot.add_cog(Teams(bot))
