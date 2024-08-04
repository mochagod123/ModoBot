import discord
from discord.ext import commands
import asyncio
import sys

class FastBoot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(FastBoot(bot))