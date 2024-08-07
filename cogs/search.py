import discord
from discord.ext import commands
import asyncio
from bs4 import BeautifulSoup
import requests
import csv
import sys
import random
import urllib.request

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
    async def ggrks(self, ctx, a: str):
        await ctx.send(f"http://ggrks.atspace.tv/?{a.replace("@", "＠")}")

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

    @search.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def niconico(self, ctx, key: str):
        try:
        #対象のサイトURL
            url = f"https://www.nicovideo.jp/search/{urllib.parse.quote_plus(key, encoding='utf-8')}?ref=nicotop_search"

            #URLリソースを開く
            res = urllib.request.urlopen(url)

            #インスタンスの作成
            soup = BeautifulSoup(res, 'html.parser')

            #必要な要素とclass名
            name = soup.find_all("p", class_="itemTitle")
            url = soup.find_all("a", class_="itemThumbWrap")

            #取得したタイトル情報を出力
            ret = []
            rets = []
            for t in name:
                ret.append(t.text)
            for a in ret:
                if a != '':
                    rets.append(a)

            reta = []
            retsa = []
            for t in url:
                reta.append(t['href'])
            for a in reta:
                if a != '':
                    retsa.append(a)

            embed=discord.Embed(title="NicoNico検索", description=f"{rets[0].replace("@", "")}\nhttps://www.nicovideo.jp{retsa[0].replace("@", "")}", color=0x00ff62, url=f"https://www.nicovideo.jp{retsa[0].replace("@", "")}")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✖")

            while True:
                def check(r, u):
                    if u.id == ctx.author.id:
                        return r.message.id == msg.id
                    else:
                        return False
                r, _ = await self.bot.wait_for("reaction_add", check=check, timeout=60)
                await r.remove(ctx.author)
                if r.emoji == "✖":
                    await ctx.message.delete()
                    await msg.delete()
                    break

        except IndexError:
            embed=discord.Embed(title="NicoNico検索", description="エラーが発生しました。\nそのような動画はありませんでした。", color=0x00ff62)
            await ctx.send(embed=embed)
        except:
            return

    @search.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ulookup(self, ctx, usera: int):
        try:
            user = await self.bot.fetch_user(usera)
            embed = discord.Embed(title=f"{user.display_name}",color=user.accent_color)
            embed.add_field(name="ユーザーの名前",value=str(user))
            embed.add_field(name="アカウント作成日",value=user.created_at)
            if user.bot:
                embed.add_field(name="Botかどうか？",value="はい")
            else:
                embed.add_field(name="Botかどうか？",value="いいえ")
            embed.set_thumbnail(url=user.avatar)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✖")

            while True:
                def check(r, u):
                    if u.id == ctx.author.id:
                        return r.message.id == msg.id
                    else:
                        return False
                r, _ = await self.bot.wait_for("reaction_add", check=check, timeout=60)
                await r.remove(ctx.author)
                if r.emoji == "✖":
                    await ctx.message.delete()
                    await msg.delete()
                    break
            return
        except:
            return

    @search.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def slookup(self, ctx, ser: discord.Guild):
        try:
            user = await self.bot.fetch_user(ser.owner_id)
            embed = discord.Embed(title="サーバー情報", color=0x70006e)
            embed.add_field(name="名前",value=str(ser))
            embed.add_field(name="サーバーID",value=str(ser.id))
            embed.add_field(name="オーナーID",value=str(ser.owner_id))
            embed.add_field(name="オーナーの名前",value=f"{user.display_name}")
            embed.add_field(name="オーナーの作成日",value=f"{user.created_at}")
            embed.set_thumbnail(url=ser.icon)
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"{sys.exc_info()}")

async def setup(bot):
    await bot.add_cog(helpc(bot))