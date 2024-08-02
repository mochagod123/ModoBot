import discord
from discord.ext import commands
import asyncio
import random
import sys
import time
import io
import json

class Fatal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def fatals(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, *, member: discord.Member):
        await ctx.guild.kick(member)
        await ctx.send(f'{member.mention}をKickしました。')

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, *, member: discord.Member):
        await ctx.guild.ban(member)
        await ctx.send(f'{member.mention}をBANしました。')

    @fatals.group(aliases=["purge"])
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def clear_channel(self, ctx, a: int):
        if a == 0:
            await ctx.channel.purge()
            await ctx.send(f'チャンネルをきれいにしました。')
            return
        else:
            v = a + 1
            await ctx.channel.purge(limit=v)
            await ctx.send(f'チャンネルをきれいにしました。')
            return

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def shuffle(self, ctx):
        member_nicks = []
        targets = []
        for m in ctx.guild.members:
            member_nicks.append(m.display_name)
            targets.append(m)

        try:

            loop = asyncio.get_event_loop()
            random.shuffle(member_nicks)

            for i, m in enumerate(targets):
                loop.create_task(m.edit(nick=member_nicks[i]))

            e = discord.Embed(title=f"`{len(member_nicks)}`人のニックネームをシャッフルしました。")
            await ctx.reply(embed=e)

        except:
            await ctx.reply(f"error!\n{sys.exc_info()}")

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def nickreset(self, ctx):
        targets = []
        for m in ctx.guild.members:
            targets.append(m)
        loop = asyncio.get_event_loop()
        for i, m in enumerate(targets):
            loop.create_task(m.edit(nick=None))  
        e = discord.Embed(title=f"`{len(targets)}`人のニックネームをリセットしました。")
        await ctx.reply(embed=e)

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def anke(self, ctx, a: str):
        targets = []
        for m in ctx.guild.members:
            targets.append(m)
        loop = asyncio.get_event_loop()
        for i, m in enumerate(targets):
            loop.create_task(m.edit(nick=a))  
        e = discord.Embed(title=f"`{len(targets)}`人のニックネームを`{a}`にしました。")
        await ctx.reply(embed=e)

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def nickexport(self, ctx):
        asyncio.get_event_loop()
        res = {}
        for m in ctx.guild.members:
            res[m.id] = m.display_name
        e = discord.Embed(title=f"`{len(res.keys())}`人のニックネームをエクスポートしました。\nCode by SevenBot")
        sio = io.StringIO(json.dumps(res))
        await ctx.reply(
            embed=e,
            file=discord.File(sio, filename=f"NickName.json"),
        )
        sio.close()

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def nickimport(self, ctx):
        try:
            if len(ctx.message.attachments) == []:
                e = discord.Embed(title="エクスポートしたファイルを添付してください。")
                await ctx.reply(embed=e)
                return
            try:
                nicks = json.loads(await ctx.message.attachments[0].read())
            except BaseException:
                e = discord.Embed(title="読み込みに失敗しました。")
                await ctx.reply(embed=e)
                return
            c = 0
            for m in ctx.guild.members:
                try:
                    await m.edit(nick=nicks[str(m.id)])
                    c += 1
                except:
                    pass
            await ctx.channel.send("インポートが完了しました。")
        except:
            await ctx.reply(f"error!\n{sys.exc_info()}")

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def chexport(self, ctx):
        asyncio.get_event_loop()
        res = {}
        c = 0
        for m in ctx.guild.channels:
            res[f"{c}"] = m.name
            c += 1
        e = discord.Embed(title=f"`{len(res.keys())}`個のチャンネルをエクスポートしました。")
        sio = io.StringIO(json.dumps(res))
        await ctx.reply(
            embed=e,
            file=discord.File(sio, filename=f"Channels.json"),
        )
        sio.close()

    @fatals.group()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def chimport(self, ctx):
        try:
            if len(ctx.message.attachments) == []:
                e = discord.Embed(title="エクスポートしたファイルを添付してください。")
                await ctx.reply(embed=e)
                return
            try:
                nicks = json.loads(await ctx.message.attachments[0].read())
            except BaseException:
                e = discord.Embed(title="読み込みに失敗しました。")
                await ctx.reply(embed=e)
                return
            for channel in list(ctx.message.guild.channels):
                try:
                    await channel.delete()
                    await asyncio.sleep(1)
                except:
                    pass
            c = 0
            for ch in nicks:
                await ctx.guild.create_text_channel(name=nicks[f"{c}"])
                c += 1
                await asyncio.sleep(1)
            await ctx.author.send("インポートが完了しました。")
        except:
            await ctx.author.send(f"error!\n{sys.exc_info()}")

async def setup(bot):
    await bot.add_cog(Fatal(bot))