import discord
from discord_components import *
from discord.ext import commands
import asyncio
from discord.ext.commands.errors import CommandInvokeError
import random
import datetime
import time


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun : ✅')


    @commands.command()
    async def otlet(self, ctx, *, saymsg=None):
        if saymsg == None:
            return await ctx.send("Írj valami ötletet a ?otlet után és úgy jó lesz!")
        sayEmbed = discord.Embed(title=f"{ctx.author.name} ötlete :", color=discord.Color.blue(),
                                 description=f"{saymsg}")

        Embed = await ctx.send(embed=sayEmbed)
        await Embed.add_reaction(emoji="✅")
        await Embed.add_reaction(emoji="❌")

    @commands.command()
    async def csay(self, ctx, room, *, message):
        gen = int(room[2: -1])
        channel = self.bot.get_channel(gen)
        await channel.send(message)
        print(f"{ctx.author.name} használta a csay parancsot")

    @commands.command()
    async def SayEmbed(self, ctx, uzenet_cim, uzenet_tartalma, csatorna_neve):
        Embed = discord.Embed(title=uzenet_cim, description=uzenet_tartalma)
        id = int(csatorna_neve[2: -1])
        channel = self.bot.get_channel(id)
        await channel.send(embed=Embed)
        print(f"{ctx.author.name} használta a sayembed parancsot")


def setup(bot):
    bot.add_cog(Chat(bot))