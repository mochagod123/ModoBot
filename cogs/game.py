import discord
from discord.ext import commands
import random
import asyncio
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
import io
import sys
from googletrans import Translator

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def games(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @games.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def uranai(self, ctx):
        unsei = ["大吉", "中吉", "吉", "末吉", "小吉", "凶", "大凶"]
        choice = random.choice(unsei)
        await ctx.send(choice)

    @games.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def whn(self, ctx):
        def check(m=ctx.message):
            return m.author == ctx.author
        num = random.randint(0, 100)
        await ctx.channel.send("1~100までの数字を入れて")
        i = 0
        while True:
            numc = await self.bot.wait_for("message", check=check, timeout=None)
            try:
                if int(numc.content) == num:
                    await ctx.channel.send(f"数字が正しいです！(正解するまでに{i}回かかりました。)")
                    break
                elif int(numc.content) > num:
                    await ctx.channel.send("数字がもっと小さいよ！")
                    i += 1
                    await asyncio.sleep(2)
                elif int(numc.content) < num:
                    await ctx.channel.send("数字がもっと大きいよ！")
                    i += 1
                    await asyncio.sleep(2)
            except:
                await ctx.reply("数字以外入れてる？ゲームを中断するね")
                break

    @games.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def invert(self, ctx, text: str):
        textf = text[::-1]
        embed=discord.Embed(title="文字列を反転")
        embed.add_field(name="反転前", value=f"{text}", inline=False)
        embed.add_field(name="反転後", value=f"{textf}", inline=False)
        await ctx.reply(embed=embed)

    @games.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def cli(self, ctx, text: str):
        embed=discord.Embed(title="改行コードを改行に変換", color=0x00d5ff)
        embed.add_field(name="変換前", value=f"{text.replace("@", "＠")}", inline=False)
        embed.add_field(name="変換後", value=f"{text.replace("\\n", "\n").replace("@", "＠")}", inline=False)
        await ctx.reply(embed=embed)

    @games.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def loop_trans(self, ctx, text: str):
        try:
            translator = Translator()
            jpen = translator.translate(text, src='ja', dest='en')
            enfr = translator.translate(jpen.text, src='en', dest='fr')
            frch = translator.translate(enfr.text, src='fr', dest='zh-cn')
            chjp = translator.translate(frch.text, src='zh-cn', dest='ja')
            c = discord.Embed(title=f"{text}", description=f"JP->EN->FR->ZH->JP")
            msg = await ctx.send(embed=c)
            await asyncio.sleep(2)
            v = discord.Embed(title=f"{jpen.text}", description=f"JP->EN->FR->ZH->JP")
            await msg.edit(embed=v)
            await asyncio.sleep(2)
            a = discord.Embed(title=f"{enfr.text}", description=f"JP->EN->FR->ZH->JP")
            await msg.edit(embed=a)
            await asyncio.sleep(2)
            c = discord.Embed(title=f"{frch.text}", description=f"JP->EN->FR->ZH->JP")
            await msg.edit(embed=c)
            await asyncio.sleep(2)
            s = discord.Embed(title=f"{chjp.text}", description=f"JP->EN->FR->ZH->JP")
            await msg.edit(embed=s)
            await asyncio.sleep(2)
            await ctx.reply("LoopTransが終了しました。")
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

async def setup(bot):
    await bot.add_cog(Game(bot))