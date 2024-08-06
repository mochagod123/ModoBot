import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import json
import asyncio
from pymongo import MongoClient
import sys
import time

COOLDOWN_AMOUNT = 2.0  # seconds
last_executed = time.time()
def assert_cooldown():
    global last_executed  # you can use a class for this if you wanted
    if last_executed + COOLDOWN_AMOUNT < time.time():
        last_executed = time.time()
        return True
    return False

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def panels(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @panels.command(name="poll")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ank(self, ctx, *, arg):
        try:
            if arg:
                aka = arg.split(' ')
                a = aka[1]
                b = aka[2]
                c = aka[3].replace("None", "*")
                d = aka[4].replace("None", "*")
                e = aka[5].replace("None", "*")
                embed=discord.Embed(title=f"{aka[0]}", description=f"```[1] ... {a}\n[2] ... {b}\n[3] ... {c}\n[4] ... {d}\n[5] ... {e}```\n下のリアクションを付けて答えてください。", color=0xa6c412)
                m = await ctx.send(embed=embed)
                await m.add_reaction("<:1_:1266356576948850780>")
                await m.add_reaction("<:2_:1266356598524215326>")
                await m.add_reaction("<:3_:1266633035907072062>")
                await m.add_reaction("<:4_:1266633061303324682>")
                await m.add_reaction("<:5_:1266633990341660733>")
            else:
                await ctx.send("エラー。")
        except:
            await ctx.send("エラー。\n5つ必ず埋める必要があります。\n空いている場合は、「None」でうめてください。")

    @panels.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def rolepanel(self, ctx, role: discord.Role):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            try:
                embed=discord.Embed(title=f"{role.name}", description=f"リアクションでロールを入手する", color=0xa6c412)
                m = await ctx.send(embed=embed)
                await m.add_reaction("🏅")
                add_datad = {f"IDs": f"{m.id}"}
                client['Main']["RolePanel"].delete_one(add_datad)
                add_data = {f"IDs": f"{m.id}", f"Role": f"{role.id}"}
                client['Main']["RolePanel"].insert_one(add_data)
            except:
                await ctx.send("Error!")
        except:
            await ctx.send(f"{sys.exc_info()}")


    @panels.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def top(self, ctx):
        try:
            lists = []
            async for ad in ctx.channel.history(limit=1, oldest_first=True):
                lists.append(ad.jump_url)
            embed = discord.Embed(title="最上部に移動する", url=lists[0])
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"{sys.exc_info()}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, pl):
        try:
            if pl.member.bot:
                return
            if not assert_cooldown():
                return
            client = MongoClient('mongodb://localhost:27017/')
            for mon in client["Main"]["RolePanel"].find():
                if mon["IDs"] == f"{pl.message_id}":
                    guild = self.bot.get_guild(pl.guild_id)
                    member = guild.get_member(pl.user_id)
                    role = guild.get_role(int(mon["Role"]))
                    await member.add_roles(role)
                    channel = self.bot.get_channel(pl.channel_id)
                    msg = await channel.send(f"{role.name}を{member.name}に付与しました。")
                    await asyncio.sleep(3)
                    await msg.delete()
                else:
                    pass
        except:
            channel = self.bot.get_channel(pl.channel_id)
            await channel.send(f"{sys.exc_info()}")

async def setup(bot):
    await bot.add_cog(Panel(bot))