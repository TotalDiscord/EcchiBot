import discord
from discord.ext import commands
import time

def owner_check(ctx):
        return ctx.message.author.id == 350765965278969860

class misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    @commands.check(owner_check)
    @commands.command(name="ping", pass_context=True)
    async def pingt(self, ctx):
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.send("Pong: ``{}ms`` :ping_pong:".format(round((t2-t1)*1000)))

    @commands.command(name="cike_time")
    async def localtime(self, ctx):
        seconds = time.time()
        local_time = time.ctime(seconds)
        await ctx.send("Local cike time: " + local_time)



def setup(bot):
    bot.add_cog(misc(bot))