# teams.py
import discord, random, time
from discord.ext import commands


# todo display all users in a team

# todo join teams by reacting to message

# todo limit role creation to one role

def unpack(s):
    return "\n".join(map(str, s))



Colors = [discord.Color.default(),
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
    async def all_teams(self, ctx):
        channel = self.bot.get_channel(698146745258999948)
        created_teams = []
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                created_teams.append(role)

        await channel.purge(limit=100)
        if created_teams == []:
            created_teams.append('No teams yet, use !create <teamname> to create one!')
        embed = discord.Embed(title='All Teams, use !join to join one! ', description=f'{unpack(created_teams.reverse())}',
                              color=random.choice(Colors))
        await channel.send(embed=embed)

    @commands.command()
    async def create(self, ctx, *, role):
        created_teams = []
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                created_teams.append(role)

        if any(i in created_teams for i in ctx.author.roles) or created_teams == []:
            guild = ctx.guild
            new_col = random.choice(Colors)
            if ('@' or 'participant' or 'TechHacks' or 'everyone' or '#' or 'http' or '.') in role or (
                    role in created_teams):
                await ctx.send(f'frick off {ctx.author.mention}')
            else:
                await guild.create_role(name=role, color=new_col)
                time.sleep(3)
                role = discord.utils.get(ctx.guild.roles, name=role)
                user = ctx.message.author
                await user.add_roles(role)
                embed = discord.Embed(title=f'New Team {role} Created!', description='', color=new_col)
                await ctx.send(embed=embed)

                await self.all_teams(ctx)
                print(created_teams)

        else:
            await ctx.send('You are already on a team!')
            print(created_teams)

    @commands.command()
    async def join(self, ctx, *, role):
        created_teams = []
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                created_teams.append(role)

        if any(i in created_teams for i in ctx.author.roles) or created_teams == []:
            guild = ctx.guild
            role = discord.utils.get(guild.roles, name=role)
            user = ctx.message.author
            try:
                if role not in user.roles:
                    await user.add_roles(role)
                    col = role.color
                    embed = discord.Embed(title=f'{ctx.author} has joined {role}', description='', color=col)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('You already have that role!')
            except discord.Forbidden:
                await ctx.send('Sorry boss, that\'s way above my pay grade')
        else:
            await ctx.send('You are already on a team!')

    @commands.command()
    async def leave(self, ctx, *, role):
        guild = ctx.guild
        if role == 'participant':
            await ctx.send(f'frick off {ctx.author.mention}')

        else:
            role = discord.utils.get(guild.roles, name=role)
            user = ctx.message.author
            try:
                await user.remove_roles(role)
                await ctx.send(f'{ctx.author.mention} has left {role}')
            except discord.Forbidden:
                await ctx.send('Sorry boss, that\'s way above my pay grade')

    @commands.command()
    @commands.has_role('exec')
    async def remove(self, ctx, *, role):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role)
        if role:
            try:
                col = role.color
                embed = discord.Embed(title="The role {} has been deleted!".format(role.name), description='',
                                      color=col)

                await role.delete()
                await ctx.send(embed=embed)
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
        await ctx.send('All teams removed')
        all_created_teams = []


def setup(bot):
    bot.add_cog(Teams(bot))
