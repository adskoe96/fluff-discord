#АВТОРЫ: SandeMC и adskoe96.

import os
import discord
import qrcode
import logging
import sys
import traceback
import requests
import youtube_dl
import time
import asyncio
import urllib
import shutil
from gtts import gTTS
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from random import choice
#
#VARIABLES
#
token = os.getenv("TOKEN")
queue = []
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {'format': 'bestaudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
status = ['Jamming out to music!', 'Eating!', 'Sleeping!']

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

bot = commands.Bot(command_prefix='>')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#
#BOT ON READY
#
@bot.event
async def on_ready():
	await bot.wait_until_ready()
	activity = discord.Game(name="@adskoe96", type=3)
	await bot.change_presence(status=discord.Status.idle, activity=activity)
	botname = bot.user
	print(f"Бот {botname} готов!")
#
#HELP MENU
#
@bot.command()
async def h(ctx):
	author = ctx.message.author
	await ctx.send(embed = discord.Embed(title = f'Help menu right here, {author.name}.', description = f'https://adskoe96.github.io/links/pages/fluffy.html', color=0x24ff00))
#
#START
#
@bot.command()
@commands.has_permissions(kick_members=True)
async def start(ctx, *args):
    author = ctx.message.author.name
    await ctx.message.delete()
    if author == "adsk":
	    howdy = discord.Game(name=" ".join(args[:]), type=3)
	    await bot.change_presence(status=discord.Status.idle, activity=howdy)
    else:
        message = await ctx.channel.send("Nope.")
        await asyncio.sleep(2)
        await message.delete()
#
#CLEAR
#
@bot.command()
@commands.has_permissions(kick_members=True)
async def clear(ctx, amount=None):
	author = ctx.message.author
	await ctx.channel.purge(limit=int(amount))
	await ctx.channel.send(f':white_check_mark: Сообщения успешно удалены пользователем: {author.mention}')
#
#WEBSCRAPING
#
@bot.command()
async def ws(ctx, url):
    try:
        author = ctx.message.author
        page = urllib.request.urlopen(url)
        f = open("index.html", "wb")
        shutil.copyfileobj(page, f)
        f.close()
        with open("index.html", "rb") as file:
            await ctx.send(f"{author.mention}, your file here:", file=discord.File(file, "index.html"))
        await ctx.message.delete()
    except:
        await ctx.message.delete()
        message = await ctx.channel.send('Url error.')
        await asyncio.sleep(2)
        await message.delete()
#
#QR
#
@bot.command()
async def qr(ctx, *args):
	nameofqrcode = "code.jpg"
	img = qrcode.make(" ".join(args[:]))
	img.save(nameofqrcode)
	discordfile=discord.File(fp=nameofqrcode)
	await ctx.send(file=discordfile)
#
#SAY
#
@bot.command()
@commands.has_permissions(kick_members=True)
async def say(ctx, channel: discord.TextChannel, *, text):
	await channel.send(text)
	await ctx.message.delete()
#
#JOIN
#
@bot.command(pass_context=True)
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
#
#PLAY
#
@bot.command(name='play', help='This command plays songs')
async def play(ctx, url):
    with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio(URL))
#
#LEAVE
#
@bot.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
#
#PAUSE
#
@bot.command(pass_context=True)
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()
#
#RESUME
#
@bot.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()
#
#STOP
#
@bot.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()
#
#MYINFO
#
@bot.command()
async def myInfo(ctx):
	author = ctx.message.author
	await ctx.send(embed = discord.Embed(title = f'{author.name}', description= f'Ping: {author.mention}\nAvatar URL: {author.avatar_url}\nUserId: {author.id}', color=0x00a3ff).set_thumbnail(url=author.avatar_url))
#
#GETINFO
#
@bot.command()
async def getInfo(ctx, member: discord.Member):
	await ctx.send(embed = discord.Embed(title = f'{member.name}', description= f'Ping: {member.mention}\nAvatar URL: {member.avatar_url}\nUserId: {member.id}', color=0x00a3ff).set_thumbnail(url=member.avatar_url))
#
#Looping status
#
@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))
#
#ERROR
#
@bot.event
async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, и {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' и '.join(missing)
        _message = 'Мне нужное это разрешение(ия) чтобы сделать эту команду: **{}**'.format(fmt)
        await ctx.send(_message)
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send('Эта команда была отключена.')
        return

    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, и {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' и '.join(missing)
        _message = 'Вам нужно это разрешение(ия) на использование этой команды: **{}**'.format(fmt)
        await ctx.send(_message)
        return

    if isinstance(error, commands.UserInputError):
        await ctx.channel.send("Неизвестная команда.")
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send('Эта команда не может быть использована в личке.')
        except discord.Forbidden:
            pass
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send("У вас нет разрешения на использование этой команды")
        return

    # ignore all other exception types, but print them to stderr
    print('Игнорирование ошибки в команде {}:'.format(ctx.command), file=sys.stderr)

    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
#
#RUN TOKEN
#
bot.run(token)