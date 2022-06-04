import discord
import aiofiles
from discord.ext import commands
import random
import asyncio
import json
import os
import re

if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"bannedWords": []}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

bannedWords = configData["bannedWords"]




class Moderacio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderacio : ✅')


#----------------------------------KICK-------------------------------------------------------

    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def kick(self, cty, member: discord.Member, *, reason=None):
        print(f"{cty.author.name} használta a kick parancsot")
        if member == None:
            await cty.send("Írj embert indokkal együtt. /kick @ember spamelt")
        else:
            await member.kick(reason=reason)
            await cty.send(f'Kicked {member.mention} by {cty.author.mention}')

#--------------------------------------BAN----------------------------------------------------

    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        print(f"{ctx.author.name} használta a ban parancsot")
        if member == None:
            await ctx.send("Írj embert indokkal együtt. /ban @ember csúnyán beszélt")
        else:
            await member.ban(reason=reason)
            await ctx.send(f'{ctx.author.mention} kibannolta {member.mention}-t')




    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def unban(self, ctx, *, member):
        print(f"{ctx.author.name} használta a unban parancsot")
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await  ctx.send(f'{ctx.author.mention} feloldotta {user.mention} banját')
                return

#-------------------------------------MUTE----------------------------------------------------------

    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        print(f"{ctx.author.name} használta a mute parancsot")
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted') #►│👤 Tag
        TagRole = discord.utils.get(guild.roles, name='►│👤 Tag')

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False,
                                              read_messages=False)
                await ctx.send(f'Sikeres muteolás')
                await member.send(f'Le lettél némítva Tarifnya szerverén mert {reason}')
                await member.add_roles(mutedRole, reason=reason)
                await member.remove_roles(TagRole)
                break
        else:
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False,
                                              read_messages=False)
                await ctx.send(f'Sikeres muteolás')
                await member.send(f'Le lettél némítva a Tarifnya szerverén mert {reason}')
                await member.add_roles(mutedRole, reason=reason)
                await member.remove_roles(TagRole)
                break




    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def unmute(self, ctx, member: discord.Member):
        print(f"{ctx.author.name} használta az unmute parancsot")
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
        TagRole = discord.utils.get(ctx.guild.roles, name='►│👤 Tag')

        await member.remove_roles(mutedRole)
        await member.add_roles(TagRole)
        await ctx.send(f'Unmuted {member.mention}')
        await member.send('Unmuteolva lettél Tarifnya szerverén Irány chatelni')

#---------------------------------BannedWords-------------------------------------------------

    @commands.command()
    @commands.has_role("►│🔧 Bot+")
    async def abw(self, ctx, szo):
        if szo.lower() in bannedWords:
            await ctx.send("Már ki van bannolva a szó")
        else:
            bannedWords.append(szo.lower())

            with open("./config.json", "r+") as f:
                data = json.load(f)
                data["bannedWords"] = bannedWords
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()

            await ctx.send("A szó hozzá lett a adva a szó listához")
            print(f"{ctx.author.name} használta a abw parancsot")


    @commands.command()
    @commands.has_role("►│🔧 Bot+")
    async def rbw(self, ctx, bannedszo):
        if bannedszo.lower() in bannedWords:
            bannedWords.remove(bannedszo.lower())

            with open("./config.json", "r+") as f:
                data = json.load(f)
                data["bannedWords"] = bannedWords
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()

            await ctx.send("A szó törölve lett a tiltó listáról.")
        else:
            await ctx.send("A szó nincs meg tiltva.")
        print(f"{ctx.author.name} használta a rbw parancsot")

#-------------------------------------------------LOCK----------------------------------------------

    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def lock(self, ctx):
        print(f"{ctx.author.name} használta a lock parancsot")
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(title=f"🔒 Locked by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def unlock(self, ctx):
        print(f"{ctx.author.name} használta a unlock parancsot")
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(title=f"🔓 Unlocked by {ctx.author.name}")
        await ctx.send(embed=embed)


#------------------------------------------NUKE---------------------------------------------

    @commands.command()
    @commands.has_role('►│🔧 Bot+')
    async def nuke(self, ctx, amount=10000):
        print(f"{ctx.author.name} használta a nuke parancsot")
        await ctx.channel.purge(limit=int(amount))
        embed = discord.Embed(title='', Color=0xff087f)
        embed.add_field(name=f'Nuked by {ctx.author.name}',
                        value='ennek a szobának az üzenetei törölve!')
        await ctx.channel.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Moderacio(bot))