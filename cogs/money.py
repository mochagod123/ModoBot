import discord
from discord.ext import commands
import asyncio
import sys
import random
from pymongo import MongoClient 

class MoneySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def moneys(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @moneys.group()
    @commands.cooldown(1, 1200, type=commands.BucketType.user)
    async def work(self, ctx):
        mon =  random.randint(500,1000)
        client = MongoClient('mongodb://localhost:27017/')
        try:
            for mons in client["Main"]["Money"].find():
                if not mons["IDs"] == f"{ctx.author.id}":
                    add_datad = {f"IDs": f"{ctx.author.id}"}
                    client['Main']["Money"].delete_one(add_datad)
                    add_data = {f"IDs": f"{ctx.author.id}", f"Money": f"{mon}"}
                    client['Main']["Money"].insert_one(add_data)
                else:
                    add_datad = {f"IDs": f"{ctx.author.id}"}
                    client['Main']["Money"].delete_one(add_datad)
                    add_data = {f"IDs": f"{ctx.author.id}", f"Money": f"{int(mons["Money"]) + mon}"}
                    client['Main']["Money"].insert_one(add_data)
        except:
            await ctx.send("Error!")
        embed=discord.Embed(title="働く", description=f"「{mon}円」稼ぎました！\n現実のお金には変換できません！", color=0xffc800)
        await ctx.send(embed=embed)

    @moneys.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def money(self, ctx):
        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["Money"].find():
            if mon["IDs"] == f"{ctx.author.id}":
                embed=discord.Embed(title="お金参照", description=f"「{ctx.author.name}」さんは、\n「{mon["Money"]}円」です！", color=0xffc800)
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MoneySystem(bot))