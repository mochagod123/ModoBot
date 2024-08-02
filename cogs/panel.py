import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import json
import asyncio
from pymongo import MongoClient

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

async def setup(bot):
    await bot.add_cog(Panel(bot))