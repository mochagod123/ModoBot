import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient
import aiohttp
from discord import Webhook
import json
import requests
import io
from functools import cache
import sys
import urllib
import re

def NameSelect(id: int):
    username = f"😊"
    ownername = f"🔨"
    premiumname = f"💎"
    hunter = f"🐲"
    money = f"💰"
    if id == 1206048010740432906:
        return ownername
    elif id == 1210579549230989358:
        return premiumname
    elif id == 1217596121702993970:
        return hunter
    elif id == 1218897983555506236:
        return money
    else:
        return username

class Global(commands.Cog):
    def __init__(self, bot):
        
        self.bot = bot

    async def send_gmute(self, userid: discord.User):
        chid = []
        client = MongoClient('mongodb://localhost:27017/')
        for channels in client["Main"]["GlobalChat"].find():
            if channels["Name"] == "gban":
                chid.append(channels["IDs"])

        for ch in chid:
            channel = self.bot.get_channel(int(ch))
            async with aiohttp.ClientSession() as session:
                ch_webhooks = await channel.webhooks()
                whname = f"ModoBot-Global-gban"
                webhooks = discord.utils.get(ch_webhooks, name=whname)
                if webhooks is None:
                    webhooks = await channel.create_webhook(name=f"{whname}")
                webhook = Webhook.from_url(webhooks.url, session=session)
                await webhook.send(f"「{userid.display_name}」をGMuteしました。", username=f"🔨 ModoBotGMuteSystem-System", avatar_url=f"https://media.discordapp.net/attachments/1265857640026603520/1267938279542493276/gmuteimage.png?ex=66aa9b0a&is=66a9498a&hm=3776fc3058bb7db45b756048d9cc7270ded863517d3378ef8f3be2be7bc39247&=&format=webp&quality=lossless&width=434&height=468")

    async def send_gban(self, userid: discord.User):
        chid = []
        client = MongoClient('mongodb://localhost:27017/')
        for channels in client["Main"]["GlobalChat"].find():
            if channels["Name"] == "gban":
                chid.append(channels["IDs"])

        for ch in chid:
            channel = self.bot.get_channel(int(ch))
            async with aiohttp.ClientSession() as session:
                ch_webhooks = await channel.webhooks()
                whname = f"ModoBot-Global-gban"
                webhooks = discord.utils.get(ch_webhooks, name=whname)
                if webhooks is None:
                    webhooks = await channel.create_webhook(name=f"{whname}")
                webhook = Webhook.from_url(webhooks.url, session=session)
                await webhook.send(f"「{userid.display_name}」をGBANしました。", username=f"🔨 ModoBotGBANSystem-System", avatar_url=f"https://media.discordapp.net/attachments/1265857640026603520/1267938279215333532/gbansystem.png?ex=66aa9b0a&is=66a9498a&hm=b406675ee05e38b697463b0866ba8f1146206f68519f7030b2b14222a099ffc1&=&format=webp&quality=lossless&width=434&height=468")

    async def send_login(self, name: str):
        chid = []
        client = MongoClient('mongodb://localhost:27017/')
        for channels in client["Main"]["GlobalChat"].find():
            if channels["Name"] == f"{name}":
                chid.append(channels["IDs"])

        for ch in chid:
            channel = self.bot.get_channel(int(ch))
            async with aiohttp.ClientSession() as session:
                ch_webhooks = await channel.webhooks()
                whname = f"ModoBot-Global-{name}"
                webhooks = discord.utils.get(ch_webhooks, name=whname)
                if webhooks is None:
                    webhooks = await channel.create_webhook(name=f"{whname}")
                webhook = Webhook.from_url(webhooks.url, session=session)
                await webhook.send(f"新しいサーバーが入出したよ！", username=f"🔨 GlobalChat-Join", avatar_url=f"https://media.discordapp.net/attachments/1265857640026603520/1268169914154483743/join.png?ex=66ab72c4&is=66aa2144&hm=b30c0a8208ac92fc398dea75c6daa6b56e693c5dcb7b341c7cf7c2244a329d4a&=&format=webp&quality=lossless")

    async def send_message(self, name: str, message: str, userid: int, displayname: str, guildname: str, avatar: str, channelid: int, fileurl=None, filename=None):
        chid = []

        INVITE_PATTERN = re.compile(r"(https?://)?((ptb|canary)\.)?(discord\.(gg|io)|discord(app)?.com/invite)/[0-9a-zA-Z]+")

        client = MongoClient('mongodb://localhost:27017/')

        for channels in client["Main"]["GlobalChat"].find():
            if channels["Name"] == name:
                chid.append(channels["IDs"])

        for ch in chid:
            channel = self.bot.get_channel(int(ch))
            if not channel.id == channelid:
                async with aiohttp.ClientSession() as session:
                    files = []
                    if fileurl:
                        u = urllib.parse.unquote(fileurl)
                        fio = io.BytesIO()
                        async with session.get(u) as r:
                            fio.write(await r.read())
                        fio.seek(0)
                        files.append(discord.File(fio, filename=f"{filename}"))
                        fio.close()
                        ch_webhooks = await channel.webhooks()
                        whname = f"ModoBot-Global-{name}"
                        webhooks = discord.utils.get(ch_webhooks, name=whname)
                        if webhooks is None:
                            webhooks = await channel.create_webhook(name=f"{whname}")
                        webhook = Webhook.from_url(webhooks.url, session=session)
                        await webhook.send(re.sub(INVITE_PATTERN, "[Invite link]", message.replace("@", "＠")), username=f"{NameSelect(userid)}{displayname}-{userid}-{guildname}", avatar_url=f"{avatar}", files=files)
                    else:
                        ch_webhooks = await channel.webhooks()
                        whname = f"ModoBot-Global-{name}"
                        webhooks = discord.utils.get(ch_webhooks, name=whname)
                        if webhooks is None:
                            webhooks = await channel.create_webhook(name=f"{whname}")
                        webhook = Webhook.from_url(webhooks.url, session=session)
                        await webhook.send(re.sub(INVITE_PATTERN, "[Invite link]", message.replace("@", "＠")), username=f"{NameSelect(userid)}{displayname}-{userid}-{guildname}", avatar_url=f"{avatar}")

    async def checkgmute(self, user: discord.User):
        client = MongoClient('mongodb://localhost:27017/')
        for usercheck in client['Main']["GMute"].find():
            if str(user.id) == usercheck["IDs"]:
                return True

    @commands.Cog.listener("on_message")
    async def on_message_global(self, message):
        if message.author.bot:
            return
        if message.author.id == self.bot.user.id:
            return

        if (type(message.channel) == discord.DMChannel):
            return

        if await self.checkgmute(message.author):
            return

        client = MongoClient('mongodb://localhost:27017/')

        try:
            for channelss in client["Main"]["GlobalChat"].find():
                if channelss["IDs"] == str(message.channel.id):
                    if not message.reference:
                        if message.attachments != []:
                            u = message.attachments[0].url
                            na = message.attachments[0].filename
                            await self.send_message(channelss["Name"], f"{message.content}\n+File", message.author.id, message.author.display_name, message.guild.name, message.author.avatar.url, message.channel.id, f"{u}", f"{na}")
                        else:
                            await self.send_message(channelss["Name"], message.content, message.author.id, message.author.display_name, message.guild.name, message.author.avatar.url, message.channel.id)
                    else:
                        reference_msg = await message.channel.fetch_message(message.reference.message_id)
                        if message.attachments != []:
                            u = message.attachments[0].url
                            na = message.attachments[0].filename
                            await self.send_message(channelss["Name"], f"「{reference_msg.author.display_name}」さんに返信しました。\n-> {message.content}\n+File", message.author.id, message.author.display_name, message.guild.name, message.author.avatar.url, message.channel.id, f"{u}", f"{na}")
                        else:
                            await self.send_message(channelss["Name"], f"「{reference_msg.author.display_name}」さんに返信しました。\n-> {message.content}", message.author.id, message.author.display_name, message.guild.name, message.author.avatar.url, message.channel.id)
        except:
            await message.channel.send(f"GlobalChat-Crashed!\n{sys.exc_info()}")

    @commands.group(invoke_without_command=True)
    async def globals(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @globals.group()
    @commands.has_permissions(manage_channels=True)
    async def talkglobal(self, ctx, a: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            webhook = await ctx.channel.create_webhook(
                name=f"ModoBot-Global-{a}",
                )
            add_datad = {f"IDs": f"{ctx.channel.id}", f"Name": f"{a}"}
            client['Main']["GlobalChat"].delete_one(add_datad)
            add_data = {f"IDs": f"{ctx.channel.id}", f"Name": f"{a}"}
            client['Main']["GlobalChat"].insert_one(add_data)
            embed=discord.Embed(title=f"GlobalChat-Join", description=f"グローバルチャットにログインしました。\nName: {a}", color=0x3acf26)
            await ctx.send(embed=embed)
            await self.send_login(a)
        except:
            await ctx.send(f"エラー!\n{sys.exc_info()}")

    @globals.group()
    @commands.is_owner()
    async def adminglobal(self, ctx, a: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            webhook = await ctx.channel.create_webhook(
                name=f"ModoBot-Global-{a}",
                )
            add_datad = {f"IDs": f"{ctx.channel.id}", f"Name": f"{a}"}
            client['Main']["GlobalChat"].delete_one(add_datad)
            add_data = {f"IDs": f"{ctx.channel.id}", f"Name": f"{a}"}
            client['Main']["GlobalChat"].insert_one(add_data)
            embed=discord.Embed(title=f"GlobalChat-Join", description=f"Botの管理者権限でグローバルチャットに\nログインしました。\nName: {a}", color=0x3acf26)
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー!")

    @globals.group()
    @commands.is_owner()
    async def deleteglobal(self, ctx, a: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"Name": f"{a}"}
            client['Main']["GlobalChat"].delete_many(add_datad)
            embed=discord.Embed(title=f"GlobalChat-Join", description=f"Botの管理者権限でグローバルチャットから全員退出させました。\nName: {a}", color=0x3acf26)
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー!")

    @globals.group()
    async def gclist(self, ctx, a: str):
        chid = []
        guilds = []
        try:
            client = MongoClient('mongodb://localhost:27017/')
            for channels in client["Main"]["GlobalChat"].find():
                if channels["Name"] == a:
                    chid.append(channels["IDs"])

            for ch in chid:
                channel = self.bot.get_channel(int(ch))
                guilds.append(channel.guild.name)

            embed = discord.Embed(title=f"{a}に参加している鯖", description=f"{"\n".join(guilds)}")
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー!")

    @globals.group()
    async def grlist(self, ctx):
        chid = []
        try:
            client = MongoClient('mongodb://localhost:27017/')
            for channels in client["Main"]["GlobalChat"].find():
                chid.append(channels["Name"])

            for i, f in enumerate(chid): # 基準となるフルーツとインデックスを取得
                for compared_i, compared_f in enumerate(chid): # 比較対象のフルーツとインデックスを取得
                    
                    if i != compared_i and f == compared_f: # 両者のインデックスが同じではなく、要素が同じ場合、比較対象を削除
                        chid.pop(i)

            embed = discord.Embed(title=f"グローバルチャットの部屋リスト", description=f"{"\n".join(chid)}")
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー!")

    @globals.group()
    @commands.has_permissions(manage_channels=True)
    async def deactivate(self, ctx):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"IDs": f"{ctx.channel.id}"}
            client['Main']["GlobalChat"].delete_many(add_datad)
            embed=discord.Embed(title=f"GlobalChat-Leave", description=f"グローバルチャットからログオフしました。", color=0x3acf26)
            await ctx.send(embed=embed)
        except:
            await ctx.send("エラー!")

async def setup(bot):
    await bot.add_cog(Global(bot))