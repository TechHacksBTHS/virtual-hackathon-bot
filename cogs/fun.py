import discord, random
from discord.ext import commands

def attachm(message):
    if (len(message.attachments) > 0 or 'https://' in message.content):
        return True
    else:
        return False

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('fun.py online')


    @commands.Cog.listener()
    async def on_message(self, message):
        if attachm(message):
            await message.add_reaction('<:upvote:776161705960931399>')
            await message.add_reaction('<:downvote:776162465842200617>')



def setup(bot):
    bot.add_cog(Fun(bot))
