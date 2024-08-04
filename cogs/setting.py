import discord
from discord.ext import commands
import requests
from pymongo import MongoClient
import asyncio
import json

class setting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message_cmd(self, message):
        if "mo." in message.content or "mo#" in message.content or "mo!" in message.content:
            with open('local/save.json') as f:
                count = json.load(f)
                tasu = count['commandcount'] + 1
                count['commandcount'] = tasu
                with open('local/save.json', 'w') as fa:
                    json.dump(count, fa, indent=2)

            count = len(self.bot.guilds)
            raw_ping = self.bot.latency
            ping = round(raw_ping * 1000)
            await self.bot.change_presence(activity=discord.CustomActivity(name=f"{count}鯖 | {len(self.bot.users)}人"))

            await asyncio.sleep(2)

    @commands.group(invoke_without_command=True)
    async def setting(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @setting.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def count(self, ctx):
        try:
            with open('local/save.json') as f:
                count = json.load(f)
            embed=discord.Embed(title="コマンドカウント", description=f"「{count['commandcount']}回」実行されました。", color=0xa6c412)
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー。")

async def setup(bot):
    await bot.add_cog(setting(bot))