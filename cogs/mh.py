import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import json
import asyncio
from translate import Translator

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

async def setup(bot):
    await bot.add_cog(MonsterHunter(bot))