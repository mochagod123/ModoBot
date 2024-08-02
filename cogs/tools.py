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
import tweepy

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

async def setup(bot):
    await bot.add_cog(Tools(bot))