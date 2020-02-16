import os, praw, discord, random, asyncio, json, time
from pybooru import Danbooru
from random import randint, sample
from os import path
from discord.ext import commands, tasks
from discord.ext.commands import cooldown
from concurrent.futures import ThreadPoolExecutor

with open("config.json") as f:
    config = json.load(f)

#Functions
dan = Danbooru('danbooru', username=config.get('danbooru_username'), api_key=config.get('danbooru_key'))
def danbooru(tags):
    for i in range(0,5):
        while True:
            try:
                time.sleep(1) #Wait x seconds so that danbooru doesnt fuck itself
                print("Sleep done")
                posts = dan.post_list(tags=tags, limit=1, random="True")
                print("Ran booru fetchery")
                return posts[0]['file_url'], posts[0]['id'], posts[0]['created_at'], posts[0]['source']
            except KeyError:
                print("Got KeyError")
                continue
            except TimeoutError:
                print("Fucker timed out")
                time.sleep(5)
                continue
            except ConnectionError:
                print("Fucker timed out ConnectionError")
                time.sleep(5)
                continue                
            break
#Tasks
@tasks.loop(minutes=10, reconnect=True,)
async def keepboorualive():
    print("Stayin alive, stayin alive, aaah aah aah ah STAYYYIN ALLIIIIIVE!")
    danbooru(tags=None)


async def booruembed(tags: str = None):    
        loop = asyncio.get_event_loop()
        post = await loop.run_in_executor(ThreadPoolExecutor(), danbooru, tags)
        embed = discord.Embed(title="Post: "+str(post[1]), description="Uploaded: "+str(post[2]), color=discord.Color.dark_blue(), url="https://danbooru.donmai.us/posts/"+str(post[1]))
        embed.set_image(url=post[0])
        embed.set_footer(text="Source: "+str(post[3]))
        return embed

class nsfw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0
    
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Starting ting")

    #Commands
    @commands.cooldown(1,1)
    @commands.is_nsfw()
    @commands.command()
    async def hentai(self, ctx):
        embed = await booruembed(tags="rating:explicit")
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.cooldown(1,1)
    @commands.is_nsfw()
    @commands.command()
    async def booru(self, ctx, tags, tags1: str=""):
        embed = await booruembed(tags=tags+" "+tags1)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.cooldown(1,1)
    @commands.command()
    async def anime(self, ctx):
        embed = await booruembed(tags="rating:safe")
        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(nsfw(bot))
    
