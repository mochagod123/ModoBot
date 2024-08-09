import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
import io
import glob
import suddendeath
import aiohttp
import asyncio
from functools import cache
import cv2
import re

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def image(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def hunter(self, ctx):
        embed = discord.Embed(title="ハンター")
        fname="hunter.png"
        file = discord.File(fp="data/MonsterHunter/hunter.png",filename=fname,spoiler=False)
        embed.set_image(url=f"attachment://{fname}")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(file=file, embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def mhavatar(self, ctx, a: str):
        n = 6
        join_string = "\n"
        new_string = join_string.join([a[i:i+n] for i in range(0, len(a), n)])
        sendio = io.BytesIO()
        image1 = Image.open("data/MonsterHunter/hunter.jpg")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 50)
        draw.text((270, 0), new_string, fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="モンハンアバター")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def shinchoku(self, ctx, a: str):
        sendio = io.BytesIO()
        image1 = Image.open("data/Shinchoku/Base.png")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 10)
        draw.text((45, 24), a, fill=(255, 255, 255), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="進捗")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def robokasu(self, ctx, a: str):
        n = 8
        join_string = "\n"
        new_string = join_string.join([a[i:i+n] for i in range(0, len(a), n)])
        sendio = io.BytesIO()
        image1 = Image.open("data/Robo/Base.png")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 15)
        draw.text((40, 35), new_string, fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="ろぼかす")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yuta(self, ctx, a: str):
        sendio = io.BytesIO()
        image1 = Image.open("data/Yuta/Base.jpg")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 30)
        draw.text((75, 15), a, fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="ゆうた・ふんたー")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def dragon(self, ctx, a: str):
        n = 9
        join_string = "\n"
        new_string = join_string.join([a[i:i+n] for i in range(0, len(a), n)])
        sendio = io.BytesIO()
        image1 = Image.open("data/LDr/Base.png")
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 30)
        draw.text((110, 80), new_string, fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="なんかのドラゴン")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nikuyaki(self, ctx, *, member: discord.User):
        content = requests.get(member.display_avatar)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/NikuYaki/Base.png")
        img_resize = img.resize((50, 50))
        image1.paste(img_resize, (60, 54))
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="肉焼き")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yusha(self, ctx, *, member: discord.User):
        content = requests.get(member.display_avatar)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/DRG/Base.png")
        img_resize = img.resize((140, 172))
        image1.paste(img_resize, (175, 100))
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="勇者")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def riaju(self, ctx, *, member: discord.User):
        content = requests.get(member.display_avatar)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/Riaju/Base.jpg")
        img_resize = img.resize((184, 184))
        image1.paste(img_resize, (310, 300))
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="リア充の大爆発!")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command(name="3ds")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def sands(self, ctx):
        if not ctx.message.attachments:
            e = discord.Embed(title="添付ファイルがないです!", description="このメッセージは、\n5秒後に削除されます。")
            msg = await ctx.reply(embed=e)
            await ctx.message.delete()
            await asyncio.sleep(5)
            await msg.delete()
            return
        image_byte = ctx.message.attachments[0]
        content = requests.get(image_byte)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/3ds/Base.jpg")
        img_resize = img.resize((768, 772))
        image1.paste(img_resize, (7, 23))
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="3ds")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()
        await ctx.message.delete()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def myqu(self, ctx, user: discord.User, a: str):
        if user.id == 1206048010740432906:
            await ctx.send("管理者のコラ画像は作成できません！")
            return
        n = 7
        join_string = "\n"
        new_string = join_string.join([a[i:i+n] for i in range(0, len(a), n)])
        content = requests.get(user.display_avatar)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/MyQ/Base.png")
        img_resize = img.resize((595, 595))
        enhancer = ImageEnhance.Brightness(img_resize)
        im_enhance = enhancer.enhance(0.5)
        image1.paste(im_enhance, (0, 0))
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 50)
        fonta = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 20)
        draw.text((625, 35), new_string, fill=(250, 251, 252), font=font)
        draw.text((625, 520), user.display_name, fill=(250, 251, 252), font=fonta)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="MyQU")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def love(self, ctx, *, member: discord.User):
        content = requests.get(ctx.author.display_avatar)
        mb = io.BytesIO(content.content)
        contenta = requests.get(member.display_avatar)
        ma = io.BytesIO(contenta.content)
        sendio = io.BytesIO()
        img = Image.open(mb)
        imga = Image.open(ma)
        image1 = Image.open("data/Love/Love.png")
        img_resize = img.resize((135, 135))
        image1.paste(img_resize, (25, 45))
        img_resizea = imga.resize((135, 135))
        image1.paste(img_resizea, (385, 45))
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 50)
        draw.text((210, 245), f"{random.randint(0, 100)}%", fill=(0, 0, 0), font=font)
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="Love")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def naguru(self, ctx, *, member: discord.User):
        content = requests.get(member.display_avatar)
        pdf_data = io.BytesIO(content.content)
        sendio = io.BytesIO()
        img = Image.open(pdf_data)
        image1 = Image.open("data/naguru.jpg")
        img_resize = img.resize((67, 69))
        image1.paste(img_resize, (65, 65))
        image1.save(sendio,format="png")
        sendio.seek(0)
        amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(sendio, filename="result.png"))
        embed = discord.Embed(title="なぐる")
        embed.set_image(url=amsg.attachments[0].url)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)
        sendio.close()

    @image.command(name="5000")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def gosenchoen(self, ctx, a: str, b: str):
        embed = discord.Embed(title="5000兆円ほしい!")
        embed.set_image(url=f"https://gsapi.cbrx.io/image?top={a}&bottom={b}")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def neko(self, ctx):
        url = "https://nekobot.xyz/api/image?type=neko"
        response = requests.get(url)
        jsonData = response.json()
        embed = discord.Embed(title="猫耳娘", color=jsonData["color"])
        embed.set_image(url=jsonData["message"])
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kemomimi(self, ctx):
        url = "https://nekobot.xyz/api/image?type=kemonomimi"
        response = requests.get(url)
        jsonData = response.json()
        embed = discord.Embed(title="ケモミミちゃん", color=jsonData["color"])
        embed.set_image(url=jsonData["message"])
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def food(self, ctx):
        url = "https://nekobot.xyz/api/image?type=food"
        response = requests.get(url)
        jsonData = response.json()
        embed = discord.Embed(title="食べ物", color=jsonData["color"])
        embed.set_image(url=jsonData["message"])
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def coffee(self, ctx):
        url = "https://nekobot.xyz/api/image?type=coffee"
        response = requests.get(url)
        jsonData = response.json()
        embed = discord.Embed(title="コーヒー☕", color=jsonData["color"])
        embed.set_image(url=jsonData["message"])
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kanna(self, ctx):
        url = "https://nekobot.xyz/api/image?type=kanna"
        response = requests.get(url)
        jsonData = response.json()
        embed = discord.Embed(title="カンナちゃん", color=jsonData["color"])
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=jsonData["message"])
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def poke(self, ctx):
        url = "https://api.waifu.pics/sfw/poke"
        response = requests.get(url)
        jsonData = response.json()
        embed = discord.Embed(title="突く")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=jsonData["url"])
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def dog(self, ctx):
        url = "https://dog.ceo/api/breeds/image/random"
        response = requests.get(url)
        jsonData = response.json()
        embed = discord.Embed(title="犬")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=jsonData["message"])
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def httpcat(self, ctx, a: str):
        embed = discord.Embed(title="HttpCat")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://http.cat/{a}")
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def fox(self, ctx):
        url = "https://randomfox.ca/floof/"
        response = requests.get(url)
        jsonData = response.json()
        embed = discord.Embed(title="きつね🦊")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=jsonData["image"])
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nounai(self, ctx, a: str):
        embed = discord.Embed(title="脳内メーカー")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://maker.usoko.net/nounai/img/{a}.gif")
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def isekai(self, ctx, a: str):
        embed = discord.Embed(title="異世界家系図メーカー")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/kakeizu_fantasy/r/img/{a}.gif")
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def kabuto(self, ctx, a: str):
        embed = discord.Embed(title=f"{a}の兜")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/kabuto/img/{a}.gif")
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def smartphone(self, ctx, a: str):
        embed = discord.Embed(title=f"{a}のスマホ")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_image(url=f"https://usokomaker.com/sumaho/img/{a}.gif")
        msg = await ctx.reply(embed=embed)

    @image.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def hikakin(self, ctx):
        embed = discord.Embed(title="ヒカキン")
        list = glob.glob('data/Hikakin/*.png')
        data = random.choice(list)
        file=discord.File(data, filename="hikakin.png")
        embed.set_image(url=f"attachment://hikakin.png")
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        await ctx.reply(file=file, embed=embed)

    @commands.group(invoke_without_command=True)
    async def text(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @text.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def suddendeath(self, ctx, a: str):
        await ctx.reply(f"```{suddendeath.suddendeathmessage(a).replace("@", "")}```")

    @text.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def yudachat(self, ctx, a: str):
        url = f"https://script.google.com/macros/s/AKfycbxhkPAagftxnWMP5kFa3UKOGDqtWSFUw3-g8usEXjXTnAjAg97zGq1W0zUgpXejXOk/exec?message={a}"
        response = requests.get(url)
        jsonData = response.json()
        embed=discord.Embed(title="ゆだチャット", description=f"{jsonData["message"]}", color=0x800000)
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")
        embed.set_footer(text="by YudaAPI", icon_url="https://stat.ameba.jp/user_images/20090904/04/lava7night/a1/b2/j/o0400040010246539099.jpg")
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))