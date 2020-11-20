# teams.py
import discord, random, time
from discord.ext import commands
from discord.utils import get


# TODO display all users in a team
# TODO change team name
# TODO join teams by reacting to message

# STUFF THAT NEEDS TO BE DONE OVER THE WEEKEND
# TODO Create team channels on team create
# TODO stop the bugs with creating a team
# TODO filter out non-hackathon participants
# TODO presentation feature needs wayyyy more testing

def unpack(s):
    return "\n".join(map(str, s))


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
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('teams.py is active')

    @commands.command(hidden=True)
    async def all_teams(self, ctx):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(698146745258999948)
        created_teams = []
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                created_teams.append(role)
                all_created_teams.append(role)

        await channel.purge(limit=100)
        if created_teams == []:
            created_teams.append('No teams yet, use !create <teamname> to create one!')
        embed = discord.Embed(title='All Teams, use !join to join one! ', description=f'{unpack(created_teams)}',
                              color=random.choice(Colors))
        await channel.send(embed=embed)

    @commands.command(name='create')
    @commands.has_role('participant')
    async def create(self, ctx, *, role: commands.clean_content):
        await self.bot.wait_until_ready()
        role = str(role)
        print(role)
        guild = ctx.guild
        if ('@' in role) or ('#' in role) or ('http' in role) or ('.' in role):
            await ctx.send(
                f'That is an illegal name, names cannot include \'.\', \'@\',\'#\' or \'http\'. Capishe {ctx.author.mention}?')
            return
        elif (get(ctx.guild.roles, name=role)) in ctx.guild.roles:
            await ctx.send(f'Team {role} already exists, pick a new name or do !join to join them!')
        else:
            new_col = random.choice(Colors)
            perms = discord.Permissions(send_messages=True, add_reactions=True)
            await guild.create_role(name=role, color=new_col, hoist=True)
            role_str = role
            role = discord.utils.get(ctx.guild.roles, name=role)
            user = ctx.message.author
            await user.add_roles(role)
            particpant = discord.utils.get(ctx.guild.roles, name='participant')
            await role.edit(position=2)
            await user.remove_roles(particpant)
            permissions = discord.PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False,
                                                      speak=False, stream=False)
            team_perms = discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True,
                                                     speak=True, stream=True)
            embed = discord.Embed(title=f'New Team {role} Created!', description='', color=new_col)
            await ctx.send(embed=embed)

            # Text/Voice Channel for Teams
            #await guild.create_text_channel(name=role_str, category='Team Chats', permissions=permissions)
            #await guild.create_voice_channel(name=role_str, category='Team Chats', permissions=permissions)
            #team_txt = discord.utils.get(guild.text_channels, name=role_str)
            #team_voice = discord.utils.get(guild.voice_channels, name=role_str)
            #team_txt.set_permissions(role, team_perms)
            #team_voice.set_permissions(role, team_perms)

            # update join-teams:
            await self.all_teams(ctx)

    @commands.command()
    async def join(self, ctx, *, role: commands.clean_content):
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
                if len(role.members) > 5:
                    await ctx.send(f'{role} already has 4 members')
                    return
                await user.add_roles(role)
                await user.remove_roles(participant_role)
                col = role.color
                embed = discord.Embed(title=f'{ctx.author.name} has joined {role}', description='', color=col)
                await ctx.send(embed=embed)
            else:
                if role in user.roles:
                    await ctx.send('You already have that role!')
                else:
                    await ctx.send('You are already in a team!')
        except discord.Forbidden:
            await ctx.send('Sorry boss, that\'s way above my pay grade')

    @commands.command()
    async def leave(self, ctx):
        await self.bot.wait_until_ready()
        guild = ctx.guild
        exec_role = get(guild.roles, name='exec')
        everyone_role = get(guild.roles, name='@everyone')
        participant_role = get(guild.roles, name='participant')
        all_roles = ctx.author.roles
        if 'participant' in all_roles:
            await ctx.send(f'Cannot leave particpants {ctx.author.mention}')

        else:
            if (exec_role) in all_roles:
                all_roles.remove(exec_role)
            if participant_role in all_roles:
                all_roles.remove(participant_role)

            all_roles.remove(everyone_role)
            
            for i in all_roles:
                if not i.permissions.change_nickname:
                    role = i #instead of removing first role, remove the filters and just remove any role without a change_nickname permission
            
            user = ctx.message.author
            try:
                await user.remove_roles(role)

                particpant = discord.utils.get(ctx.guild.roles, name='participant')
                await user.add_roles(particpant)
                col = role.color
                embed = discord.Embed(title=f'{ctx.author.name} has left {role}', description='', color=col)
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await ctx.send('Sorry boss, that\'s way above my pay grade')

    @commands.command()
    @commands.has_role('exec')
    async def remove(self, ctx, *, role: commands.clean_content):
        await self.bot.wait_until_ready()
        guild = ctx.guild
        print(ctx.message.author)
        #team_txt = discord.utils.get(guild.text_channels, name=role)  # TEAM TEXT CHANNEL
        #team_voice = discord.utils.get(guild.voice_channels, name=role)  # TEAM VOICE CHANNEL
        role = discord.utils.get(guild.roles, name=role)
        participant_role = get(guild.roles, name='participant')
        if role:
            try:
                col = role.color
                embed = discord.Embed(title="The role {} has been deleted!".format(role.name), description='',
                                      color=col)
                for i in role.members:
                    member = i
                    print(i)
                    await member.add_roles(participant_role)

                #await team_txt.delete(reason='!removed')
                #await team_voice.delete(reason='!removed')
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
        await self.bot.wait_until_ready()
        guild = ctx.guild
        participant_role = get(guild.roles, name='participant')
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                for i in role.members:
                    await i.add_roles(participant_role)
                #team_txt = guild.get(guild.text_channels, name=role)
                #team_voice = guild.get(guild.voice_channels, name=role)
                #await team_txt.delete(reason='!purged')
                #await team_voice.delete(reason='!purged')
                await role.delete()
        await self.all_teams(ctx)
        await ctx.send('All teams removed')
        all_created_teams = []

    @commands.command(name='test', hidden=True)
    async def test(self, ctx):
        guild = ctx.guild
        everyone_role = get(guild.roles, name='@everyone')
        roles = ctx.author.roles
        if everyone_role in roles:
            roles.remove(everyone_role)
        print(ctx.send(roles))

    """
    @commands.command(name='oldcreate', hidden=True)
    async def oldcreate(self, ctx, *, role):
        created_teams = []
        print(ctx.guild.roles)

        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                await ctx.send(role)

                created_teams.append(role)
                if ctx.author in role.members:
                    work = False
                else:
                    work = True

        guild = ctx.guild
        new_col = random.choice(Colors)
        if ('@' or 'participant' or 'TechHacks' or 'everyone' or '#' or 'http' or '.') in role or (
               role in created_teams):
               await ctx.send(f'frick off {ctx.author.mention}')
        else:
            await guild.create_role(name=role, color=new_col, hoist=True)
            role = guild.get_role(name=role)
            user = ctx.message.author
            await user.add_roles(role)
            embed = discord.Embed(title=f'New Team {role} Created!', description='', color=new_col)
            await ctx.send(embed=embed)

            await self.all_teams(ctx)
            print(created_teams)

    #else:
    #    await ctx.send('You are already on a team!')
    #    print(created_teams)
    """


def setup(bot):
    bot.add_cog(Teams(bot))
