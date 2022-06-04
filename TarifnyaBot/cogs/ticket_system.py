import discord
import aiofiles
from discord.ext import commands
import random
import asyncio
import json
import os
import re


class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.ticket_configs = {}

    @commands.Cog.listener()
    async def ready(self):
        print("Randomg : ✅")
        async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
            pass

        async with aiofiles.open("ticket_configs.txt", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                self.bot.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]



    @commands.command()
    async def tic(self, ctx, msg: discord.Message = None, category: discord.CategoryChannel = None):
        if msg is None or category is None:
            await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid.")
            return

        self.bot.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id]  # this resets the configuration

        async with aiofiles.open("ticket_configs.txt", mode="r") as file:
            data = await file.readlines()

        async with aiofiles.open("ticket_configs.txt", mode="w") as file:
            await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")
            for line in data:
                if int(line.split(" ")[0]) != ctx.guild.id:
                    await file.write(line)

        await msg.add_reaction(u"\U0001F3AB")
        await ctx.channel.send("A ticket config készen van! :)")
        print(f"{ctx.author.name} használta a tic parancsot")

    @commands.command()
    async def t_config(self, ctx):
        try:
            msg_id, channel_id, category_id = self.bot.ticket_configs[ctx.guild.id]

        except KeyError:
            await ctx.send("The ticket system is not configured")
        else:
            embed = discord.Embed(title="Ticket System Configartions", color=discord.Color.green())
            embed.description = f'**Reaction Message ID** : {msg_id}\n'
            embed.description += f'**Ticket Category ID** : {category_id}\n\n'

            await ctx.channel.send(embed=embed)
        print(f"{ctx.author.name} használta a t_config parancsot")

def setup(bot):
    bot.add_cog(TicketSystem(bot))