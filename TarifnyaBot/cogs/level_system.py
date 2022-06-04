import discord
import json

from discord import File
from discord.ext import commands
from typing import Optional
from easy_pil import Editor, load_image_async, Font

level = ["►│TarifnyaFAN𝟯", "►│TarifnyaFAN𝟮", "►│TarifnyaFAN𝟭"]

level_num = [10, 15, 20]


class Levelsys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Level system : ✅")


    @commands.Cog.listener()
    async def on_message(self, message):

        if not message.content.startswith("?"):

            if not message.author.bot:
                with open("levels.json", "r") as f:
                    data = json.load(f)


                if str(message.author.id) in data:
                    xp = data[str(message.author.id)]['xp']
                    lvl = data[str(message.author.id)]['level']

                    increased_xp = xp + 25
                    new_level = int(increased_xp / 100)

                    data[str(message.author.id)]['xp'] = increased_xp

                    with open("levels.json", "w") as f:
                        json.dump(data, f)

                    if new_level > lvl:
                        data[str(message.author.id)]['level'] = new_level
                        data[str(message.author.id)]['xp'] = 0

                        with open("levels.json", "w") as f:
                            json.dump(data, f)

                        for i in range(len(level)):
                            if new_level == level_num[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level[i]))

                                mbed = discord.Embed(title=f"Gratulálok {message.author.name} Elérted a **{level[i]} rangot! 🎉🎉🎉🎉**",
                                                     color=message.author.colour)
                                mbed.set_thumbnail(url=message.author.avatar_url)
                                channel = self.bot.get_channel(975097759860400198)
                                await channel.send(embed=mbed)

                        userr = message.author

                        with open("levels.json", "r") as f:
                            data = json.load(f)

                        xp = data[str(userr.id)]["xp"]
                        lvl = data[str(userr.id)]["level"]

                        next_level_xp = (lvl + 1) * 100
                        xp_need = next_level_xp
                        xp_have = data[str(userr.id)]["xp"]

                        percentage = int(((xp_have * 100) / xp_need))

                        if percentage < 1:
                            percentage = 0
                        background = Editor(f"zIMAGE2.png")
                        profile = await load_image_async(str(userr.avatar_url))

                        profile = Editor(profile).resize((150, 150)).circle_image()

                        poppins = Font.poppins(size=40)
                        poppins_small = Font.poppins(size=30)

                        ima = Editor("zBLACK.png")
                        background.blend(image=ima, alpha=.5, on_top=False)

                        background.paste(profile.image, (30, 30))

                        background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
                        background.bar(
                            (30, 220),
                            max_width=650,
                            height=40,
                            percentage=percentage,
                            fill="green",
                            radius=20,
                        )
                        background.text((200, 40), str(userr.name), font=poppins, color="green")

                        background.rectangle((200, 100), width=350, height=2, fill="green")
                        background.text(
                            (200, 130),
                            f"Level : {lvl}   "
                            + f" XP : {xp} / {(lvl + 1) * 100}",
                            font=poppins_small,
                            color="green",
                        )
                        card = File(fp=background.image_bytes, filename="zCARD.png")
                        channel = self.bot.get_channel(975097759860400198)
                        await channel.send(f"{message.author.mention} szintet lépett. El érte a {new_level}. szintet!")
                        await channel.send(file=card)
                else:
                    data[str(message.author.id)] = {}
                    data[str(message.author.id)]['xp'] = 0
                    data[str(message.author.id)]['level'] = 1

                    with open("levels.json", "w") as f:
                        json.dump(data, f)

    @commands.command(name="rank")
    async def rank(self, ctx: commands.Context, user: Optional[discord.Member]):
        userr = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)

        xp = data[str(userr.id)]["xp"]
        lvl = data[str(userr.id)]["level"]

        next_level_xp = (lvl + 1) * 100
        xp_need = next_level_xp
        xp_have = data[str(userr.id)]["xp"]

        percentage = int(((xp_have * 100) / xp_need))

        if percentage < 1:
            percentage = 0

        ## Rank card
        background = Editor(f"zIMAGE.png")
        profile = await load_image_async(str(userr.avatar_url))

        profile = Editor(profile).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        ima = Editor("zBLACK.png")
        background.blend(image=ima, alpha=.5, on_top=False)

        background.paste(profile.image, (30, 30))

        background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percentage,
            fill="#800080",
            radius=20,
        )
        background.text((200, 40), str(userr.name), font=poppins, color="#800080")

        background.rectangle((200, 100), width=350, height=2, fill="#800080")
        background.text(
            (200, 130),
            f"Level : {lvl}   "
            + f" XP : {xp} / {(lvl + 1) * 100}",
            font=poppins_small,
            color="#800080",
        )

        card = File(fp=background.image_bytes, filename="zCARD.png")
        await ctx.send(file=card)

    @commands.command("rank_reset")
    @commands.has_role('►│🔧 Bot+')
    async def rank_reset(self, ctx, user: Optional[discord.Member]):
        member = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)

        del data[str(member.id)]

        with open("levels.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f"{member.mention} törölve lett a szinted")

    @commands.command(name="add_level")
    @commands.has_role('►│🔧 Bot+')
    async def add_level(self, ctx, increase_by: int, user: Optional[discord.Member]):
        member = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)

        data[str(member.id)]['level'] += increase_by

        with open("levels.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f"{member.mention}, a leveled növelve lett ennyivel : {increase_by}")

    @commands.command(name="add_xp")
    @commands.has_role('►│🔧 Bot+')
    async def add_xp(self, ctx, increase_by: int, user: Optional[discord.Member]):
        member = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)

        data[str(member.id)]['xp'] += increase_by

        with open("levels.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f"{member.mention}, az xp szinted növelve lett ennyivel : {increase_by}")


def setup(client):
    client.add_cog(Levelsys(client))