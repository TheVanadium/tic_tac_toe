import discord
from discord.ext import commands
from elo_commands import *
from game_commands import *

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

# elo commands
bot.add_command(leaderboard)
bot.add_command(elo)

# game commands
bot.add_command(joinqueue)
bot.add_command(leavequeue)
bot.add_command(accept)
bot.add_command(move)
bot.add_command(showqueue)
bot.add_command(showgames)
bot.add_command(board)
bot.add_command(numberedboard)
bot.add_command(quit)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='ping', help='Responds with "pong" to make sure the bot is working')
async def ping(ctx):
    await ctx.send('pong')

COMMAND_CATEGORIES = {
    'Elo': ['elo', 'leaderboard'],
    'Game': ['accept', 'board', 'joinqueue', 'leavequeue', 'move', 'numberedboard', 'quit', 'showgames', 'showqueue'],
    'Misc': ['help', 'ping']
}
@bot.remove_command('help')
@bot.command(name='help', help='Shows this message')
async def help(ctx, *args):
    if len(args) == 0:
        embed = discord.Embed(title='Help', description='Use !help <command> for more info on a command', color=0x00ff00)
        for category in COMMAND_CATEGORIES:
            embed.add_field(name=category, value=', '.join(COMMAND_CATEGORIES[category]), inline=False)
        await ctx.send(embed=embed)
    elif len(args) == 1:
        command = bot.get_command(args[0])
        if command is None:
            await ctx.send('Command not found')
        else:
            embed = discord.Embed(title=command.name, description=command.help, color=0x00ff00)
            await ctx.send(embed=embed)
    else:
        await ctx.send('Too many arguments')