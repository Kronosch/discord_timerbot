# https://discord.com/api/oauth2/authorize?client_id=1064192553299226725&permissions=0&scope=bot%20applications.commands
import os
import random
import pickle
import json
from datetime import datetime
from datetime import timedelta
import discord
from discord.ext import commands
#from dotenv import load_dotenv

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')

TIMERFILE = 'timerlist.txt'

intents = discord.Intents.default()
intents.message_content = True

bot    = commands.Bot(command_prefix='/', intents=intents)
#info   = commands.errors
timers = {}
#init timer list

try:
    with open(TIMERFILE, 'r') as tf:
        timers = json.load(tf)
except FileNotFoundError:
    timers = {}
except EOFError:
    timers = {}
except:
    timers = {}
print(timers)

def getTimeUnit(unit):
    match unit.upper():
        case 'H':
            munit='hours'
        case 'HRS':
            munit='hours'
        case 'HR':
            munit='hours'
        case 'HOUR':
            munit='hours'
        case 'HOURS':
            munit='hours'
        case 'DAY':
            munit='days'
        case 'DAYS':
            munit='days'
        case 'D':
            munit='days'
        case _:
            munit='days'
    return munit

def timer_add(user: str, starttime: datetime, endtime: datetime, lastseen: datetime):
    m_timer = {}
    m_id = str(user.id)

    m_timer['name']=user.name
    m_timer['discriminator']=user.discriminator
    m_timer['started']=starttime.isoformat()
    m_timer['ending']=endtime.isoformat()
    m_timer['lastseen']=lastseen.isoformat()

    if timer_show(user=user) == None:
        timers[m_id]=m_timer
    else:
        #will update the timer, but only if new endtime is higher
        endtime_existing = datetime.fromisoformat(timers[m_id]['ending'])
        
        if (endtime - endtime_existing).total_seconds() > 0:
            timers[m_id]['ending']   = m_timer['ending']
        
        timers[m_id]['lastseen'] = m_timer['lastseen']

    ret = timers[m_id]['ending']
    with open(TIMERFILE, 'w') as tf:
        json.dump(timers, tf)
    print(timers)
    return ret

def timer_show(user: str):
    print(user.id)
    
    try:
        mtimer = timers[str(user.id)]
    except KeyError:
        mtimer = None

    return mtimer

@bot.command()
async def hello(ctx):
    await ctx.send("Hello")

@bot.command()
async def showtimer(ctx, to: discord.User = commands.Author):
    timer = timer_show(user=to)
    if timer != None:
        msg = 'Your timer ends at: ' + timer['ending']
    else:
        msg = 'No timer active'
    await ctx.send(msg)

@bot.command()    
async def generatetimer(ctx, amount: int, unit: str, to: discord.User = commands.Author):

    now = datetime.now()
    if amount <= 0:
            msg = 'invalid time given'
    munit = getTimeUnit(unit)

    targettime = now
    if munit == 'days':
        targettime = now + timedelta(days=amount)
    if munit == 'hours':
        targettime = now + timedelta(hours=amount)

    set_endtime=timer_add(user=to, starttime=now, endtime=targettime, lastseen=now)
    msg='timer started or updated, lasting to ' + set_endtime

    await ctx.send(msg)

#@bot.error
#async def info_error(ctx, error):
#    if isinstance(error, commands.BadArgument):
#        await ctx.send('I could not find that member...')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

bot.run(TOKEN)
