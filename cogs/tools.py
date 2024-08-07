import discord
from discord.ext import commands
import asyncio
import requests
import urllib
import io
import aiohttp
import sys
import logging
from contextlib import redirect_stdout
from io import BytesIO
from yt_dlp import YoutubeDL
import requests
from bs4 import BeautifulSoup
import re
from pyshorteners import Shortener
from googletrans import Translator
from threading import Thread

def download_bytesio(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': '-',
        'logger': logging.getLogger()
    }

    video = BytesIO()
    with redirect_stdout(video):
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    return video


class Kukulu():
    def __init__(self,csrf_token:str=None,sessionhash:str=None,proxy:dict=None):
        self.csrf_token=csrf_token
        self.sessionhash=sessionhash
        self.proxy=proxy
        self.session=requests.Session()
        if csrf_token!=None and sessionhash!=None:
            self.session.cookies.set("cookie_csrf_token",csrf_token)
            self.session.cookies.set("cookie_sessionhash",sessionhash)
            self.session.post("https://m.kuku.lu",proxies=proxy)
        else:
            self.session.post("https://m.kuku.lu",proxies=proxy)
    
    def new_account(self):
        return {"csrf_token":self.session.cookies["cookie_csrf_token"],"sessionhash":self.session.cookies["cookie_sessionhash"]}
    
    def create_mailaddress(self):
        return self.session.get("https://m.kuku.lu/index.php?action=addMailAddrByAuto&nopost=1&by_system=1",proxies=self.proxy).text[3:]
    
    def specify_address(self,address:str):
        return self.session.get(f"https://m.kuku.lu/index.php?action=addMailAddrByManual&nopost=1&by_system=1&t=1716696234&csrf_token_check={self.csrf_token}&newdomain={address}",proxies=self.proxy).text[3:]
    
    def check_top_mail(self,mailaddress:str):
        mailaddress=mailaddress.replace("@","%40")
        mails=self.session.get(f"https://m.kuku.lu/recv._ajax.php?&q={mailaddress}&&nopost=1&csrf_token_check={self.csrf_token}",proxies=self.proxy)
        soup=BeautifulSoup(mails.text,"html.parser")
        script=soup.find_all("script")
        match = re.search("(openMailData[^ ]+)", str(script))
        openMailData=match.group()
        openMailData=openMailData.replace("openMailData(","")
        match2=re.findall(f"{openMailData} [^ ]+", str(script))
        maildata=match2[1].split("'")
        mail=self.session.post("https://m.kuku.lu/smphone.app.recv.view.php",data={"num":maildata[1],"key":maildata[3],"noscroll": "1"},proxies=self.proxy)
        soup=BeautifulSoup(mail.text,"html.parser")
        title=soup.find(class_="full").text

        #--------------------------------------------
        #ここの部分は届くメールによってよく変わるから注意
        text=soup.find(dir="ltr").text
        #m.kuku.luは便利だけど自動化するにあたっては他のプラットフォームの方がいい可能性アリ
        #----------------------------------------------------------------------------

        return {"title":title[7:-4],"text":text}

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def tools(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @tools.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def webshot(self, ctx, url: str):
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = f'url={url}&waitTime=1&browserWidth=1000&browserHeight=1000'
            url = "https://securl.nu/jx/get_page_jx.php"
            response = requests.post(url, headers=headers, data=data)
            jsonData = response.json()
            headersa = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            urla = f"https://securl.nu{jsonData["img"]}"
            response = requests.get(urla, headers=headersa)
            async with aiohttp.ClientSession() as session:
                u = urllib.parse.unquote(urla)
                fio = io.BytesIO()
                async with session.get(u) as r:
                    fio.write(await r.read())
                fio.seek(0)
                amsg = await self.bot.get_channel(1265978647391633439).send(file=discord.File(fio, filename=f"webshot.png"))
                embed = discord.Embed(title="スクリーンショット")
                embed.set_image(url=amsg.attachments[0].url)
                await ctx.reply(embed=embed)
                fio.close()
        except:
            await ctx.send(f"エラー！URLが間違えてるかも！？")

    @tools.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def afk(self, ctx, yoke: str):
        embed=discord.Embed(title="AFKになりました。", description=f"理由: {yoke}", color=0x00d5ff)
        await ctx.send(embed=embed)
        while True:
            numc = await self.bot.wait_for("message", timeout=None)
            try:
                if not numc.content == "" and numc.author == ctx.author:
                    embed=discord.Embed(title="AFKが解除されました。", description=f"理由: {yoke}", color=0x00d5ff)
                    await numc.channel.send(embed=embed)
                    break
            except:
                await ctx.reply("エラーが発生しました。")
                break

    @tools.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def wcalc(self, ctx, waw: int, watm: int, wats: int):
        try:
            calc = (waw * watm) / wats
            await ctx.send(f"電子レンジの「{waw}w ({watm}秒)」を「{wats}w」に変換すると、\n「{calc}秒」です。")
        except:
            await ctx.send("Error!")

    @tools.command(name="2ch")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nichan(self, ctx, num: int):
        try:
            if num > 301:
                await ctx.send(f"300以内にしてください。")
                return
            lists = []
            async for ad in ctx.channel.history(limit=300):
                lists.append(ad.content)

            for ads in range(len(lists)):
                if ads == num - 1:
                    embed=discord.Embed(title="2ch風引用", description=lists[ads].replace("@", "＠"), color=0xeeff00)
                    embed.set_footer(text=f"> {num}")
                    await ctx.send(embed=embed)
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

    @tools.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def shorturl(self, ctx, num: str):
        try:
            s = Shortener()
            shortened_link = s.tinyurl.short(num)
            embed = discord.Embed(title="短縮URL", description=f"{shortened_link}")
            await ctx.reply(embed=embed)
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

    @tools.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def qrcode(self, ctx, num: str):
        try:
            await ctx.reply(f"https://api.qrserver.com/v1/create-qr-code/?data={num.replace("@", "")}&size=100x100")
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

    @tools.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def trans(self, ctx, num: str):
        try:
            translator = Translator()
            translated = translator.translate(num, src='ja', dest='en')
            embed = discord.Embed(title=f"{num}の翻訳結果", description=f"{translated.text}")
            await ctx.reply(embed=embed)
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

    @tools.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def email(self, ctx):
        try:
            kukulu=Kukulu()
            token=kukulu.new_account()#dictで "csrf_token" と "sessionhash" だけが返ってくる
            kukulu=Kukulu(token["csrf_token"],token["sessionhash"])
            newmail=kukulu.create_mailaddress()
            embed = discord.Embed(title=f"Emailジェネレーター", description=f"{newmail}")
            await ctx.reply(embed=embed)
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

    @tools.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def jpy(self, ctx):
        url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=your_token'
        raw = requests.get(url)
        data = raw.json()
        datetime = data["Realtime Currency Exchange Rate"]["6. Last Refreshed"]
        USDJPY = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        embed = discord.Embed(
        title="現在のドルは何円？",
        color=0x00ff00,
        description="1$=" + USDJPY + "円")
        embed.add_field(name="最終更新時間",value=datetime)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Tools(bot))