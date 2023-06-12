import discord
from discord.ext import commands
from tic_tac_toe import TicTacToe
from queue_navigation_methods import *
from player_elo_manager import *

@commands.command(name='joinqueue', help='Join the game queue', category='Game')
async def joinqueue(ctx, user=None):
    if player_is_in_game_queue(ctx.author):
        await ctx.send("You're already waiting for a game!")
        return
    if player_is_in_ongoing_game(ctx.author):
        await ctx.send("You're already in a game!")
        return
    # convert author to string so that it can be used as a key in the dictionary
    playersLookingForGame[str(ctx.author)] = user
    await ctx.send(f"{str(ctx.author)} has joined the game queue!")

@commands.command(name='leavequeue', help='Leave the game queue', category='Game')
async def leavequeue(ctx):
    if str(ctx.author) not in playersLookingForGame:
        await ctx.send("You're not waiting for a game!")
        return
    del playersLookingForGame[str(ctx.author)]
    await ctx.send("You've left the game queue.")

@commands.command(name='accept', help='Accept a tic tac toe game', category='Game')
async def accept(ctx, user):
    if player_is_in_ongoing_game(ctx.author):
        await ctx.send("You're already in a game!")
        return
    if str(ctx.author) in playersLookingForGame:
        await ctx.send("You're waiting for a game! Leave the queue before accepting a match!")
        return
    if user not in playersLookingForGame:
        await ctx.send(f"{user} isn't waiting for a game!")
        return
    if playersLookingForGame[user] != str(ctx.author) and playersLookingForGame[user] != None:
        await ctx.send("That user is waiting for a game with someone else!")
        return
    
    del playersLookingForGame[user]
    game = TicTacToe()

    # X always goes first, so the first player is always the user who started the game
    key = make_key(user, str(ctx.author))
    ongoingGames[key] = game
    await ctx.send("Let's play tic tac toe!")
    await ctx.send(game.board_to_string())

@commands.command(name='move', help='Make a move in tic tac toe', category='Game')
async def move(ctx, square):
    # if square is not a number, return
    try:
        int(square)
    except ValueError:
        await ctx.send("Square must be a number!")
        return
    # find the game the caller is in
    for k in ongoingGames:
        if user_is_in_game(k, ctx.author):
            key = k
            break
    else:
        await ctx.send("You're not in a game!")
        return
    game = ongoingGames[key]
    # the first player is always X and the second player is always O
    xPlayer = key.split(SPACER_CHARACTER)[0]
    oPlayer = key.split(SPACER_CHARACTER)[1]
    if game.turnPlayer == 'X' and str(ctx.author) != xPlayer:
        await ctx.send("It's not your turn!")
        return
    if game.turnPlayer == 'O' and str(ctx.author) != oPlayer:
        await ctx.send("It's not your turn!")
        return
    if not game.make_move(int(square)):
        await ctx.send("Invalid move!")
        return
    
    await ctx.send(f"{str(ctx.author)} played on {square}")
    await ctx.send(game.board_to_string())

    opponent = xPlayer if str(ctx.author) == oPlayer else oPlayer

    if game.check_win():
        await ctx.send(f"{game.turnPlayer} wins!")
        del ongoingGames[key]
        update_player_stats(str(ctx.author), opponent)
        return
    
    if game.check_draw():
        await ctx.send("It's a draw!")
        del ongoingGames[key]
        update_player_stats(str(ctx.author), opponent, True)
        return
    
    game.switch_turn_player()

# showqueue
@commands.command(name='showqueue', help='List the players waiting for a game', category='Game')
async def showqueue(ctx):
    if len(playersLookingForGame) == 0:
        await ctx.send("There's no one waiting for a game!")
        return
    message = "Players waiting for a game:\n"
    for player in playersLookingForGame:
        # if the player is waiting for a game with a specific user, show that
        if playersLookingForGame[player] != None:
            message += f"{player} v {playersLookingForGame[player]}\n"
        else:
            message += f"{player} v Anyone\n"
    await ctx.send(message)

@commands.command(name='showgames', help='List the ongoing games', category='Game')
async def showgames(ctx):
    if len(ongoingGames) == 0:
        await ctx.send("There are no ongoing games!")
        return
    message = "Ongoing games:\n"
    for game in ongoingGames:
        message += f"{game}\n"
    await ctx.send(message)

# show board
@commands.command(name='board', help='Show the board of the game you are in', category='Game')
async def board(ctx):
    # find the game the caller is in
    key = None
    for game in ongoingGames:
        if user_is_in_game(game, ctx.author):
            key = game
            break
    else:
        await ctx.send("You're not in a game!")
        return
    game = ongoingGames[key]
    await ctx.send(game.board_to_string())

# show numbered board
@commands.command(name='numberedboard', help='Show the number of each cell on the board', category='Game')
async def numberedboard(ctx):
    tempGame = TicTacToe()
    await ctx.send(tempGame.board_to_string_with_numbers())

# quit
@commands.command(name='quit', help='Quit the game you are in', category='Game')
async def quit(ctx):
    if not user_is_in_game(str(ctx.author)):
        await ctx.send("You're not in a game!")
        return
    # find the game the caller is in
    key = None
    for k in ongoingGames:
        if str(ctx.author) + SPACER_CHARACTER in k or SPACER_CHARACTER + str(ctx.author) in k:
            key = k
            break
    del ongoingGames[key]
    # give the other player a win
    opponent = key.split(SPACER_CHARACTER)[0] if str(ctx.author) == key.split(SPACER_CHARACTER)[1] else key.split(SPACER_CHARACTER)[1]
    update_player_stats(opponent, str(ctx.author))
    await ctx.send("You've quit the game.")
    await ctx.send(f"{opponent} wins!")