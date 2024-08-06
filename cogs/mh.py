import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import json
import asyncio
from translate import Translator
from discord import Webhook
import aiohttp

class MonsterHunter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def mh(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @mh.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def mhww(self, ctx, a: str):
        try:
            url = f"https://mhw-db.com/weapons/{a}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            jsonData = response.json()
            translator = Translator(from_lang = "en", to_lang = "ja")
            result = translator.translate(jsonData["name"])
            embed = discord.Embed(title=result, color=0x702f00)
            embed.set_image(url=jsonData['assets']['image'])
            embed.set_thumbnail(url=jsonData['assets']['icon'])
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。\nそのような武器はない。")

    @mh.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def mhwa(self, ctx, a: str):
        try:
            url = f"https://mhw-db.com/armor/{a}"
            response = requests.get(url)
            jsonData = response.json()
            if not jsonData["assets"] == None:
                embed = discord.Embed(title=jsonData["name"], color=0x702f00)
                embed.set_image(url=jsonData["assets"]['imageMale'])
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="致命的なエラー。", color=0x702f00)
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="エラー。\nそのような武器はない。", color=0x702f00)
            await ctx.send(embed=embed)

    @mh.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def sayuta(self, ctx):
        try:
            meigen = ["はちみつちょうだい", "秘薬ください", "よろしく", "これいこ", "はやくいこ(ﾁﾘﾝﾁﾘﾝﾁﾘﾝﾁﾘﾝ)", "しっぽきって やくめでしょ", "かいぞうクエちょうだい", "これうごくやつ？", "ふざきんな!!111"]
            icon = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-ZkkfRJ1eBaRHYa19He8-NpYntiUSf00eCQ&s", "https://www.4gamer.net/games/245/G024582/20141118074/TN/004.jpg"]
            whname = f"ModoBot-Yuta"
            ch_webhooks = await ctx.channel.webhooks()
            webhooks = discord.utils.get(ch_webhooks, name=whname)
            if webhooks is None:
                webhooks = await ctx.channel.create_webhook(name=f"{whname}")
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhooks.url, session=session)
                await webhook.send(f"{random.choice(meigen)}", username=f"ゆうた", avatar_url=f"{random.choice(icon)}")
            await ctx.message.delete()
        except:
            await ctx.send("Error!")

async def setup(bot):
    await bot.add_cog(MonsterHunter(bot))