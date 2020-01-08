import discord
import os
import json
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)

def owner_check(ctx):
        return ctx.message.author.id == int(config.get('owner'))
            
class owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0


    #OLD COMMANDS

    @commands.cooldown(1, 45, commands.BucketType.guild)
    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')

    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        if member is None:
            member = ctx.author

        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')

    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        if not member:
            member = ctx.author

        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)


    #NEW COMMANDS

    @commands.command(name='shutdown', aliases=['fuckoff'])
    @commands.check(owner_check)
    async def shutdown(self, ctx):
        await ctx.send('Shutting down! :wave:')
        await ctx.bot.logout()

    @commands.command(name='reload', aliases=['cogreload'])
    @commands.check(owner_check)
    async def reloadcog(self, ctx, *, cog):
        self.bot.reload_extension("cogs."+cog)
        await ctx.message.add_reaction(emoji="🔄")

    @commands.command(name='prefix', aliases=['change_prefix'], pass_context=True)
    @commands.check(owner_check)
    async def _prefix(self, ctx, *, defined_prefix):
        with open("config.json") as f:
            prefixprep = {'prefix': [defined_prefix]}
            json.dump("prefix", defined_prefix)
        await ctx.message.add_reaction(emoji="✅")
        

    

def setup(bot):
    bot.add_cog(owner(bot))
