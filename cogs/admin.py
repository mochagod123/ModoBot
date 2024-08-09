import discord
from discord.ext import commands
import asyncio
import os
from pymongo import MongoClient
import sys

class AdminCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_gban(self, userid: discord.User):
        chid = []
        client = MongoClient('mongodb://localhost:27017/')
        for channels in client["Main"]["GlobalChat"].find():
            if channels["Name"] == "gban":
                try:
                    chid.append(channels["IDs"])
                except:
                    continue

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


    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def admins(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @admins.group()
    @commands.has_permissions()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def server_list(self, ctx):
        join_servers_information = '\n'.join(f"{s.name}, {s.id}, {s.member_count}人" for s in self.bot.guilds)
        embed = discord.Embed(title="導入鯖一覧", description=join_servers_information)
        await ctx.send(embed=embed)

    @admins.command()
    @commands.cooldown(3, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def reload(self, ctx, a: str):
        if (os.path.isfile(f"cogs/{a}.py")):
            await self.bot.reload_extension(f"cogs.{a}")
            await ctx.reply("Reload .. OK!")
        else:
            await ctx.reply("Error! No File!")

    @admins.command()
    @commands.cooldown(3, 10, type=commands.BucketType.user)
    @commands.is_owner()
    async def addload(self, ctx, a: str):
        if (os.path.isfile(f"cogs/{a}.py")):
            await self.bot.load_extension(f"cogs.{a}")
            await ctx.reply("Load .. OK!")
        else:
            await ctx.reply("Error! No File!")

    @admins.group()
    @commands.is_owner()
    async def gmute(self, ctx, *, member: discord.User):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"IDs": f"{member.id}"}
            client['Main']["GMute"].delete_one(add_datad)
            client['Main']["GMute"].insert_one(add_datad)
            await self.send_gmute(member)
            await ctx.send(f"{member.display_name}をGMuteをしました。")
        except:
            await ctx.send(f"error!\n{sys.exc_info()}")

    @admins.group()
    @commands.is_owner()
    async def ungmute(self, ctx, *, member: discord.User):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            add_datad = {f"IDs": f"{member.id}"}
            client['Main']["GMute"].delete_one(add_datad)
            await ctx.send(f"{member.display_name}のGMuteを解除をしました。")
        except:
            await ctx.send(f"error!\n{sys.exc_info()}")

    @admins.command() # Mass Ban Command
    @commands.is_owner()
    async def gban(self, ctx, user: discord.User):
        await ctx.send(f"{user.display_name}をGBANしています..")
        usid = []
        for guild in self.bot.guilds:
            try:
                await guild.ban(user)
                usid.append(f"{guild.name}..OK")
                await asyncio.sleep(1)
            except:
                usid.append(f"{guild.name}..Error")
        await ctx.send(f"{user.display_name}のGBANが完了しました。\n```{'\n'.join(usid)}```")
        await self.send_gban(user)

    @admins.command() # Mass Ban Command
    @commands.is_owner()
    async def ungban(self, ctx, user: discord.User):
        await ctx.send(f"{user.display_name}のGBANを解除しています..")
        usid = []
        for guild in self.bot.guilds:
            try:
                await guild.unban(user)
                usid.append(f"{guild.name}..OK")
                await asyncio.sleep(1)
            except:
                usid.append(f"{guild.name}..Error")
        await ctx.send(f"{user.display_name}のGBAN解除が完了しました。\n```{'\n'.join(usid)}```")

    @admins.command() # Mass Ban Command
    @commands.is_owner()
    async def pollgban(self, ctx, user: discord.User, riyu: str):
        embed=discord.Embed(title=f"「{user.name}」のGBANをしたほうがいい？\n理由:「{riyu}」", description=f"```[1] ... したほうがいい！！\n[2] ... しないほうがいい。。```\n下のリアクションを付けて答えてください。", color=0xa6c412)
        m = await ctx.send(embed=embed)
        await m.add_reaction("<:1_:1266356576948850780>")
        await m.add_reaction("<:2_:1266356598524215326>")

    @admins.command() # Mass Ban Command
    @commands.is_owner()
    async def sleave(self, ctx, server: int):
        try:
            user = await self.bot.fetch_guild(int(server))
            await user.leave()
            await ctx.send(f"{user.name}から退出させました。")
        except:
            await ctx.send("Error!")

    @admins.command() # Mass Ban Command
    @commands.is_owner()
    async def editmoney(self, ctx, user: discord.User, money: int):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            for mons in client["Main"]["Money"].find():
                if mons["IDs"] == f"{user.id}":
                    if mons == None:
                        add_datad = {f"IDs": f"{user.id}"}
                        client['Main']["Money"].delete_one(add_datad)
                        add_data = {f"IDs": f"{user.id}", f"Money": f"{money}"}
                        client['Main']["Money"].insert_one(add_data)
                    else:
                        add_datad = {f"IDs": f"{user.id}"}
                        client['Main']["Money"].delete_one(add_datad)
                        add_data = {f"IDs": f"{user.id}", f"Money": f"{int(mons["Money"]) + money}"}
                        client['Main']["Money"].insert_one(add_data)
                    embed=discord.Embed(title="お金操作", description=f"{user.name}さんの所持金を「{money}」円増やしました。", color=0xffc800)
                    await ctx.send(embed=embed)

        except:
            await ctx.send("Error!")

    @admins.command() # Mass Ban Command
    @commands.is_owner()
    async def fine(self, ctx, user: discord.User):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            for mons in client["Main"]["Money"].find():
                if mons["IDs"] == f"{user.id}":
                    if mons == None:
                        add_datad = {f"IDs": f"{user.id}"}
                        client['Main']["Money"].delete_one(add_datad)
                        add_data = {f"IDs": f"{user.id}", f"Money": f"0"}
                        client['Main']["Money"].insert_one(add_data)
                    else:
                        add_datad = {f"IDs": f"{user.id}"}
                        client['Main']["Money"].delete_one(add_datad)
                        add_data = {f"IDs": f"{user.id}", f"Money": f"0"}
                        client['Main']["Money"].insert_one(add_data)
                    embed=discord.Embed(title="罰金", description=f"{user.name}さんからすべてのお金を取り上げました。", color=0xffc800)
                    await ctx.send(embed=embed)

        except:
            await ctx.send("Error!")

async def setup(bot):
    await bot.add_cog(AdminCommand(bot))