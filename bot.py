import os
import discord
import time
import logging
import json
from discord.ext import commands
from discord import Game, Embed, Color, Status, ChannelType
from random import randint, sample
from discord.ext.commands import cooldown
from os import path


#Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open("config.json") as f:
    config = json.load(f)


OWNER = 350765965278969860

#Cogs
initial_extensions = ['cogs.misc',
                      'cogs.owner',
                      'cogs.nsfw']

# Creating bot instance
bot = commands.Bot(command_prefix=config.get('prefix'), self_bot=False, owner_id=OWNER, case_insensitive=True, help_command=None)

#Loaading cogs

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

#listeners

@bot.event
async def on_ready():
    id = bot.user.id
    bot_user = bot.user.name
    print ("------------------------------------")
    print ("Bot Name: " + bot_user)
    print ("Bot ID: " + str(id))
    print ("discord.py version: " + discord.__version__)
    print ("------------------------------------")
    if path.isfile("presence.txt"):
        with open("presence.txt") as f:
            presence = f.readline()
            await bot.change_presence(activity=discord.Game(name=presence, type=1))
    else:
        with open("presence.txt", "w") as f:
            f.write("Prefix: "+str(config.get('prefix')))
        with open("presence.txt") as f:
            presence = f.readline()
            await bot.change_presence(activity=discord.Game(name=presence, type=1))


#Message on error event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on a cooldown, please try again in {:.2f}s'.format(error.retry_after)
        user = ctx.message.author
        await user.send(msg)
        await ctx.message.add_reaction(emoji="❌")
    elif isinstance(error, commands.CheckFailure):
        msg = 'You do not have the required permission to use this command!.'
        user = ctx.message.author
        await user.send(msg)
    elif isinstance(error, commands.CommandNotFound):
        msg = '**This command does not exist!**'
        user = ctx.message.author
        await user.send(msg)
    else:
        raise error

#Help commands
@bot.command()
async def help(ctx):
    user = ctx.message.author
    helpembed = discord.Embed(color=discord.Color.red())
    helpembed.set_author(name="Help (Base commands)")
    helpembed.add_field(name="-help_image", value="Shows help for image commands.",inline=False)
    helpembed.add_field(name="-help", value="Shows this message :rofl:",inline=False)
    await user.send(embed=helpembed)
    await ctx.message.add_reaction(emoji="✅")

@bot.command()
async def help_image(ctx):
    user = ctx.message.author
    helpembed = discord.Embed(color=discord.Color.red())
    helpembed.set_author(name="Help (Image commands)")
    helpembed.add_field(name="-anime", value="Sends SFW anime images.",inline=False)
    helpembed.add_field(name="-booru", value="hentai (tag) , sends an image according to the tag you specifiy.",inline=False)
    helpembed.add_field(name="-hentai", value="Sends hentai images.",inline=False)
    helpembed.add_field(name="-help", value="Shows help for base commands.",inline=False)
    helpembed.add_field(name="-help_image", value="Shows this message :rofl:",inline=False)
    await user.send(embed=helpembed)
    await ctx.message.add_reaction(emoji="✅")

# Authentication
print("[INFO] Starting up and logging in...")
bot.run(config.get('token'), bot=True, reconnect=True)