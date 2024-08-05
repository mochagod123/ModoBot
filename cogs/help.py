import discord
from discord.ext import commands
import requests

class search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def ping(self, ctx):
        raw_ping = self.bot.latency
        ping = round(raw_ping * 1000)
        await ctx.reply(f"BotのPing値は{ping}msです。")

    @commands.command()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def help(self, ctx, *, arg=None):
        if arg:
            aka = arg.split(' ')
            if aka[0] == "1":
                url = f"https://raw.githubusercontent.com/mochagod123/Help-Text/main/firebot.txt"
                response = requests.get(url)
                embed=discord.Embed(title="ヘルプ！", description=response.text, color=0xd60000)
                await ctx.send(embed=embed)
            elif aka[0] == "2":
                url = f"https://raw.githubusercontent.com/mochagod123/Help-Text/main/firebot2.txt"
                response = requests.get(url)
                embed=discord.Embed(title="ヘルプ！", description=response.text, color=0xd60000)
                await ctx.send(embed=embed)
            elif aka[0] == "3":
                url = f"https://raw.githubusercontent.com/mochagod123/Help-Text/main/firebot3.txt"
                response = requests.get(url)
                embed=discord.Embed(title="ヘルプ！", description=response.text, color=0xd60000)
                await ctx.send(embed=embed)
            elif aka[0] == "4":
                url = f"https://raw.githubusercontent.com/mochagod123/Help-Text/main/firebot4.txt"
                response = requests.get(url)
                embed=discord.Embed(title="ヘルプ！", description=response.text, color=0xd60000)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="ヘルプ！", description="ModoBot ヘルプへようこそ！\n```Prefix .. mo# or mo.```\nページは、```mo#help 1~3```を入力して切り替えます。\n\nad👇", color=0xd60000)
                embed.set_image(url="https://media.discordapp.net/attachments/1267402637880459356/1267402785222299679/ad2.png?ex=66a8a853&is=66a756d3&hm=dead1bc504ded63e0151e39bc66c21642eafdd08a44dc2ebef0a4ecf5ea6eb09&=&format=webp&quality=lossless")
                await ctx.send(embed=embed)
        else:
                embed=discord.Embed(title="ヘルプ！", description="ModoBot ヘルプへようこそ！\n```Prefix .. mo# or mo.```\nページは、```mo#help 1~3```を入力して切り替えます。\n\nad👇", color=0xd60000)
                embed.set_image(url="https://media.discordapp.net/attachments/1267402637880459356/1267402785222299679/ad2.png?ex=66a8a853&is=66a756d3&hm=dead1bc504ded63e0151e39bc66c21642eafdd08a44dc2ebef0a4ecf5ea6eb09&=&format=webp&quality=lossless")
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(search(bot))