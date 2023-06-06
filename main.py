import discord
from discord.ext import commands
# from bot import MyClient

intents = discord.Intents.all()

# print the intents value to the console
print(intents.value)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='ping', help='Responds with "beep boop beep"')
async def ping(ctx):
    await ctx.send('pong')

bot.run('MTExNTY2MDEwNTYxOTM0NTU0OQ.Gpz4TG.oD6LAqM2W6YLvc8UvHM88-3PJ_D4FfFIcC0VmY')