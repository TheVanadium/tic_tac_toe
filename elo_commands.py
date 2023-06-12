import discord
from discord.ext import commands
from player_elo_manager import *

@commands.command (name='leaderboard', help='Displays the leaderboard', category='Elo')
async def leaderboard(ctx):
    leaderboard = get_leaderboard()
    message = "Leaderboard:\n"
    for i, player in enumerate(leaderboard):
        message +=  i + f"{player[0]}: {player[1]}\n"
    await ctx.send(message)

@commands.command(name='elo', help='Show your elo', category='Elo')
async def elo(ctx, player_name=None):
    if player_name == None:
        player_name = str(ctx.author)
    if get_player_stat(player_name, 'rating') == None: 
        await ctx.send(f"{player_name} doesn't have an elo yet!")
        return
    message = f"{player_name}'s elo is {get_player_stat(player_name, 'rating')}"
    # if rd is > 100, add a ? to the end to signify that the rating is not accurate
    if get_player_stat(player_name, 'rd') > 100: message += "?"
    await ctx.send(f"{player_name}'s elo is {get_player_stat(player_name, 'rating')}")