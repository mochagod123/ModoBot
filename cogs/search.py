import discord
from discord.ext import commands
import asyncio
from bs4 import BeautifulSoup
import requests
import random
import csv
import sys

class helpc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def search(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @search.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def google(self, ctx, a: str):
        await ctx.send(f"https://www.google.co.jp/search?q={a.replace("@", "＠")}")

    @search.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ggrks(self, ctx, *, a):
        await ctx.send(f"http://ggrks.atspace.tv/?{a.replace("@", "＠").replace(" ", "+")}")

    @search.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def amazon(self, ctx, a: str):
        await ctx.send(f"https://www.amazon.co.jp/s?k={a.replace("@", "＠")}")

    @search.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def safeweb(self, ctx, a: str):
        await ctx.send(f"分析結果: \nhttps://safeweb.norton.com/report?url={a.replace("@", "＠")}")

    @search.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def rafi(self, ctx):
        try:
            lists = []
            filename = 'data/malnet.csv'
            with open(filename, encoding='utf8', newline='') as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    lists.append(row[1])

            embed=discord.Embed(title=f"とても危険なサイト\nURL-> {random.choice(lists).replace("http", "ht0p")}", description="このサイトはとても危険です。\nアクセスする際は自己責任でお願いします。\n(リンク切れかも。。)")
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"{sys.exc_info()}")

async def setup(bot):
    await bot.add_cog(helpc(bot))