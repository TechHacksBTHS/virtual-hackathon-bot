import discord, random
from discord.ext import commands


#FAQ

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def faq(self, ctx):
        await ctx.send('yes sir')



def setup(bot):
    bot.add_cog(Example(bot))
