import discord
from discord.ext import commands, tasks
import os
from pymongo import MongoClient
import asyncio
import pathlib
import sys
import json

intents = discord.Intents().all()
intents.message_content = True
bot = commands.Bot(command_prefix=('mo#', 'mo.', 'mo!'), intents=intents, help_command=None)

client = MongoClient('mongodb://localhost:27017')

perm_dic = {"add_reactions": "リアクションの追加", "administrator": "管理者", "attach_files": "ファイルを添付", "ban_members": "メンバーをBAN", "change_nickname": "ニックネームの変更", "connect": "接続(ボイスチャンネル)", "create_instant_invite": "招待を作成", "deafen_members": "メンバーのスピーカーをミュート", "embed_links": "埋め込みリンク", "external_emojis": "外部の絵文字を使用する", "external_stickers": "外部のスタンプを使用する(Use Ecternal Stickers)", "kick_members": "メンバーをキック", "manage_channels": "チャンネルの管理", "manage_emojis": "絵文字の管理", "manage_emojis_and_stickers": "絵文字・スタンプの管理", "manage_events": "", "manage_guild": "サーバー管理", "manage_messages": "メッセージの管理", "manage_nicknames": "ニックネームの管理", "manage_permissions": "ロールの管理", "manage_roles": "ロールの管理", "manage_threads": "スレッドの管理", "manage_webhooks": "ウェブフックの管理", "mention_everyone": "`@evryone`,`@here`,すべてのロールにメンション", "move_members": "メンバーを移動(ボイスチャンネル)", "mute_members": "メンバーをミュート", "priority_speaker": "優先スピーカー", "read_message_history": "メッセージ履歴を読む", "read_messages": "チャンネルを見る", "request_to_speak": "スピーカー参加権をリクエスト", "send_messages": "メッセージを送信", "send_tts_messages": "テキスト読み上げメッセージを送信する", "speak": "発言(ボイスチャンネル)", "stream": "WEBカメラ(映像を配信する)", "use_external_emojis": "外部の絵文字を使用する", "use_external_stickers": "外部のスタンプを使用する(Use Ecternal Stickers)", "use_private_threads": "非公開スレッドの使用(Private Thread)", "use_slash_commands": "スラッシュコマンドを使用", "use_threads": "公開スレッドの使用(Public Thread)", "use_voice_activation": "音声検出を使用", "value": "", "view_audit_log": "監査ログを表示", "view_channel": "チャンネルを見る", "view_guild_insights": "サーバーインサイトを見る", }

tokenjson = open('../token.json', 'r')
tokens = json.load(tokenjson)

def t_perm(perm):
    if perm in perm_dic:
        return perm_dic[perm]
    else:
        return perm

@tasks.loop(seconds=300)
async def autodeletetemp():
    check_dir = pathlib.Path("temp")
    for file in check_dir.iterdir():
        if file.is_file():
            file.unlink()

@bot.event
async def on_ready():
    os.system('cls')
    print("======================")
    print("  Created by もどっぐ  ")
    print("======================")
    print("Log >>")
    count = len(bot.guilds)
    raw_ping = bot.latency
    ping = round(raw_ping * 1000)
    await bot.change_presence(activity=discord.CustomActivity(name=f"{count}鯖 | {len(bot.users)}人"))
    autodeletetemp.start()

@bot.event
async def on_guild_join(guild):
    if guild.system_channel:
        embed=discord.Embed(title="ModoBotを入れていただきありがとうございます！", description="ゆっくりしていってね！", color=0x00ccff)
        await guild.system_channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandOnCooldown):
        a = None
        return a
    elif isinstance(err, commands.BotMissingPermissions):
        p = "\n".join([t_perm(perm) for perm in err.missing_permissions])
        embed=discord.Embed(title="Botの権限がありません!", description=f"{p}", color=0xff0000)
        await ctx.send(embed=embed)
    elif isinstance(err, commands.MissingPermissions):
        p = "\n".join([t_perm(perm) for perm in err.missing_permissions])
        embed=discord.Embed(title="あなたの権限がありません!", description=f"{p}", color=0xff0000)
        await ctx.send(embed=embed)
    elif isinstance(err, commands.errors.MissingRequiredArgument ):
        await ctx.send("引数が足りないよ！")

@bot.event
async def setup_hook():
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            await bot.load_extension(f"cogs.{cog[:-3]}")

bot.run(tokens["token"])