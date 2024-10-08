import discord
from discord.ext import commands
import sys
from pymongo import MongoClient
import aiohttp
from discord import Webhook
import random

class autoreply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message_autotrply(self, message):
        if message.author.bot:
            return

        if (type(message.channel) == discord.DMChannel):
            return

        client = MongoClient('mongodb://localhost:27017/')
        for mon in client["Main"]["AutoReply"].find():
            if mon["IDs"] == f"{message.guild.id}":
                try:
                    if mon["q"] == message.content:
                        whname = f"ModoBot"
                        ch_webhooks = await message.channel.webhooks()
                        webhooks = discord.utils.get(ch_webhooks, name=whname)
                        if webhooks is None:
                            webhooks = await message.channel.create_webhook(name=f"{whname}")
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(webhooks.url, session=session)
                            await webhook.send(f"{random.choice(mon["a"].rsplit(','))}", username=f"{mon["name"]}", avatar_url=f"{mon["icon"]}")
                except:
                    continue

    @commands.hybrid_group(fallback='info', description = "自動返信関連のコマンドです。")
    async def autoreply(self, ctx):
        await ctx.reply("自動返信関連のコマンドです。")

    @autoreply.command(name = "add", with_app_command = True, description = "自動返信を作成します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def autoreply_add(self, ctx, 受け取り: str, 返し: str, 名前: str, あばたーurl: str):
        try:
            q = 受け取り
            a = 返し
            name = 名前
            icon = あばたーurl
            client = MongoClient('mongodb://localhost:27017/')
            add_data = {f"IDs": f"{ctx.guild.id}", f"q": f"{q}"}
            add_datad = {f"IDs": f"{ctx.guild.id}", f"q": f"{q}", "a": f"{a}", "name": f"{name}", f"icon": f"{icon}"}
            client['Main']["AutoReply"].delete_one(add_data)
            client['Main']["AutoReply"].insert_one(add_datad)
            await ctx.reply(embed=discord.Embed(title=f"自動返信 - {q}", description="を追加しました。"))
        except:
            await ctx.send("エラー。")

    @autoreply.command(name = "remove", with_app_command = True, description = "自動返信を削除します。")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def autoreply_remove(self, ctx, 受け取り: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"IDs": f"{ctx.guild.id}", f"q": f"{受け取り}"}
            client['Main']["AutoReply"].delete_one(add_datad)
            await ctx.reply(embed=discord.Embed(title=f"自動返信削除 - {受け取り}", description="を削除しました。"))
        except:
            await ctx.send("エラー。")

    @autoreply.command(name = "list", with_app_command = True, description = "自動返信リストを表示します、")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def autoreply_list(self, ctx):
        try:
            num = 1
            ch = []
            client = MongoClient('mongodb://localhost:27017/')
            for mon in client["Main"]["AutoReply"].find():
                if mon["IDs"] == f"{ctx.guild.id}":
                    ch.append(f"{num}. | {mon["q"]} | {mon["a"][:7]} | {mon["name"][:6]}")
                    num = num + 1
            if len(ch) == 0:
                await ctx.reply(embed=discord.Embed(title=f"自動返信リスト", description=f"まだありません。"))
                return
            await ctx.reply(embed=discord.Embed(title=f"自動返信リスト", description=f"何番？  反応する言葉　返信する言葉　　名前```{"\n".join(ch)}```"))
        except:
            await ctx.send("エラー。")

async def setup(bot):
    await bot.add_cog(autoreply(bot))