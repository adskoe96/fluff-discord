#АВТОРЫ: SandeMC и adskoe96.

import os
import discord
import qrcode
import logging
import sys
import traceback
import requests
import random
import urllib
from discord.ext.commands import Bot
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pysstv.grayscale import Robot24BW
#
#VARIABLES
#
token = os.getenv("TOKEN")
bot = commands.Bot(command_prefix='/')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#HITS
hits = ['ударил', 'ударил, но получил сдачи от', 'добил до отключки', 'хотел ударить, но пощадил', 'ударил до смерти и спрятал труп в мусорку', 'опоздал до удара']
#ERRORS
errors = ['`...Aus wie ein scheiss Autounfall`', "`Ich brauch 'nen verschissenen Arzt.`", "`Je déteste le cigarette électronique.`", "`Mala palabra.`", "`Faites attention.`", "`Sì, capisco.`", "`Siéntate`", "`Aéme su cabeza.`", "`I'm feeling a bit sick.`", "`Ich brauch nen verschissenen Arzt.`", "`I don't feel too well.`"]
#COMMAND ERROR
unknown_command_error = ["Неизвестная команда." + " " + random.choice(errors), "Неизветная команда."]
#NO PERMISSION
no_permission_error = ["У вас нет разрешения на использование этой команды." + " " + random.choice(errors), "У вас нет разрешения на использование этой команды."]

#
#BOT ON READY
#
@bot.event
async def on_ready():
	await bot.wait_until_ready()
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='/h | @adskoe96'))
	botname = bot.user
	print(f"Бот {botname} готов!")
#
#HELP MENU
#
@bot.command()
async def h(ctx):
	author = ctx.message.author
	await ctx.send(embed = discord.Embed(title = 'Help menu.', description = f'{author.mention},\n/h - помощь.\n/hello - приветствие с ботом.\n/qr [text] - перевести слова в QR код\n/myInfo - узнать больше о вас информации\n/getInfo [mention] - узнать информацию о пользователе.\n\ndeveloped by - <@413001095720337409>', color=0x24ff00))
#
#START
#
@bot.command()
@commands.has_permissions(kick_members=True)
async def start(ctx, *args):
	howdy = discord.Game(name=" ".join(args[:]), type=3)
	await bot.change_presence(status=discord.Status.idle, activity=howdy)
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
#HELLO
#
@bot.command()
async def hello(ctx):
	author = ctx.message.author
	await ctx.send(f'Привет, {author.mention}!')
#
#SSTV24BW
#
@bot.command()
async def sstv(ctx, *args):
	author = ctx.message.author
	resp = requests.get(args, stream=True)
	sstv = Robot24BW(img, 44100, 16)
	sstv.write_wav("sstv.wav")
	await ctx.send(f'{author.mention}.', file="sstv.wav")
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
async def getInfo(ctx, user: discord.Member):
    img = Image.open("infoimgimg.png") #Replace infoimgimg.png with your background 
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Modern_Sans_Light.otf", 100) #Make sure you insert a valid font from your folder.
    fontbig = ImageFont.truetype("Fitamint Script.ttf", 400) #Make sure you insert a valid font from your folder.
    #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
    draw.text((200, 0), "Information:", (255, 255, 255), font=fontbig) #draws Information
    draw.text((50, 500), "Username: {}".format(user.name), (255, 255, 255), font=font) #draws the Username of the user
    draw.text((50, 700), "ID: {}".format(user.id), (255, 255, 255), font=font) #draws the user ID
    draw.text((50, 900), "User Status: {}".format(user.status), (255, 255, 255), font=font) #draws the user status
    draw.text((50, 1100), "Account created: {}".format(user.created_at), (255, 255, 255), font=font) #When the account was created 
    draw.text((50, 1300), "Nickname: {}".format(user.display_name), (255, 255, 255), font=font) # Nickname of the user
    draw.text((50, 1500), "Users' Top Role: {}".format(user.top_role), (255, 255, 255), font=font) #draws the top rome
    draw.text((50, 1700), "User Joined: {}".format(user.joined_at), (255, 255, 255), font=font) #draws info about when the user joined
    img.save('infoimg2.png') #Change infoimg2.png if needed.
    discordfile=discord.File(fp="infoimg2.png")
    await ctx.send(file=discordfile)
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
#adh
#
@bot.command()
@commands.has_permissions(kick_members=True)
async def adh(ctx):
	author = ctx.message.author
	await author.send(embed = discord.Embed(title = 'Admin help menu.', description = f'{author.mention},\n/h - помощь.\n/clear [число] - очистка чата от сообщений (очистка зависит от числа).\n/start [текст] - назначить активность бота в свой текст.\n/say [канал] [текст] - сказать что-то от имени бота.\n\ndeveloped by - <@413001095720337409>', color=0x24ff00))
#
#HIT
#
@bot.command()
async def hit(ctx, member: discord.Member):
	author = ctx.message.author
	await ctx.send(embed = discord.Embed(title = f'{author.name}' + ' ' + random.choice(hits) + ' ' + f' {member.name}', color=0x00a3ff).set_image(url="https://www.yapfiles.ru/files/351061/kotyboksgifkipesochnica104344.gif"))
#
#ERRORS
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

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Пожалуйста, подождите {} секунд и попробуйте снова.".format(math.ceil(error.retry_after)))
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
        await ctx.send(random.choice(unknown_command_error))
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send('Эта команда не может быть использована в личке.')
        except discord.Forbidden:
            pass
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send(random.choice(no_permission_error))
        return

    # ignore all other exception types, but print them to stderr
    print('Игнорирование ошибки в команде {}:'.format(ctx.command), file=sys.stderr)

    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
#
#RUN TOKEN
#
bot.run(token)