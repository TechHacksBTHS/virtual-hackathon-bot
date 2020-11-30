# teams.py
import discord, random, time
from discord.ext import commands
from discord.utils import get


# TODO display all users in a team
# TODO change team name
# TODO join teams by reacting to message

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
        """ sends an embed msg to #join-team & lists team names and members """
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

        await channel.purge(limit=100)
        if created_teams == []:
            created_teams.append('No teams yet, use !create <teamname> to create one!')
        embed = discord.Embed(title='All Teams, use !join to join one! ', description=f'{unpack(created_teams)}',
                              color=random.choice(Colors))
        # await channel.send(embed=embed)
        await channel2.send(unpack(users_in_teams))

    # @commands.command(name='getusers')
    # @commands.has_role('exec')
    def print_members(self, ctx, role: discord.Role):
        """ returns a <LIST> of users in a role """
        self.bot.wait_until_ready()
        role = str(role)
        guild = ctx.guild
        # channel = self.bot.get_channel(779380419153363004)  # private-bot-cmd
        role = discord.utils.get(guild.roles, name=role)
        users = [user.name for user in ctx.guild.members if role in user.roles]
        return users

    @commands.command(name='create')
    @commands.has_role('participant')
    async def create(self, ctx, *, role: commands.clean_content):
        await self.bot.wait_until_ready()
        participant = ctx.guild.get_role(697533967859187803)
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
            role_str = role
            role = await guild.create_role(name=role, color=new_col, hoist=True)
            user = ctx.message.author
            await user.add_roles(role)
            await role.edit(position=3)
            await user.remove_roles(participant)
            permissions = discord.PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False,
                                                      speak=False, stream=False,read_message_history=False, connect=False)

            team_perms = discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True,
                                                     speak=True, stream=True, read_message_history=True,connect=True)

            embed = discord.Embed(title=f'New Team {role} Created!', description='', color=new_col)
            await ctx.send(embed=embed)

            # ------------------------- team channels -------------------------
            guild = ctx.guild
            team_cat = guild.get_channel(699729155301834762) #get the Team Chat category
            team_txt = await guild.create_text_channel(role_str,category=team_cat, permissions=permissions) # make a team text channel
            team_vc = await guild.create_voice_channel(role_str,category=team_cat, permissions=permissions) # make a team voice channel
            await team_txt.set_permissions(role, overwrite=team_perms) # only give the team access to the tc
            await team_vc.set_permissions(role, overwrite=team_perms)  # only give the team access to the vc

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
                if len(role.members) > 7:
                    await ctx.send(f'{role} already has 6 members')
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
        all_roles = ctx.author.roles
        if 'participant' in all_roles:
            await ctx.send(f'Cannot leave particpants {ctx.author.mention}')
        else:
            for i in all_roles:
                if not i.permissions.change_nickname: # filters out any role without change nickname permission AKA the team roles
                    role = i
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
        #print(ctx.message.author)
        team_txt = discord.utils.get(guild.text_channels, name=role)  # TEAM TEXT CHANNEL
        team_voice = discord.utils.get(guild.voice_channels, name=role)  # TEAM VOICE CHANNEL
        role = discord.utils.get(guild.roles, name=role)
        participant_role = get(guild.roles, name='participant')
        if role:
            try:
                col = role.color
                embed = discord.Embed(title="The role {} has been deleted!".format(role.name), description='', color=col)
                for i in role.members:
                    member = i
                    print(i)
                    await member.add_roles(participant_role)
                # cleanup
                await team_txt.delete(reason='!removed')
                await team_voice.delete(reason='!removed')
                await role.delete()
                await ctx.send(embed=embed)
                await self.all_teams(ctx) # refresh the join-teams channel
            except discord.Forbidden:
                await ctx.send('Sorry boss, that\'s way above my pay grade')
        else:
            await ctx.send("The role doesn't exist!")

    @commands.command()
    @commands.has_role('exec')
    async def purge(self, ctx):
        await self.bot.wait_until_ready()
        guild = ctx.guild
        team_cat = guild.get_channel(699729155301834762) # get the team chat category
        participant_role = get(guild.roles, name='participant')
        for role in ctx.guild.roles:
            if not role.permissions.change_nickname:
                for i in role.members:
                    await i.add_roles(participant_role)
                await role.delete(reason='purged')
        for channel in ctx.guild.text_channels:
            if channel.category == team_cat: # remove every tc in team chat category
                await channel.delete(reason='purged')
        for channel in ctx.guild.voice_channels:
            if channel.category == team_cat: # remove every tc in team chat category
                await channel.delete(reason='purged')
        await self.all_teams(ctx)
        await ctx.send('All teams removed')
        all_created_teams = []

    @commands.command(name='test', hidden=True)
    async def test(self, ctx):
        guild = ctx.guild



def setup(bot):
    bot.add_cog(Teams(bot))
