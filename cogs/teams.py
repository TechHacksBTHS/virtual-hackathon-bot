""" teams.py - Allows for the creation, removal, leaving, and purging of teams
"""

import random
import discord
from discord.ext import commands
from discord.utils import get


# TODO ability to change team name
# TODO ability to join teams by reacting to message

def unpack(lst):
    """ Joins a newline character after each element in list """
    return "\n".join(map(str, lst))


all_created_teams = []

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
    """ Handles functions listed in module doc string """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """ Sends ready message in stdout """
        print('teams.py is active')

    @commands.command(hidden=True)
    async def all_teams(self, ctx):
        """ Sends an embed msg to #join-team & lists team names and team
        members """
        await self.bot.wait_until_ready()
        # join-team channel where it shows all teams
        channel = self.bot.get_channel(698146745258999948)
        channel2 = self.bot.get_channel(779380419153363004)  # private-bot-cmd

        created_teams = []
        users_in_teams = []
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                created_teams.append(role)
                all_created_teams.append(role)
                users_in_teams.append(self.print_members(ctx, role))

        # inserts the team name after each teammember list spaced 2 elements
        # apart.
        iterator = 0
        for teamname in all_created_teams:
            users_in_teams.insert(iterator, '**'+teamname.name+'**')
            iterator += 2

        # flattens team[] by appending a comma after each teammember
        teams = []
        for team in users_in_teams:
            if isinstance(team, list):
                team = ',  '.join(map(str, team))
                teams.append(team)
            else:
                teams.append(team)

        await channel.purge(limit=100)
        if created_teams == []:
            teams.append('No teams yet, use !create <teamname> to create one!')
        embed = discord.Embed(title='All Teams, use !join to join one! ',
                              description=f'{unpack(teams)}',
                              color=random.choice(Colors))
        await channel2.send(embed=embed)

    def print_members(self, ctx, role: discord.Role):
        """ Returns a list of users in a role """
        self.bot.wait_until_ready()
        role = str(role)
        role = discord.utils.get(ctx.guild.roles, name=role)
        users = [user.display_name for user in ctx.guild.members if role in
                 user.roles]
        return users

    @commands.command(name='create')
    @commands.has_role('participant')
    async def create(self, ctx, *, role: commands.clean_content):
        """ Creates a team with name teamname """
        await self.bot.wait_until_ready()
        guild = ctx.guild
        participant = guild.get_role(697533967859187803)
        role = str(role)
        print(role)
        if ('@' in role) or ('#' in role) or ('http' in role) or ('.' in role):
            await ctx.send(
                f'That is an illegal name, names cannot include '
                f'\'.\',\'@\',\'#\' or \'http\'. Capishe '
                f'{ctx.author.mention}?')
            return
        elif get(guild.roles, name=role) in guild.roles:
            await ctx.send(f'Team {role} already exists, pick a new name or do'
                           f'!join to join them!')
        else:
            new_col = random.choice(Colors)
            role_str = role
            role = await guild.create_role(name=role, color=new_col,
                                           hoist=True)
            user = ctx.message.author
            await user.add_roles(role)
            await role.edit(position=3)
            await user.remove_roles(participant)
            perms = discord.PermissionOverwrite(read_messages=False,
                                                view_channel=False,
                                                send_messages=False,
                                                speak=False,
                                                stream=False,
                                                read_message_history=False,
                                                connect=False)

            team_perms = discord.PermissionOverwrite(read_messages=True,
                                                     view_channel=True,
                                                     send_messages=True,
                                                     speak=True, stream=True,
                                                     read_message_history=True,
                                                     connect=True)

            embed = discord.Embed(title=f'New Team {role} Created!',
                                  description='', color=new_col)
            await ctx.send(embed=embed)

            # ------------------------- team channels -------------------------
            guild = ctx.guild
            # get the Team Chat category
            team_cat = guild.get_channel(699729155301834762)
            # make a team text channel
            team_txt = await guild.create_text_channel(role_str,
                                                       category=team_cat,
                                                       permissions=perms)
            # make a team voice channel
            team_vc = await guild.create_voice_channel(role_str,
                                                       category=team_cat,
                                                       permissions=perms)
            # only give the team access to the tc
            await team_txt.set_permissions(role, overwrite=team_perms)
            # only give the team access to the vc
            await team_vc.set_permissions(role, overwrite=team_perms)

            # update join-teams:
            await self.all_teams(ctx)

    @commands.command()
    async def join(self, ctx, *, role: commands.clean_content):
        """ Join a team with name teamname """
        await self.bot.wait_until_ready()
        role = str(role)
        user = ctx.message.author
        guild = ctx.guild

        everyone_role = get(guild.roles, name='@everyone')
        participant_role = get(guild.roles, name='participant')
        all_roles = ctx.author.roles

        role = discord.utils.get(guild.roles, name=role)
        try:
            if participant_role in user.roles:
                if len(role.members) > 7:
                    await ctx.send(f'{role} already has 6 members')
                    return
                await user.add_roles(role)
                await user.remove_roles(participant_role)
                col = role.color
                e = discord.Embed(title=f'{ctx.author.name} has joined {role}',
                                  description='', color=col)
                await ctx.send(embed=e)
            else:
                if role in user.roles:
                    await ctx.send('You already have that role!')
                else:
                    await ctx.send('You are already in a team!')
        except discord.Forbidden:
            await ctx.send('Sorry boss, that\'s way above my pay grade')

    @commands.command()
    async def leave(self, ctx):
        """ Leaves your current teams """
        await self.bot.wait_until_ready()
        all_roles = ctx.author.roles
        guild = ctx.guild
        if 'participant' in all_roles:
            await ctx.send(f'Cannot leave participants {ctx.author.mention}')
        else:
            for i in all_roles:
                # filters out any role without change nickname permission AKA
                # the team roles
                if not i.permissions.change_nickname:
                    role = i
            user = ctx.message.author
            try:
                await user.remove_roles(role)
                participant = get(guild.roles, name='participant')
                await user.add_roles(participant)
                col = role.color
                e = discord.Embed(title=f'{ctx.author.name} has left {role}',
                                  description='', color=col)
                await ctx.send(embed=e)
            except discord.Forbidden:
                await ctx.send('Sorry boss, that\'s way above my pay grade')

    @commands.command()
    @commands.has_role('exec')
    async def remove(self, ctx, *, role: commands.clean_content):
        """ Deletes team role from discord """
        await self.bot.wait_until_ready()
        guild = ctx.guild
        # print(ctx.message.author)
        # TEAM TEXT CHANNEL
        team_txt = get(guild.text_channels, name=role)
        # TEAM VOICE CHANNEL
        team_voice = get(guild.voice_channels, name=role)
        role = get(guild.roles, name=role)
        participant_role = get(guild.roles, name='participant')
        if role:
            try:
                col = role.color
                msg = "The role {} has been deleted!".format(role.name)
                embed = discord.Embed(title=msg, description='', color=col)
                for i in role.members:
                    member = i
                    print(i)
                    await member.add_roles(participant_role)
                # cleanup
                await team_txt.delete(reason='!removed')
                await team_voice.delete(reason='!removed')
                await role.delete()
                await ctx.send(embed=embed)
                await self.all_teams(ctx)  # refresh the join-teams channel
            except discord.Forbidden:
                await ctx.send('Sorry boss, that\'s way above my pay grade')
        else:
            await ctx.send("The role doesn't exist!")

    @commands.command()
    @commands.has_role('exec')
    async def purge(self, ctx):
        """ Deletes all teams created """
        await self.bot.wait_until_ready()
        guild = ctx.guild
        # get the team chat category
        team_cat = guild.get_channel(699729155301834762)
        participant_role = get(guild.roles, name='participant')
        for role in guild.roles:
            if not role.permissions.change_nickname:
                for i in role.members:
                    await i.add_roles(participant_role)
                await role.delete(reason='purged')
        for channel in guild.text_channels:
            # remove every tc in team chat category
            if channel.category == team_cat:
                await channel.delete(reason='purged')
        for channel in guild.voice_channels:
            # remove every tc in team chat category
            if channel.category == team_cat:
                await channel.delete(reason='purged')
        await self.all_teams(ctx)
        await ctx.send('All teams removed')
        all_created_teams = []

    @commands.command(name='test', hidden=True)
    async def test(self, ctx):
        """ Test function """
        guild = ctx.guild


def setup(bot):
    """ Relays to bot.py to load this cog """
    bot.add_cog(Teams(bot))
