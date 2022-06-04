import discord
from discord_components import *
from discord.ext import commands
import asyncio
from discord.ext.commands.errors import CommandInvokeError
import random
import datetime
import time


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun : ✅')

#-----------------------------------LINKCREATE----------------------------------------------


    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def lc(self, ctx, url=None, *, button=None):
        print(f"{ctx.author.name} használta az lc parancsot")
        if url == None:
            ctx.send("Írj valami Link-et")
        elif button == None:
            ctx.send("Szöveget is írj a Link mellé")
        else:
            await ctx.channel.send(
                "",
                components=[
                    Button(style=ButtonStyle.URL, label=button, url=url)
                ]
            )
            await ctx.message.delete()

#----------------------------------------MATH,VALTO--------------------------------------------------------

    @commands.command()
    async def math(self, ctx, num1:int, valami:str, num2:int):
        if valami == "+":
            sum1 = num1 + num2
            print(f'{ctx.author.name} || {num1} {valami} {num2} az {sum1}')
            embed = discord.Embed(title=f'{ctx.author.name}')
            embed.add_field(name=f'Eredményed',
                            value=f'{num1} {valami} {num2} = {sum1}')
            await ctx.send(embed=embed)
        elif valami == "-":
            sum1 = num1 - num2
            print(f'{ctx.author.name} || {num1} {valami} {num2} az {sum1}')
            embed = discord.Embed(title=f'{ctx.author.name}')
            embed.add_field(name=f'Eredményed',
                            value=f'{num1} {valami} {num2} = {sum1}')
            await ctx.send(embed=embed)
        elif valami == "/":
            sum1 = num1 / num2
            print(f'{ctx.author.name} || {num1} {valami} {num2} az {sum1}')
            embed = discord.Embed(title=f'{ctx.author.name}')
            embed.add_field(name=f'Eredményed',
                            value=f'{num1} {valami} {num2} = {sum1}')
            await ctx.send(embed=embed)
        elif valami == "*":
            sum1 = num1 * num2
            print(f'{ctx.author.name} || {num1} {valami} {num2} az {sum1}')
            embed = discord.Embed(title=f'{ctx.author.name}')
            embed.add_field(name=f'Eredményed',
                            value=f'{num1} {valami} {num2} = {sum1}')
            await ctx.send(embed=embed)

    @commands.command()
    async def valto(self, ctx, num1:int, mertek):
        if mertek.lower() == "k":
                await ctx.send(f"S{num1}E3")
        elif mertek.lower() == "m":
                await ctx.send(f"S{num1}E6")
        elif mertek.lower() == "b":
                await ctx.send(f"S{num1}E9")
        elif mertek.lower() == "t":
                await ctx.send(f"S{num1}E12")
        elif mertek.lower() == "q":
                await ctx.send(f"S{num1}E15")
        elif mertek.lower() == "qt":
            await ctx.send(f"S{num1}E18")
        else:
            await ctx.send("Nem a jó a megadott paraméter ezek közül válassz : K|M|B|T|Q|QT")

#---------------------------------------------RANDOMG------------------------------------------------

    @commands.command()
    async def randomg(self, ctx, num1 = None, num2 = None):
        print(f"{ctx.author.name} használta a randomg parancsot")
        if num1 == None:
            await ctx.send("Írj két számot pl.: ?randomg 10 30")
        elif num2 == None:
            await ctx.send("Írj két számot pl.: ?randomg 10 30")
        else:
            num = random.randint(int(num1), int(num2))
            await ctx.send(f'A kapott szám az a : {num}')


def setup(bot):
    bot.add_cog(Fun(bot))