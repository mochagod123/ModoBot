import discord
from discord.ext import commands
import asyncio
import sys

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def mc(self,ctx):
        e = discord.Embed(title="サブコマンドがないです!", description="このメッセージは、\n5秒後に削除されます。")
        msg = await ctx.reply(embed=e)
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()

    @mc.group()
    @commands.has_permissions()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def give(self, ctx, *, itemid: str):
        await ctx.send(f'Giveコマンド\n```/give @p {itemid.replace("@", "")}```')

    @mc.group()
    @commands.has_permissions()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def cbuild(self, ctx):
        e = discord.Embed(title=f"Minecraftコマンドビルダー v1.0\nリアクションを付けて作ります。\n====================\n🌳..Giveコマンド\n⚔..Killコマンド\n✖..終了")
        cmds = ""
        msg = await ctx.send(embed=e)
        await msg.add_reaction("🌳")
        await msg.add_reaction("⚔")
        await msg.add_reaction("✖")
        try:
            while True:
                def check(r, u):
                    if u.id == ctx.author.id:
                        return r.message.id == msg.id
                    else:
                        return False
                r, _ = await self.bot.wait_for("reaction_add", check=check, timeout=None)
                await r.remove(ctx.author)
                if r.emoji == "🌳":
                    def checks(m=ctx.message):
                        return m.author == ctx.author
                    await ctx.send('アイテムIDを入れて')
                    numc = await self.bot.wait_for("message", check=checks, timeout=None)
                    await ctx.send("Giveコマンドを追加しました。")
                    cmds += f"\n/give @p {numc.content.replace("@", "")}"
                elif r.emoji == "⚔":
                    def checks(m=ctx.message):
                        return m.author == ctx.author
                    await ctx.send('ユーザーネームを入れて')
                    numc = await self.bot.wait_for("message", check=checks, timeout=None)
                    await ctx.send("Killコマンドを追加しました。")
                    cmds += f"\n/kill {numc.content.replace("@", "＠")}"
                elif r.emoji == "✖":
                    await ctx.send("コードが完成しました。")
                    await ctx.send(f"```{cmds}```")
                    break
        except:
            await ctx.send(f"Error!\n{sys.exc_info()}")

async def setup(bot):
    await bot.add_cog(Minecraft(bot))