import os
import praw
import discord
import random
import asyncio
from pybooru import Danbooru
from random import randint, sample
from os import path
from discord.ext import commands, tasks
from discord.ext.commands import cooldown
from concurrent.futures import ThreadPoolExecutor

dan = Danbooru('danbooru')
def danbooru(tags):
    for i in range(0,5):
        while True:
            try:
                posts = dan.post_list(tags=tags, limit=1, random="True")
                return posts[0]['file_url'], posts[0]['id'], posts[0]['created_at'], posts[0]['source']
            except KeyError:
                continue
            break          

class nsfw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    @commands.cooldown(1,1)
    @commands.command()
    async def hentai(self, ctx):
        loop = asyncio.get_event_loop()
        tags = "rating:explicit"
        post = await loop.run_in_executor(ThreadPoolExecutor(), danbooru, tags)
        embed = discord.Embed(title="Post: "+str(post[1]), description="Uploaded: "+str(post[2]), color=discord.Color.dark_red(), url="https://danbooru.donmai.us/posts/"+str(post[1]))
        embed.set_image(url=post[0])
        embed.set_footer(text="Source: "+str(post[3]))
        await ctx.send(embed=embed)

    @commands.cooldown(1,1)
    @commands.command()
    async def booru(self, ctx, tags):
        loop = asyncio.get_event_loop()
        post = await loop.run_in_executor(ThreadPoolExecutor(), danbooru, tags)
        embed = discord.Embed(title="Post: "+str(post[1]), description="Uploaded: "+str(post[2]), color=discord.Color.dark_red(), url="https://danbooru.donmai.us/posts/"+str(post[1]))
        embed.set_image(url=post[0])
        embed.set_footer(text="Source: "+str(post[3]))
        await ctx.send(embed=embed)

    @commands.cooldown(1,1)
    @commands.command()
    async def anime(self, ctx, tags: str = "rating:safe"):
        loop = asyncio.get_event_loop()
        post = await loop.run_in_executor(ThreadPoolExecutor(), danbooru, tags)
        embed = discord.Embed(title="Post: "+str(post[1]), description="Uploaded: "+str(post[2]), color=discord.Color.dark_red(), url="https://danbooru.donmai.us/posts/"+str(post[1]))
        embed.set_image(url=post[0])
        embed.set_footer(text="Source: "+str(post[3]))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(nsfw(bot))
    
