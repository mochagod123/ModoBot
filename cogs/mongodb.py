import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import json
import asyncio
from pymongo import MongoClient 

class mongos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def mongo(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @mongo.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def add(self, ctx, a: str, b: str, c: str):
        client = MongoClient('mongodb://localhost:27017/')
        add_data = {f"{b}": f"{c}"}
        client['Main'][a].insert_one(add_data)
        embed=discord.Embed(title=f"MongoDB - {a}", description=f"「{c}」を「{b}」に追加しました!")
        await ctx.send(embed=embed)

    @mongo.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def delete(self, ctx, a: str, b: str, c: str):
        client = MongoClient('mongodb://localhost:27017/')
        add_data = {f"{b}": f"{c}"}
        client['Main'][a].delete_one(add_data)
        embed=discord.Embed(title=f"MongoDB - {a}", description=f"「{c}」から「{b}」を削除しました!")
        await ctx.send(embed=embed)

    @mongo.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def update(self, ctx, a: str, b: str, c: str, d: str):
        client = MongoClient('mongodb://localhost:27017/')
        add_data = {f"{b}": f"{c}"}
        client['Main'][a].update_one(add_data)
        embed=discord.Embed(title=f"MongoDB - {a}", description=f"「{b}」の「{c}」を\n「{d}」に編集しました!")
        await ctx.send(embed=embed)

    @mongo.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def list(self, ctx, b: str):
        client = MongoClient('mongodb://localhost:27017/')
        embed=discord.Embed(title=f"MongoDB - {b}", description=f"{list(client['Main'][b].find())}")
        await ctx.send(embed=embed)

    @mongo.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def value(self, ctx, b: str, c: int, d: str):
        client = MongoClient('mongodb://localhost:27017/')
        embed=discord.Embed(title=f"MongoDB - {b}", description=f"{list(client['Main'][b].find())[c][d]}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(mongos(bot))