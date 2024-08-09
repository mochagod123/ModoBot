import discord
from discord.ext import commands
import asyncio
import aiohttp
from discord import Webhook
import random

class Hiroyuki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def hiroyuki(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @hiroyuki.group()
    @commands.has_permissions()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def hirosay(self, ctx):
        try:
            meigen = [f"嘘を嘘と見抜けない人は、{ctx.guild.name}を使うのは難しいでしょう", "それってあなたの感想ですよね", "日本人はモラルが高いのではなく、同調圧力に弱いだけ。", "『こういうときは、こうしておこう』というルールを先に決めます", "それって明らかではないですよね？"]
            whname = f"ModoBot-Hiroyuki"
            ch_webhooks = await ctx.channel.webhooks()
            webhooks = discord.utils.get(ch_webhooks, name=whname)
            if webhooks is None:
                webhooks = await ctx.channel.create_webhook(name=f"{whname}")
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhooks.url, session=session)
                await webhook.send(f"{random.choice(meigen)}", username=f"ひろゆき", avatar_url=f"https://dol.ismcdn.jp/mwimgs/d/5/1200/img_d50898395a8e97cc62f70681d2bd541f381966.jpg")
            await ctx.message.delete()
        except:
            await ctx.send("Error!")

async def setup(bot):
    await bot.add_cog(Hiroyuki(bot))