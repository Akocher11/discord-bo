import discord
import aiofiles
from discord.ext import commands
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




token = "OTUyOTgwMzEyNDM3MTgyNDY0.Yi96FA.YBEcAsLg-U_ApEymua4ZJENU1LI"
bannedWords = configData["bannedWords"]


bot = commands.Bot(command_prefix='?')
bot.ticket_configs = {}



@bot.event  # Bot elindító
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="/help / Prefix : /"))
    print(f"\n\n\nBot logged in as {bot.user}\n\n-------------------------------------------------\n\nGstart : ✅\nTTT : ✅")
    async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
        pass

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')




@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.id != bot.user.id and str(payload.emoji) == u"\U0001F3AB":
        msg_id, channel_id, category_id = bot.ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = bot.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)
            ticket_channel = await category.create_text_channel(f"ticket-{payload.member.display_name}",
                                                                topic=f"A ticket for {payload.member.display_name}.",
                                                                permission_synced=True)

            await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)

            message = await channel.fetch_message(msg_id)
            await message.remove_reaction(payload.emoji, payload.member)

            await ticket_channel.send(
                f"{payload.member.mention} a ticketed elkészült! használd a **'/close'** parancsot hogy be zárhasd a ticketet.")

            try:
                await bot.wait_for("message", check=lambda
                    m: m.channel == ticket_channel and m.content == "/close",
                                   timeout=3600)

            except asyncio.TimeoutError:
                await ticket_channel.delete()

            else:
                await ticket_channel.delete()

def msg_contains_word(msg, word):
    return re.search(fr'\b({word})\b', msg) is not None


@bot.event
async def on_message(message):
    messageAuthor = message.author

    if bannedWords != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for bannedWord in bannedWords:
            if msg_contains_word(message.content.lower(), bannedWord):
                await message.delete()
                await message.channel.send(
                    f"{messageAuthor.mention} az üzeneted törölve lett ne beszélj csúnyán")

    await bot.process_commands(message)

bot.run(token)