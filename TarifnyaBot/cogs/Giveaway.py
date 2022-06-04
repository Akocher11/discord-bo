import discord
from discord.ext import commands
import asyncio
from discord.ext.commands.errors import CommandInvokeError
import random
import datetime
import time

aliasis = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,    }


class Gway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def convert(self, time):
        unit = time[-1]
        if unit not in aliasis.keys():
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2
        return val * aliasis[unit]


    @commands.command(name="giveaway", aliases=["gway", "gw"])
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _giveaway(self, ctx):
        print(f"{ctx.author.name} használta a giveaway parancsot")
        em = discord.Embed(title="Giveaway parancsok", color=discord.Color.random())
        em.add_field(name="?gstart <time> <winners> <nyeremény>",
                     value="Giveawayt indít.", inline=False)
        em.add_field(name="?greroll <message_id>", value="Újra sorsolja a giveawayt.", inline=False)
        em.add_field(name="?gend <message_id>", value="Leállítja a giveawayt", inline=False)
        await ctx.send(embed=em)

    @commands.command(name="gstart", aliases=["giveawaystart", "gcreate"])
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _gstart(self, ctx, timee: str, winners: str, *, message):
        print(f"{ctx.author.name} használta a gstart parancsot")
        """
        Starts the giveaway
        """
        winners = winners.replace("w", " ")
        winners = int(winners)
        time = self.convert(timee)
        if time == -1:
            raise CommandInvokeError('Nem jó az idő meg adása : s|m|h|d')
        elif time == -2:
            raise CommandInvokeError('...')
        em = discord.Embed(title=f'{message}',
                           description=f"Reagálj :tada: hogy tudj csatlakozni\nIdő: **{timee}**\nÁltala: {ctx.author.mention}",
                           color=discord.Color.orange())
        end = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
        end = datetime.datetime.strftime(end, "%d %b %Y %I:%M %p")
        em.set_footer(text=f"{winners} Nyertes | Ends at • {end}")

        msg = await ctx.send(":tada:    **GIVEAWAY**    :tada:", embed=em)
        # print(msg)
        gchannel = ctx.channel
        await msg.add_reaction("🎉")
        await asyncio.sleep(time)
        cache_msg = await gchannel.fetch_message(msg.id)
        if "ended" not in cache_msg.content.lower():
            await self.gend(msg, em, winners, message, gchannel, end)

    async def gend(self, msg, em, winners, message, gchannel, end):
        cache_msg = await gchannel.fetch_message(msg.id)
        if cache_msg.author.id != self.bot.user.id:
            return await gchannel.send("Nincs ilyen giveaway.")
        for reaction in cache_msg.reactions:
            if str(reaction.emoji) == "🎉":
                users = await reaction.users().flatten()
                # print(reaction.users())
                if len(users) == 1:
                    await msg.edit(content=":tada:    **GIVEAWAY ENDED**    :tada:")
                    return await gchannel.send(f"Nem nyert senki mert le lett állítva : **{message}**")

        try:
            winners2 = random.sample([user for user in users if not user.bot], k=winners)
        except ValueError:
            em.add_field(name="Winners", value="Not enough participants")
            # em.description += "\n**Winners:** "
            em.set_footer(text=f"{winners} Nyertes | Ended at • {end}")
            await msg.edit(content=":tada:    **GIVEAWAY ENDED**    :tada:")
            await msg.edit(embed=em)
            return await gchannel.send("Nincs elég személy")
        else:
            y = ", ".join(winner.mention for winner in winners2)
            x = ", ".join(winner.mention for winner in winners2)
            x += f"** Nyerte/Nyerték a giveawayt, Ezt nyerte/nyerték : `{message}`**"
            em.add_field(name="Winners", value=f"{y}")
            # em.description += f"\n**Winners: ** {y}"
            em.set_footer(text=f"{winners} Nyertes | Ended at • {end}")
            em.color = discord.Color.blue()
            #
            await msg.edit(embed=em)
            await msg.edit(content=":tada:    **GIVEAWAY ENDED**    :tada:")
            await gchannel.send(x)

    @commands.command(name="reroll", aliases=["re", "greroll"])
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _reroll(self, ctx, msg_id):
        print(f"{ctx.author.name} használta a reroll parancsot")
        reroll = await ctx.fetch_message(msg_id)
        if reroll.author.id != self.bot.user.id:
            return await ctx.send("Nincs ilyen giveaway.")
        em = reroll.embeds[0]
        message = em.title
        for reaction in reroll.reactions:
            if str(reaction.emoji) == "🎉":
                users = await reaction.users().flatten()
                # print(reaction.users())
                if len(users) == 1:
                    await reroll.edit(content=":tada:    **GIVEAWAY ENDED**    :tada:")
                    return await ctx.send(f"Nem nyerte meg senki a : **{message}**")
        em = reroll.embeds[0]
        message = em.title
        winners = em.footer.text[0]
        winners = int(winners)
        users = await reroll.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winners2 = random.sample([user for user in users if not user.bot], k=winners)
        y = ", ".join(winner.mention for winner in winners2)
        em.set_field_at(0, name="Nyertes", value=f"{y}")
        await reroll.edit(embed=em)
        await ctx.send(f"**Az új nyertes/nyertesek ő/ők :** {y}, ezt kapják : `{message}`")

    @commands.command(name="gend", aliases=["giveawayend", "end"])
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def _end(self, ctx, msg_id):
        print(f"{ctx.author.name} használta a gend parancsot")
        """
        Ends the giveaway before time
        """
        msg = await ctx.fetch_message(msg_id)
        if msg.author.id != self.bot.user.id:
            return await ctx.send("Nincs ilyen Giveaway.")
        if "ended" in msg.content.lower():
            return await ctx.send("Ennek a giveawaynek már vége. Újra tudsz sorsolni : `?reroll`")
        else:
            em = msg.embeds[0]
            winners = em.footer.text[0]
            winners = int(winners)
            message = em.title
            gchannel = ctx.channel
            x = em.description.split("\n")
            x = x[1]
            x = x.split(":")
            x = x[1]
            x = x.replace("*", "")
            time = self.convert(x)
            end = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
            end = datetime.datetime.strftime(end, "%d %b %Y %I:%M %p")
            await self.gend(msg, em, winners, message, gchannel, end)


def setup(bot):
    bot.add_cog(Gway(bot))