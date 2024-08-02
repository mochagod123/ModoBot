import discord
from discord.ext import commands
import asyncio

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
        await ctx.send(f'Giveコマンド\n```/give @p {itemid}```')

async def setup(bot):
    await bot.add_cog(Minecraft(bot))